from bs4 import BeautifulSoup
import requests
import pandas as pd
import unicodedata

topics_url = 'https://github.com/topics'
response = requests.get(topics_url)
len(response.text)
page_contents = response.text
page_contents[:1000]
with open('webpage.html', 'w', encoding='utf-8') as f:
    f.write(page_contents)
        
doc = BeautifulSoup(page_contents, 'html.parser')

selected_title_tag = 'f3 lh-condensed mb-0 mt-1 Link--primary'
selected_desc_tag = 'f5 color-fg-muted mb-0 mt-1'

topic_title_tags =doc.find_all('p', {'class' : selected_title_tag})

topic_desc_tags = doc.find_all('p', {'class' : selected_desc_tag})

topic_link_tags = doc.find_all('a', {'class' : 'no-underline flex-grow-0'})



topic0_url = "https://github.com" + topic_link_tags[0]['href']

topic_titles = []

for tag in topic_title_tags:
    topic_titles.append(tag.text)
    
    
print(topic_titles)

try:
    topic_descs = []

    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())

    print(topic_descs)
except Exception as e:
    print(f"Error: {e}")
    
topic_urls = []
base_url = 'https://github.com'
for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])

print(topic_urls)

topics_dict = {
    'title': topic_titles,
    'description': topic_descs,
    'url': topic_urls
}

topic_df = pd.DataFrame(topics_dict).to_csv('topics.csv',index = None, encoding='utf-8')

topic_page_url = topic_urls[0]

response2 = requests.get(topic_page_url)

print(len(response2.text))


page_contents2 = response2.text
page_contents2[:1000]
with open('topics.html', 'w', encoding='utf-8') as f:
    f.write(page_contents2)
        
topic_doc = BeautifulSoup(page_contents2, 'html.parser')


repo_h3_class = 'f3 color-fg-muted text-normal lh-condensed'
repo_tags = topic_doc.find_all('h3', {'class' : repo_h3_class})
print(len(repo_tags))
