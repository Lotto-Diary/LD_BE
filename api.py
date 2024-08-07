from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import json
from datetime import datetime
from collections import OrderedDict
import pytz

app = FastAPI()
KST = pytz.timezone('Asia/Seoul')

def get_latest_drwNo():
    drwNo = 1130
    while True:
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
        response = requests.get(url)
        if response.status_code != 200 or response.json().get("returnValue") != "success":
            return drwNo - 1
        drwNo += 1

def fetch_and_save_lotto_data(drwNo):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ordered_data = OrderedDict()
        
        ordered_data['drwNo'] = data.get('drwNo')
        ordered_data['returnValue'] = data.get('returnValue')
        
        numbers = [data.get(f'drwtNo{i}') for i in range(1, 7)]
        numbers.append(data.get('bnusNo'))
        ordered_data['numbers'] = ','.join(map(str, numbers))
        
        filename = "latest_lotto.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(ordered_data, f, ensure_ascii=False, indent=4)
        return ordered_data
    else:
        return {"message": "Failed to fetch data"}

@app.on_event("startup")
def startup_event():
    latest_drwNo = get_latest_drwNo()
    fetch_and_save_lotto_data(latest_drwNo)

@app.get("/")
def root():
    latest_drwNo = get_latest_drwNo()
    return RedirectResponse(url=f"/fetch_lotto?drwNo={latest_drwNo}")

@app.get("/fetch_lotto")
def fetch_lotto(drwNo: int):
    now = datetime.now(KST)
    saturday_20_35 = now.replace(hour=20, minute=35, second=0, microsecond=0)
    saturday_21_30 = now.replace(hour=21, minute=30, second=0, microsecond=0)

    latest_drwNo = get_latest_drwNo()

    if now.weekday() == 5 and saturday_20_35 <= now <= saturday_21_30:
        return JSONResponse(content={"message": "추첨 중입니다"}, status_code=200)

    if now > saturday_21_30 and drwNo == latest_drwNo:
        drwNo += 1

    if drwNo > latest_drwNo + 1:
        return JSONResponse(content={"message": "회차 번호가 존재하지 않습니다"}, status_code=400)

    return fetch_and_save_lotto_data(drwNo)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
