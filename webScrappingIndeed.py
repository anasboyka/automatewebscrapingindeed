import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
from datetime import timedelta
import subprocess
import time


def gethtmlPage(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/92.0.4515.107 Safari/537.36', 'referer': 'https://www.google.com/'}
    url = f'https://malaysia.indeed.com/jobs?q=flutter&l=Malaysia&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def getPageCount(s):
    jobCountText = s.find('div', {'id': 'searchCountPages'}).text.strip()
    # print(jobCountText)
    match = re.search("(?<=of)(.*)(?=jobs)", jobCountText)
    totalJobs = int(jobCountText[match.start() + 1:match.end()])
    pageCount = totalJobs // 15
    return pageCount * 10


def getData(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    # print(len(divs))
    for item in divs:
        title = item.find('span').text
        if title == 'new':
            spans = item.find_all('span')
            title = spans[1].text.strip()
        company = item.find('span', class_='companyName').text.strip()
        location = item.find('div', class_='companyLocation').text.strip()
        if item.find('span', class_='salary-snippet') is not None:
            salary = item.find('span', class_='salary-snippet').text.strip()
        else:
            salary = ''
        description = item.find('ul').text.strip()

        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'description': description
        }
        jobList.append(job)

        # print(job)
    return


# sitekey = 'eb27f525-f936-43b4-91e2-95a426d4a8bd'
tomorrowdate = datetime.datetime.now().date() + timedelta(days=1)
jobList = []
runOnce = True
# print(getPageCount(gethtmlPage(0)))
while 1:
    currentdate = datetime.datetime.now().date()
    if currentdate == tomorrowdate:
        tomorrowdate = currentdate + timedelta(days=1)
        runOnce = True
    else:
        if runOnce:
            for i in range(0, getPageCount(gethtmlPage(0)), 10):
                s = gethtmlPage(i)
                getData(s)
            df = pd.DataFrame(jobList)
            print(df.head)
            df.to_csv(f'csvfiles/flutterJob{datetime.datetime.now().strftime("%d%m%Y")}.csv')
            runOnce = False

            # push file on github
            # time.sleep(3)
            # subprocess.run(["lxterminal", "-e", "git", "add", "."])
            # time.sleep(1)
            # subprocess.run(["lxterminal", "-e", "git", "add", "."])
            # time.sleep(2)
            # subprocess.run(
            #     ["lxterminal", "-e", "git", "commit", "-m", f"\"upload new file {datetime.datetime.now().date()}\""])
            # time.sleep(2)
            # subprocess.run(["lxterminal", "-e", "git", "push"])
# done
