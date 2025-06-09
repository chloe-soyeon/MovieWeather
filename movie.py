import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    font_path = "C:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

# 1. 영화 데이터 불러오기
movie_df = pd.read_csv('assets/movie_box_office_kr_until_2025_0430.csv', parse_dates=['release_date'])

# 2. 날씨 데이터 병합
weather_files = sorted(glob("assets/seoul*.csv"))
weather_df = pd.concat([pd.read_csv(f) for f in weather_files], ignore_index=True)
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])

# 3. 병합
merged = pd.merge(movie_df, weather_df, left_on='release_date', right_on='datetime', how='left')

# 4. 필요한 컬럼만 추출하고 결측치 제거
df = merged[['title', 'release_date', 'sales_seoul_krw', 'conditions']].dropna()

# 5. 날씨 상태별 서울 수익 평균 계산
grouped = df.groupby('conditions')['sales_seoul_krw'].mean().sort_values(ascending=False)

# 6. 출력
print("날씨 상태별 서울 수익 평균:")
print(grouped)
# 7. 시각화
plt.figure(figsize=(10, 6))
grouped.plot(kind='bar', color='skyblue')
plt.title('날씨 상태별 서울 수익 평균')
plt.ylabel('서울 수익 (원)')
plt.xlabel('날씨 상태')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y')
plt.show()
