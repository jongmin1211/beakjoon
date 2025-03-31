import requests
from bs4 import BeautifulSoup
import time

# 🔹 백준 아이디 설정
BAEKJOON_ID = "myf6magic05"

# 🔹 백준 프로필 페이지 크롤링
url = f"https://www.acmicpc.net/user/{BAEKJOON_ID}"
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch Baekjoon profile: {e}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")
solved_problems = soup.find("span", {"id": "solved-problem"})
if not solved_problems:
    print("Could not find solved-problem span. Check if the HTML structure has changed.")
    exit(1)

problems = solved_problems.find_all("a") if solved_problems else []
problem_list = []

for problem in problems:
    problem_number = problem.text.strip()
    problem_url = f"https://www.acmicpc.net/problem/{problem_number}"
    
    # 🔹 개별 문제 페이지에서 문제 제목 가져오기
    try:
        problem_page = requests.get(problem_url)
        problem_page.raise_for_status()
        time.sleep(1)  # 요청 간격 추가
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch problem page {problem_url}: {e}")
        continue

    problem_soup = BeautifulSoup(problem_page.text, "html.parser")
    problem_title = problem_soup.find("span", {"id": "problem_title"})
    if problem_title:
        problem_title = problem_title.text.strip()
    else:
        problem_title = "Unknown Title"

    problem_list.append((problem_number, problem_title, problem_url))

# 🔹 README 파일 업데이트
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 백준 문제 풀이 기록\n\n")
    f.write(f"## {BAEKJOON_ID}님의 백준 문제 풀이 현황\n\n")
    f.write(f"### 해결한 문제 ({len(problem_list)}개)\n\n")
    for num, title, url in problem_list:
        f.write(f"- [{num}. {title}]({url})\n")
