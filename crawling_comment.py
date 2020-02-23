import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
##크롬 드라이브를 통하여 파싱을 하겠다.
driver = webdriver.Safari()


##뉴스에 댓글이 많이 달린 뉴스들 보여주는 url로 연결
driver.get("https://news.naver.com/main/ranking/popularMemo.nhn")
driver.implicitly_wait(1)
## 첫번째 기사 클릭
driver.find_element_by_xpath("//*[@id='wrap']/table/tbody/tr/td[2]/div/div[3]/ol/li[1]/dl/dt/a").click()
driver.implicitly_wait(1)
try:
    driver.find_element_by_xpath("//*[@id='cbox_module']/div[2]/div[9]/a[1]").click()
except:
    driver.find_element_by_xpath("//*[@id='cbox_module']/div/div/a[1]").click()

while driver.find_element_by_class_name("u_cbox_btn_more"):
    driver.implicitly_wait(1)
    ## 댓글 더 보기 누르기
    try:
        driver.find_element_by_class_name("u_cbox_btn_more").click()
    except:
        break
## 댓글 내용 파싱
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
news_title = soup.find(id='articleTitle')
comments = soup.find_all(class_='u_cbox_contents')
for item in comments:
    print(item.text)

from openpyxl import Workbook

write_wb = Workbook()
# Sheet1에다 입력
write_ws = write_wb.active

# 행 단위로 추가
write_ws.append(["뉴스 제목", "댓글 내용", "타입"])

for item in comments:
    write_ws.append([news_title.text, item.text, 0])
write_wb.save('댓글들.xlsx')
