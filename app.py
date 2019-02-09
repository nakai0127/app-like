#coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import urllib.parse
import time
import datetime
import pandas as pd

#Webdriver
browser = webdriver.Chrome(executable_path='~/environment/chromedriver') #ここには任意のWebdriverを入れる
basename = datetime.date.today().strftime('%Y%m%d')
print(basename)
#URL
loginURL = "https://www.instagram.com/" #ログインする際のページ
tagSearchURL = "https://www.instagram.com/explore/tags/{}/?hl=ja" #.format()で{}の中の値を入れられるようになっている
titleSearchURL = 'https://www.instagram.com/{}/?hl=ja'

#TagSearch
tagNames = ['ありがとう','笑った','激辛', 'インドカレー', 'スパイシー', 'ラーメンインスタグラマー']
#tagNames = ['ありがとう','笑った']
namelist = []
info = []
#selectors
#ここには各ページのSelectorを選ぶ。x-pathもしくはcss selector
loginPath = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a' #xpath @https://www.instagram.com/
usernamePath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div/div[1]/input'
passwordPath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/div[1]/input'
notNowPath = '//*[@id="react-root"]/div/div[2]/a[2]'
#mediaSelector = '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]'
#mediaSelector = '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]'
#//*[@id="react-root"]/section/main/article/div[2]/div/div[7]/div[1]/a/div
mediaSelector = '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]'
personalmedia = 'div.eLAPa'
likeSelector = "span.fr66n"
#likeXpathbyPerson = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]'
likeXpathbyPerson1 = '//*[@id="react-root"]/section/main/div/div[3]/article/div/div/div[1]/div[1]/a'
likeXpathbyPerson2 = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a'
nameSelector = 'a.FPmhX'
nextPagerSelector = '/html/body/div[2]/div[1]/div/div/a[2]' #次へボタン
closePagerSelector = 'button.ckWGn'
#title = '/html/body/div[2]/div/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a'
title = '/html/body/div[2]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a'
#USER INFO
username = "nakai0127"
password = "spice@oraka9"

#list
#mediaList = []

allLike = 0

if __name__ == '__main__':

   #Login
   browser.get(loginURL)
   time.sleep(3)
   browser.find_element_by_xpath(loginPath).click()
   time.sleep(3)
   usernameField = browser.find_element_by_xpath(usernamePath)
   usernameField.send_keys(username)
   passwordField = browser.find_element_by_xpath(passwordPath)
   passwordField.send_keys(password)
   passwordField.send_keys(Keys.RETURN)

   for tagName in tagNames:
       likedCounter = 0
       namecount = 0
       print(tagName)
       #Finished logging in. now at
       time.sleep(3)
       encodedTag = urllib.parse.quote(tagName) #普通にURLに日本語は入れられないので、エンコードする
       encodedURL = tagSearchURL.format(encodedTag)
       #print("encodedURL:{}".format(encodedURL))
       browser.get(encodedURL)

       #Finished tag search. now at https://www.instagram.com/explore/tags/%E8%AA%AD%E5%A3%B2%E3%83%A9%E3%83%B3%E3%83%89/?hl=ja
       time.sleep(3)
       browser.implicitly_wait(10)

       #写真を取得してクリックする
       browser.find_element_by_xpath(mediaSelector).click()

       #for media in mediaList:
#           media.click()

       while(namecount <= 30):
           time.sleep(1)
           #if browser.find_element_by_xpath(title) == True:
           try:
               namelist.append(browser.find_element_by_xpath(title).get_attribute('title'))
               namecount += 1
               browser.find_element_by_xpath(nextPagerSelector).click()
           except NoSuchElementException:
               browser.find_element_by_xpath(nextPagerSelector).click()
            #   break
#           browser.implicitly_wait(10)

for name in namelist:
    titleName = titleSearchURL.format(name)
    browser.get(titleName)
    time.sleep(1)
    #id =  browser.find_element_by_css_selector('h1').text
    #print(id)
    info.append(browser.find_element_by_css_selector('ul').text)
    #print(info)
    try:
        time.sleep(1)
        browser.find_element_by_css_selector(personalmedia).click()
        likedCounter = 0
        while(likedCounter <= 2):
            try:
                time.sleep(1)
                browser.find_element_by_css_selector(likeSelector).click()
                likedCounter += 1
                allLike += 1
                print(allLike)
                browser.find_element_by_css_selector(nextPagerSelector).click()
            except NoSuchElementException:
                break
    except NoSuchElementException:
        continue
#df = pd.Series(namelist)
#df.tocsv(basename+'.csv')
#print(namelist)
#print(info)
df1 = pd.Series(namelist)
df2 = pd.Series(info)
df2 = df2.str.split('\n')
df2.columns = ['post','follower','follow']
#df2.to_csv('info.csv', encoding='utf_8_sig')
df = pd.concat([df1,df2], axis=1)

df.to_csv(basename+'.csv', encoding='utf_8_sig')
