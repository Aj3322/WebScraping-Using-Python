import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import json
data = []
dataJson = []
for page in tqdm(range(1,11)):
    link = 'https://quotes.toscrape.com/page/' + str(page)
    res  = requests.get(link)
    soup = bs(res.text, 'html.parser')
    for sp in soup.find_all('div', class_= 'quote'):
        tags = []
        quote = sp.find(class_='text').text[1:-1]
        author = sp.find(class_='author').text
        author_id = sp.find('a').get('href')
        author_link = "https://quotes.toscrape.com"+sp.find('a').get('href')
        for tag in sp.find_all('a', class_= 'tag'):
            tags.append(tag.text)
        tags = ','.join(tags)
        data.append([quote, author, author_id, tags , author_link])
df = pd.DataFrame(data, columns=['Quotes', 'Author_name', 'Author_id', 'Tags' , 'Author_link'])
dataJson.append({"quote":quote, "author":author, "author_id" : author_id, "tags" : tags , "author_link" : author_link} )
# Saving data into json file
df.to_csv('Data.csv')

# Saving data into json file
json_object = json.dumps(dataJson, indent=4)
with open("quotes.json", "w") as outfile:
    outfile.write(json_object)