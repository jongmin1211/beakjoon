import requests
from bs4 import BeautifulSoup
import time

# 🔹 백준 아이디 설정
BAEKJOON_ID = "myf6magic05"

# 🔹 Solved.ac API로 사용자 정보 가져오기
user_url = f"https://solved.ac/api/v3/user/show?handle={BAEKJOON_ID}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    user_response = requests.get(user_url, headers=headers)
    user_response.raise_for_status()
    user_data = user_response.json()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch user data from Solved.ac: {e}")
    exit(1)

# 🔹 Solved.ac 프로필 페이지에서 푼 문제 목록 크롤링
solvedac_profile_url = f"https://solved.ac/profile/{BAEKJOON_ID}"
try:
    profile_response = requests.get(solvedac_profile_url, headers=headers)
    profile_response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch Solved.ac profile: {e}")
    exit(1)

soup = BeautifulSoup(profile_response.text, "html.parser")

# 🔹 Solved.ac 프로필 페이지에서 푼 문제 목록 찾기
# 2025년 3월 기준으로 Solved.ac 프로필 페이지에서 푼 문제 목록은
# <div class="css-1k3iieq"> 태그 안에 있는 <a> 태그들로 표시됨
problem_list_div = soup.find("div", {"class": "css-1k3iieq"})
if not problem_list_div:
    print("Could not find problem list div in Solved.ac profile. Check if the HTML structure has changed.")
    exit(1)

problems = problem_list_div.find_all("a") if problem_list_div else []
problem_ids = []

for problem in problems:
    href = problem.get("href")
    if href and "/problem/" in href:
        problem_id = href.split("/")[-1]  # href에서 문제 번호 추출 (예: /problem/1000 -> 1000)
        problem_ids.append(problem_id)

# 🔹 Solved.ac API로 문제 제목 가져오기
problem_list = []
for problem_id in problem_ids:
    lookup_url = f"https://solved.ac/api/v3/problem/lookup?problemIds={problem_id}"
    try:
        lookup_response = requests.get(lookup_url, headers=headers)
        lookup_response.raise_for_status()
        problem_data = lookup_response.json()
        time.sleep(1)  # 요청 간격 추가
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch problem data from Solved.ac: {e}")
        continue

    if problem_data and len(problem_data) > 0:
        problem_info = problem_data[0]
        problem_title = problem_info["titleKo"]  # 한국어 제목
        problem_url = f"https://www.acmicpc.net/problem/{problem_id}"
        problem_list.append((problem_id, problem_title, problem_url))

# 🔹 README 파일 업데이트
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 백준 문제 풀이 기록\n\n")
    f.write(f"## {BAEKJOON_ID}님의 백준 문제 풀이 현황\n\n")
    f.write(f"### 해결한 문제 ({len(problem_list)}개)\n\n")
    for num, title, url in problem_list:
        f.write(f"- [{num}. {title}]({url})\n")
