from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta
import jwt
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URL = "mongodb+srv://shinhuiseong07:siniseong@herehere.gnb7p2m.mongodb.net/?retryWrites=true&w=majority&appName=herehere"

try:
    client = MongoClient(MONGODB_URL)
    db = client.LD
    collection = db.users
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")

SECRET_KEY = "2024swmesitergogogowhiteing"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class User(BaseModel):
    name: str
    phone: str
    diary_frequency: int
    id: str 
    password: str

class UserLogin(BaseModel):
    id: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/signup")
async def signup(user: User):
    try:
        existing_user = collection.find_one({"id": user.id})
        if existing_user:
            raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")
        
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user_dict = user.dict()
        user_dict['password'] = hashed_password.decode('utf-8')
        
        result = collection.insert_one(user_dict)
        
        if result.inserted_id:
            return {"status": "success", "message": "사용자가 성공적으로 등록되었습니다."}
        else:
            raise HTTPException(status_code=500, detail="사용자 등록에 실패했습니다.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/signin")
async def signin(user: UserLogin):
    try:
        user_in_db = collection.find_one({"id": user.id})
        
        if user_in_db and bcrypt.checkpw(user.password.encode('utf-8'), user_in_db["password"].encode('utf-8')):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.id}, expires_delta=access_token_expires
            )
            refresh_token = create_access_token(
                data={"sub": user.id},
                expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            )

            collection.update_one({"id": user.id}, {"$set": {"refresh_token": refresh_token}})
            
            return {"access": access_token, "refresh": refresh_token}
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if not id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user_in_db = collection.find_one({"id": id})
        if user_in_db and user_in_db.get("refresh_token") == refresh_token:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            new_access_token = create_access_token(
                data={"sub": id}, expires_delta=access_token_expires
            )
            return {"access": new_access_token}
        else:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
