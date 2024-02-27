import requests
from bs4 import BeautifulSoup

# https://remoteok.com/remote-{lang}-jobs
# infinity scroll이라는 div가 있어 모든 정보가 불러와지지가 않음
# 임시로 불러와지는 만큼만 표시

langs = ["python", "golang", "java"]

def scrap_page(url):
    res = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(res.content, "html.parser")

    all_jobs = []

    jobs = soup.find_all("tr", class_="job")
    for job in jobs:
        title = job.find("td", class_="company").find("h2").text.strip()
        company = job.find("h3", itemprop="name").text.strip()
        locations = job.find_all("div", class_="location")
        location=[]
        pay = ""
        for l in locations:
            if l.text.startswith("💰"):
                pay = l.text.strip()
            else:
                location.append(l.text.strip())

        info = {
            "title" : title,
            "company" : company,
            "location" : location,
            "pay" : pay
        }

        all_jobs.append(info)
    for info in all_jobs:
        show_info(info)

def show_info(info):
    print(f"{info["title"]} --- {info["company"]} --- {info["location"]} --- {info["pay"]}")

for lang in langs:
    print(f"================={lang}====================")
    scrap_page(f"https://remoteok.com/remote-{lang}-jobs")