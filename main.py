# http://127.0.0.1:8000/fetch_lotto?drwNo=1129
from fastapi import FastAPI
import requests
import json
from datetime import datetime

app = FastAPI()

@app.get("/fetch_lotto")
def fetch_lotto(drwNo: int):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        filename = f"lotto_{drwNo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return {"message": f"Data saved to {filename}"}
    else:
        return {"message": "Failed to fetch data"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
