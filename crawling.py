import pandas as pd
import requests

file_path = 'kost_daily_report.csv'
df = pd.read_csv(file_path)

# 'Project' 열을 제외한 나머지 열(날짜별 열)을 선택
date_columns = df.columns[1:]

# 날짜별 열을 합산하여 'Project total' 열 만들기
df['Project total'] = df[date_columns].sum(axis=1)

# 필요한 열만 추출 (프로젝트명, 비용)
df_filtered = df[['Project', 'Project total']]

# 비용을 기준으로 내림차순 정렬 후 상위 100개 추출
top_100_projects = df_filtered.sort_values(by='Project total', ascending=False).head(100)

# 상위 100개 프로젝트명 리스트
top_100_project_names = top_100_projects['Project'].tolist()

# API 요청
url = "https://"
response = requests.get(url)
data = response.json()

# API 응답에서 프로젝트 id와 name을 매핑
project_dict = {item["id"]: item["name"] for item in data}

# 상위 100개 프로젝트와 매칭되는 ID만 추출
filtered_project_dict = {id_: name for id_, name in project_dict.items() if name in top_100_project_names}

# 결과 출력
print(filtered_project_dict)
print(len(list(filtered_project_dict.keys())))