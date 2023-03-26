import requests

topics_url = 'https://github.com/topics'
response = requests.get(topics_url)

len(response.text)

page_contents = response.text
page_contents[:1000]
with open('webpage.html', 'w', encoding='utf-8') as f:
    f.write(page_contents)