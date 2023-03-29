from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
import json
import time
# import pytest
import pandas as pd
from datetime import datetime
from selenium.webdriver.chrome.options import DesiredCapabilities, Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

_url = "https://www.bustabit.com/game/"


def getResults():
    currPage = 3540414
    lastPage = 3545671 
    chrome_options = Options()
    chrome_options.add_argument(
        "user-data-dir=/Users/mac/Documents/FrontEndBustabit")  # change to profile path
    chrome_options.add_argument('profile-directory=profile1')
    # chrome_options.add_argument("--headless")


    url = _url
    gameId = []
    bustNumber = []
    timeStamp = []
    count = 0
    maxLimit = 50
    while currPage <= lastPage:
        driver = webdriver.Chrome(
            options=chrome_options, executable_path="/Users/mac/Documents/FrontEndBustabit/chromedriver")
        while count < maxLimit and currPage <= lastPage:
            count += 1
            driver.implicitly_wait(10)
            driver.get(url="{}{}".format(url, currPage))

            try:
                el = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@class='col-sm-24 col-xs-24']")))
            except:
                print("err")
                driver.quit()
                break
            # WebDriverWait(driver, 5).until(
            #     lambda s: s.find_element_by_class_name(
            #         "col-sm-24 col-xs-24").click()
            # )
            # time.sleep(4)

            soup = BeautifulSoup(driver.page_source, 'lxml')

            err = soup.find('span', class_='cf-error-type')

            if err:
                print(err)
                break

            try:
                div = soup.find('div', class_='col-sm-24 col-xs-24')
            except:
                time.sleep(3)
                driver.get(url="{}{}".format(url, currPage))
                wait = WebDriverWait(driver, 20)
                time.sleep(4)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                div = soup.find('div', class_='col-sm-24 col-xs-24')

            try:
                gameId.append(str(div.find('h4').get_text()))
            except:
                continue
            # except:
            # gameId.append('NAN')
            try:
                bustNumber.append(div.h5.find(
                    'span', class_='bold').get_text())
            except:
                #     time.sleep(2)
                #     bustNumber.append(div.h5.find(
                #         'span', class_='bold').get_text())
                continue
            # except:
            # bustNumber.append('NAN')
            try:
                timeStamp.append(div.find_all('h5')[1].get_text())
            except:
                #     time.sleep(2)
                #     timeStamp.append(div.find_all('h5')[1].get_text())
                # except:
                # timeStamp.append('NAN')
                continue
            currPage = currPage + 1

        driver.quit()
        count = 0
        saveResult(timeStamp, gameId, bustNumber)
        gameId = []
        bustNumber = []
        timeStamp = []


def saveResult(timeStamp, gameId, bustNumber):
    dataTuples = list(zip(timeStamp, gameId, bustNumber))
    df = pd.DataFrame(dataTuples, columns=[
        'Time Stamp', 'GameID', 'Bust Number'])
    df.to_csv('data-latest.csv', mode='a', header=False)


if __name__ == '__main__':
    getResults()
