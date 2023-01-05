from requests import get 
#pip install requests
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options) 


def get_page_count(keyword):
    base_url = "https://kr.indeed.com/jobs?q="
    end_url = "&limit=50"
    browser.get(f"{base_url}{keyword}{end_url}")
   
    soup = BeautifulSoup(browser.page_source, "html.parser")
    #봇으로 인식해 차단 당해서 슬립시킴
    time.sleep(5)
    
    pagination = soup.find("nav", class_="ecydgvn0")
    if pagination == None:
        return 1
    pages = pagination.find_all("div", recursive=False)
    count = len(pages)
    if count>= 5:
        return 5
    else:
        return count




def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found",pages,"pages")
    result = []
    for page in range(pages):
        base_url="https://www.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page*10}";
        print("Requesting ",final_url)
        browser.get(final_url)

    soup = BeautifulSoup(browser.page_source,"html.parser")
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all('li',recursive=False)
    for job in jobs:
        zone = job.find("div", class_="mosaic-zone")
        if zone == None:
            anchor = job.select("h2 a")
            title = anchor[0]['aria-label']
            link = anchor[0]['href']
            company = job.find("span", class_="companyName")
            location = job.find("div", class_="companyLocation")
            job_data = {
            'link':f"https://www.indeed.com{link}",
            'company':company.string,
            'location':location.string,
            'position':title
            }
            for a in job_data:
                if job_data[a] != None:
                    job_data[a] = job_data[a].replace(",", " ")

            result.append(job_data)
    return result
