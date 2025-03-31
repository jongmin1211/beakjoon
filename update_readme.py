import requests
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

# 🔹 사용자가 푼 문제 목록 가져오기
problem_stats_url = f"https://solved.ac/api/v3/user/problem_stats?handle={BAEKJOON_ID}"
try:
    problem_response = requests.get(problem_stats_url, headers=headers)
    problem_response.raise_for_status()
    problem_stats = problem_response.json()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch problem stats from Solved.ac: {e}")
    exit(1)

# 🔹 푼 문제 번호 추출
solved_problems = []
for stat in problem_stats:
    level = stat["level"]
    solved = stat["solved"]
    if solved > 0:
        # Solved.ac API에서 문제 번호를 직접 제공하지 않으므로, 문제 목록을 별도로 가져와야 함
        # 여기서는 문제 번호를 Solved.ac의 문제 검색 API로 가져오거나, 백준 문제 페이지에서 크롤링
        # 문제 번호는 1부터 시작하므로 level에 따라 문제 번호를 추정
        # 더 정확한 방법은 Solved.ac의 문제 목록 API를 사용
        pass

# 🔹 Solved.ac API로 문제 목록 가져오기 (문제 번호와 제목 매핑)
problem_list = []
problem_ids = []

# 🔹 사용자가 푼 문제 목록을 가져오기 위해 Solved.ac의 문제 태그 API 사용
# 문제 번호를 얻기 위해 사용자 푼 문제 API 호출
# Solved.ac API는 직접 문제 번호 목록을 제공하지 않으므로, 백준 크롤링으로 대체하거나 Solved.ac의 다른 API 활용
# 여기서는 백준 크롤링 대신 Solved.ac의 문제 조회 API를 사용
# 문제 번호를 얻기 위해 사용자 프로필 페이지에서 직접 문제 번호를 가져오는 방법으로 변경
# Solved.ac API는 문제 번호를 직접 제공하지 않으므로, 백준 크롤링으로 대체

# 🔹 백준 프로필에서 문제 번호만 가져오기 (최소한의 크롤링)
from bs4 import BeautifulSoup

baekjoon_url = f"https://www.acmicpc.net/user/{BAEKJOON_ID}"
try:
    baekjoon_response = requests.get(baekjoon_url, headers=headers)
    baekjoon_response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch Baekjoon profile: {e}")
    exit(1)

soup = BeautifulSoup(baekjoon_response.text, "html.parser")
solved_problems_span = soup.find("span", {"id": "solved-problem"})
if not solved_problems_span:
    print("Could not find solved-problem span. Check if the HTML structure has changed.")
    exit(1)

problems = solved_problems_span.find_all("a") if solved_problems_span else []

for problem in problems:
    problem_number = problem.text.strip()
    problem_ids.append(problem_number)

# 🔹 Solved.ac API로 문제 제목 가져오기
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
