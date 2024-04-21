import requests
import json
import pandas as pd
import time
import random
url = "https://datalab.naver.com/shoppingInsight/getCategory.naver?cid=0"  # get 방식 1분야 목록

headers = {
    "Referer": "https://datalab.naver.com/shoppingInsight/sKeyword.naver?keyword=%ED%8A%B8%EC%9C%84%EB%93%9C%EC%9E%90%EC%BC%93&cid=50000000",

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

res = requests.get(url, headers=headers)
res.raise_for_status()
data = json.loads(res.text)  # JSON 문자열을 파이썬 객체로 변환, 파싱해야 딕셔너리 형태가 돼서 'childList' 키에 접근할 수 있음
data
# 빈 데이터 프레임 생성
df = pd.DataFrame(columns=['cid', 'name'])

for i in range(0, len(data['childList'])) : # 1에서 12까지 반복
    cid_value = data['childList'][i]['cid']  # 'childList'의 i 번째 아이템의 'cid' 값을 추출
    name_value = data['childList'][i]['name']  # 'childList'의 i 번째 아이템의 'cid' 값을 추출

    df = pd.concat([df, pd.DataFrame({'cid': [cid_value], 'name': [name_value]})], ignore_index=True)

#========================================================================================
#============================= 분야 2 항목 크롤링=========================================
#========================================================================================

# 빈 데이터 프레임 생성
total_df2 = pd.DataFrame()


for i in df['cid'] :
    url = "https://datalab.naver.com/shoppingInsight/getCategory.naver?cid={}".format(i) # get 방식 cid 값이 반복문으로 돌아야 함.

    headers = {
        "Referer": "https://datalab.naver.com/shoppingInsight/sKeyword.naver?keyword=%ED%8A%B8%EC%9C%84%EB%93%9C%EC%9E%90%EC%BC%93&cid=50000000",

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    # 랜덤 시간 적용
    random_sec = random.uniform(1,1.01)
    print(random_sec)
    time.sleep(random_sec)

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    data = json.loads(res.text)  # JSON 문자열을 파이썬 객체로 변환, 파싱해야 딕셔너리 형태가 돼서 'childList' 키에 접근할 수 있음

    df2 = pd.DataFrame(columns=['cid', 'name'])  # 빈 데이터 프레임 생성

    for i in range(0, len(data['childList'])) : # 2분야 카레고리 수 만큼 반복
        cid_value = data['childList'][i]['cid']  # 'childList'의 i 번째 아이템의 'cid' 값을 추출
        name_value = data['childList'][i]['name']  # 'childList'의 i 번째 아이템의 'cid' 값을 추출
        
        df2 = pd.concat([df2, pd.DataFrame({'cid': [cid_value], 'name': [name_value]})], ignore_index=True) # 카테고리 수 만큼 추가

    # 새로운 데이터프레임을 기존 데이터프레임에 추가
    #ignore_index=True 옵션은 기존 인덱스를 무시하고 새로운 인덱스를 생성.
    total_df2 = pd.concat([total_df2, df2], ignore_index=True)  

    total_df2.to_csv('save_240422.csv')