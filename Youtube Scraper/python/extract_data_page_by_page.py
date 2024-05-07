### Libraries Included
import time
import numpy as np
import pandas as pd
from tqdm import tqdm

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.read_csv('data.csv')

print(df.head())
browser=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get('https://www.youtube.com')
time.sleep(2)

data = []

for link in tqdm(df['Vedio_link']):
    browser.get(link)
    
    time.sleep(5)
    
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    try:
        title = soup.find_all('yt-formatted-string', class_ = 'style-scope ytd-video-primary-info-renderer')[0].text
    except:
        title = np.nan
    
    try:
        view = soup.find('span' , class_ = 'view-count style-scope ytd-video-view-count-renderer').text
    except:
        view = np.nan
        
    try:
        date_time = soup.find_all('yt-formatted-string', class_ = 'style-scope ytd-video-primary-info-renderer')[1].text
    except:
        date_time = np.nan
    
    try:
        like = soup.find('yt-formatted-string', class_ = 'style-scope ytd-toggle-button-renderer style-text').text
    except:
        like = np.nan
      
    try:
        description = soup.find('yt-formatted-string', class_ = 'content style-scope ytd-video-secondary-info-renderer').text
    except:
        description = np.nan
        
    data.append([title , date_time, like, view, link, description])
len(data)
df = pd.DataFrame(data, columns = ['title' , 'date_time', 'likes', 'views', 'link' , 'description'])
df.isnull().sum()
df.to_csv('GFG.csv', index = False)