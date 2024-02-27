from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import csv
from file import save_to_file

def scrape_jobs(lang):
    pw = sync_playwright().start()

    browser = pw.chromium.launch()

    page = browser.new_page()

    page.goto(f"https://www.wanted.co.kr/search?query={lang}&tab=position")
    time.sleep(1)

    for x in range(10):
        page.keyboard.down("End")
        time.sleep(1)

    content = page.content()

    pw.stop()

    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_="JobCard_container__FqChn")

    jobs_db = []

    for job in jobs:
        link = f"https://www.wanted.co.kr/{job.find("a")["href"]}"
        title = job.find("a")["data-position-name"]
        company = job.find("a")["data-company-name"]
        job = {
            "title" : title,
            "company" : company,
            "lang" : lang,
            "link" : link
        }
        jobs_db.append(job)

    print(jobs_db)
    print(len(jobs_db))

    save_to_file(lang, jobs_db)

langs = ["python", "flutter", "java", "kotlin"]

for lang in langs:
     scrape_jobs(lang)