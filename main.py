from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

topics_url = 'https://github.com/topics'


response = requests.get(topics_url)
page_contents = response.text        
doc = BeautifulSoup(page_contents, 'html.parser')

selected_title_tag = 'f3 lh-condensed mb-0 mt-1 Link--primary'
selected_desc_tag = 'f5 color-fg-muted mb-0 mt-1'

topic_title_tags =doc.find_all('p', {'class' : selected_title_tag})
topic_desc_tags = doc.find_all('p', {'class' : selected_desc_tag})
topic_link_tags = doc.find_all('a', {'class' : 'no-underline flex-grow-0'})


topic0_url = "https://github.com" + topic_link_tags[0]['href']

topic_urls = []
base_url = 'https://github.com'
for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])
topic_page_url = topic_urls[0]


response2 = requests.get(topic_page_url)
page_contents2 = response2.text 
topic_doc = BeautifulSoup(page_contents2, 'html.parser')




    
    
def get_topic_page(topic_url):
    response2 = requests.get(topic_url)
    if response2.status_code != 200:
        raise Exception('Failed to Load {}'.format(topic_url))
    
    topic_doc = BeautifulSoup(response2.text, 'html.parser')
    return topic_doc



def parse_star_count(stars_str):
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    return int(stars_str)



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
    






def scrape_topic(topic_url, path):
    if os.path.exists(path):
        print("The file {} already Exists. Skipped".format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path, index=None, encoding='utf-8')




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

def scrape_topics(page_num):
    topic_url = 'https://github.com/topics?page={}'.format(page_num)
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception('Failed to Load {}'.format(topic_url))
    
    page_contents = response.text        
    doc = BeautifulSoup(page_contents, 'html.parser')
    
    selected_title_tag = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class' : selected_title_tag})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    
    selected_desc_tag = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class' : selected_desc_tag})
    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())
    
    topic_link_tags = doc.find_all('a', {'class' : 'no-underline flex-grow-0'})
    topic_urls = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])
        
    topics_dict = {
        'title': topic_titles,
        'description': topic_descs,
        'url': topic_urls
    }
    
    return pd.DataFrame(topics_dict)

def scrape_topics_repos():
    print("Scraping a list of the Topics in GitHub")
    all_topics_df = pd.DataFrame()
    
    for page_num in range(1, 7):
        topics_df = scrape_topics(page_num)
        all_topics_df = pd.concat([all_topics_df, topics_df], ignore_index=True)
        
    os.makedirs('csv_files', exist_ok=True)
    
    for index, row in all_topics_df.iterrows():
        print("Top Repositories are getting scraped for {}".format(row['title']))
        scrape_topic(row['url'], 'csv_files/{}.csv'.format(row['title']))

scrape_topics_repos()