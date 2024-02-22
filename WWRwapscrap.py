# 직업구인 웹사이트에서 회사정보를 가져와 정리
import requests # 웹사이트로부터 데이터 불러오기
from bs4 import BeautifulSoup # 웹사이트 데이터 분석 및 탐색

def scrape_page(url):
    print(f"Scrapping {url}...")
    response = requests.get(url)
    # url의 웹사이트로부터 데이터 불러오기

    soup = BeautifulSoup(response.content, "html.parser")
    # soup은 하나의 class로써 작동
    # 불러온 데이터를 beautifulsoup로 넘김
    # response.content에는 웹사이트 코드가 저장됨
    # "html.parser"은 response.content가 어떤 양식으로 작성됐는지 지정

    jobs = soup.find("section", class_="jobs").find_all("li")[1:-1]
    # soup뒤에 계속 find를 덧붙임으로써 상세한 탐색이 가능
    # find_all를 통해 한개가 아닌 여러 객체를 탐색 가능
    # find_all를 이용해 만든 리스트 내용도 모두 soup class이다
    # list[1:-1]를 통해 처음과 마지막 li를 제외함(관련없는 내용) 

    for job in jobs:
        title = job.find("span", class_="title").text
        company, position, region = job.find_all("span", class_="company")
        url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
        # title, company, position, region은 HTML내의 내용을 불러오지만
        # url은 Anchor("a")내에 있는 속성을 가져오기 때문에 ["href"]를 붙여 사용
        # next_sibling을 통해 다음 요소를 불러옴(첫 anchor는 잘못된 url)

        job_data = {
            "title" : title,
            "company" : company.text,
            "position" : position.text,
            "region" : region.text,
            "url" : f"https://weworkremotely.com{url}"
        }
        all_jobs.append(job_data)

def get_page(url):
    res = requests.get(url)
    so = BeautifulSoup(res.content, "html.parser")
    return len(so.find("div", class_="pagination").find_all("span", class_="page"))
    

all_jobs = []   

url = "https://weworkremotely.com/remote-full-time-jobs?page=1"
# 여러 페이지

pages = get_page(url)
for x in range(pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_page(url)

print(len(all_jobs))