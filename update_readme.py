import requests
import time

# 백준 아이디 설정
BAEKJOON_ID = "myf6magic05"

# 공통 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 1. Solved.ac API로 사용자 정보 확인
user_url = f"https://solved.ac/api/v3/user/show?handle={BAEKJOON_ID}"
try:
    user_response = requests.get(user_url, headers=headers)
    user_response.raise_for_status()
    user_data = user_response.json()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch user data from Solved.ac: {e}")
    user_data = {"solvedCount": 0}  # 실패 시 기본값

# 2. 백준 프로필 페이지에서 푼 문제 번호 가져오기 (최소 크롤링)
problem_ids = []
baekjoon_url = f"https://www.acmicpc.net/user/{BAEKJOON_ID}"
try:
    baekjoon_response = requests.get(baekjoon_url, headers=headers)
    baekjoon_response.raise_for_status()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(baekjoon_response.text, "html.parser")
    # 백준 프로필 페이지에서 문제 번호 목록 찾기
    # 2025년 3월 기준, "problem-list" 클래스를 가진 div에서 문제 번호를 찾음
    problem_list_div = soup.find("div", class_="problem-list")
    if problem_list_div:
        problems = problem_list_div.find_all("a")
        for problem in problems:
            problem_id = problem.text.strip()
            if problem_id.isdigit():  # 숫자인지 확인
                problem_ids.append(problem_id)
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch Baekjoon profile: {e}")

# 3. Solved.ac API로 문제 제목 가져오기
problem_list = []
for problem_id in problem_ids:
    lookup_url = f"https://solved.ac/api/v3/problem/lookup?problemIds={problem_id}"
    try:
        lookup_response = requests.get(lookup_url, headers=headers)
        lookup_response.raise_for_status()
        problem_data = lookup_response.json()
        time.sleep(0.5)  # 요청 간격 추가
        if problem_data and len(problem_data) > 0:
            problem_info = problem_data[0]
            problem_title = problem_info.get("titleKo", "Unknown Title")
            problem_url = f"https://www.acmicpc.net/problem/{problem_id}"
            problem_list.append((problem_id, problem_title, problem_url))
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch problem {problem_id} from Solved.ac: {e}")

# 4. README 파일 업데이트
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 백준 문제 풀이 기록\n\n")
    f.write(f"## {BAEKJOON_ID}님의 백준 문제 풀이 현황\n\n")
    f.write(f"### 해결한 문제 ({len(problem_list)}개)\n")
    if problem_list:
        for num, title, url in problem_list:
            f.write(f"- [{num}. {title}]({url})\n")
    else:
        f.write("아직 해결한 문제가 없습니다.\n")
