![로또일기배너](https://github.com/user-attachments/assets/20ded711-6844-4399-b69d-39697d3bc48d)


## ʚ🧸ྀིɞ Lotto Diary
나눔 로또에서 주마다 추첨하는 번호를 이용해 일기를 적으면 번호 한개를 주는 일기장입니다. 그동안의 지루했던 일기장과 반면에 재미를 주며 사용자가 일기를 적도록 유도하는 앱입니다.

## Contribute
|<img src="https://avatars.githubusercontent.com/u/128358820?v=4" width="160">|
|:-:|
|[신희성](https://github.com/huise0ng)|

## 🚵 Troubleshooting
- 제가 필요한 동행복권의 나눔로또의 공식 API가 존재하지 않았습니다. <br>
구글에서 정보를 찾던 중 [이것](https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1)을 보게 되었습니다. 주소의 가장 뒷자리 숫자가 회차 번호이고, 회차번호를 입력하면 회차번호에 맞는 로또 정보가 나오는 json 형식의 링크였습니다. 이 링크를 이용해서 저는 [동행복권 api를 개발](https://github.com/Lotto-Diary/Lotto_Diary_Backend/blob/main/main.py)하였습니다. 개발 당시 (24.7.28)를 기준으로 하여 토요일 8시 35분 ~ 9시 30분까지의 추첨 후 등록 시간이 지나면 링크에 나타나있는 회차번호에 +1을 하여 최신 로또 번호를 json 타입으로 가져오도록 구현하였습니다. 
