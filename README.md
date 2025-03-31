import requests
from bs4 import BeautifulSoup

# 🔹 백준 아이디 입력
BAEKJOON_ID = "your_baekjoon_id"

# 🔹 백준 프로필 페이지 크롤링
url = f"https://www.acmicpc.net/user/{BAEKJOON_ID}"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 🔹 해결한 문제 가져오기
solved_problems = soup.find("span", {"id": "solved-problem"})
problems = solved_problems.find_all("a") if solved_problems else []

problem_list = []

for problem in problems:
    problem_number = problem.text.strip()
    problem_url = f"https://www.acmicpc.net/problem/{problem_number}"
    
    # 🔹 개별 문제 페이지에서 문제 제목 가져오기
    problem_page = requests.get(problem_url)
    problem_soup = BeautifulSoup(problem_page.text, "html.parser")
    problem_title = problem_soup.find("span", {"id": "problem_title"}).text.strip()

    problem_list.append((problem_number, problem_title, problem_url))

# 🔹 README 파일 업데이트
with open("README.md", "w") as f:
    f.write(f"# 백준 문제 풀이 기록\n\n")
    f.write(f"## {BAEKJOON_ID}님의 백준 문제 풀이 현황\n\n")
    f.write(f"### 해결한 문제 ({len(problem_list)}개)\n\n")
    for num, title, url in problem_list:
        f.write(f"- [{num}. {title}]({url})\n")
