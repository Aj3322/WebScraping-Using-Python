# Importing necessary libraries
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import requests 
from datetime import datetime

# Starting the ChromeDriver
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Searching on Browser with URL
link = 'https://www.youtube.com/@wscubetech/videos'
browser.get(link)

# Scrolling infinitely so that data can reach the bottom of the page and get all the data 
for i in tqdm(range(0, 500000, 1000)):
    browser.execute_script("window.scrollTo(0," + str(i) + ")")
    time.sleep(1)

# Parsing the response into Soup
soup = BeautifulSoup(browser.page_source, 'html.parser')

# Extracting the data from response
import re
data = []
for sp in tqdm(soup.find_all('ytd-rich-item-renderer')):
    try:
        thumbnail_img = sp.find('img').get('src').split('?')[0]
    except:
        thumbnail_img = sp.find('img').get('src') 
    video_link = "https://www.youtube.com" + sp.find('a').get('href')
    title = sp.find('yt-formatted-string', class_="style-scope ytd-rich-grid-media").text
    time = sp.find('yt-formatted-string').text
    # Extracting views count using regular expression
    string = sp.find('yt-formatted-string', class_="style-scope ytd-rich-grid-media").get('aria-label')
    pattern = r'\b(\d{1,3}(?:,\d{3})*)\b views'
    views_match = re.search(pattern, sp.find('yt-formatted-string', class_="style-scope ytd-rich-grid-media").get('aria-label'))
    if views_match:
        views = int(views_match.group(1).replace(',', ''))
    else:
        print("No views found.")
    data.append([title, thumbnail_img, video_link, views, time])

# Creating DataFrame
df = pd.DataFrame(data, columns=['Title', 'Thumbnail_img', 'Video_link', 'No_Views', 'Duration'])

# Checking for missing values
print(df.isna().sum())

# Saving the data
df.to_csv('data.csv')
