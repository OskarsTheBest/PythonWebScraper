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
    
    


try:
    topic_descs = []

    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())


except Exception as e:
    print(f"Error: {e}")
    
topic_urls = []
base_url = 'https://github.com'
for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])



topics_dict = {
    'title': topic_titles,
    'description': topic_descs,
    'url': topic_urls
}

topic_df = pd.DataFrame(topics_dict).to_csv('topics.csv',index = None, encoding='utf-8')

topic_page_url = topic_urls[0]

response2 = requests.get(topic_page_url)


page_contents2 = response2.text
page_contents2[:1000]
with open('topics.html', 'w', encoding='utf-8') as f:
    f.write(page_contents2)
        
topic_doc = BeautifulSoup(page_contents2, 'html.parser')


repo_h3_class = 'f3 color-fg-muted text-normal lh-condensed'
repo_tags = topic_doc.find_all('h3', {'class' : repo_h3_class})
a_tags = repo_tags[0].find_all('a')


repo_url = base_url + a_tags[1]['href']


star_span_class = 'Counter js-social-count'
star_tags = topic_doc.find_all('span', { 'class': star_span_class})






def parse_star_count(stars_str):
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    return int(stars_str)

    
    
def get_topic_page(topic_url):
    response2 = requests.get(topic_url)
    if response2.status_code != 200:
        raise Exception('Failed to Load {}'.format(topic_url))
    
    topic_doc = BeautifulSoup(response2.text, 'html.parser')
    return topic_doc




def get_repo_info(repo_tags, star_tag):
    a_tags = repo_tags.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username, repo_name, repo_url, stars

    
    
    
    
def get_topic_repos(topic_doc):

    
    repo_h3_class = 'f3 color-fg-muted text-normal lh-condensed'
    repo_tags = topic_doc.find_all('h3', {'class' : repo_h3_class})
    
    star_span_class = 'Counter js-social-count'
    star_tags = topic_doc.find_all('span', { 'class': star_span_class})
    
    topic_repos_dict = {
    'username': [],
    'repo_name': [],
    'stars': [],
    'repo_url': []
    }
    
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[3])
        topic_repos_dict['repo_url'].append(repo_info[2])
        
    return pd.DataFrame(topic_repos_dict)
    




get_topic_repos(get_topic_page(topic_urls[4])).to_csv('androidtopics.csv',index = None, encoding='utf-8')




def get_topic_titles(doc):
    selected_title_tag = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class' : selected_title_tag})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    
    return topic_titles

def get_topic_descs(doc):
    selected_desc_tag = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class' : selected_desc_tag})
    
    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())
    topic_descs[:5]
    
    return topic_descs

def get_topic_urls(doc):
    topic_link_tags = doc.find_all('a', {'class' : 'no-underline flex-grow-0'})
        
    topic_urls = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])
        
    return topic_urls

def scrape_topics():
    topic_url = 'https://github.com/topics'
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception('Failed to Load {}'.format(topic_url))
    
    topics_dict = {
        'title': get_topic_titles(doc),
        'description': get_topic_descs(doc),
        'url': get_topic_urls(doc)
    }
    
    return pd.DataFrame(topics_dict)
    

