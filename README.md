Github Topic Web Scraper

This is a Python script that scrapes Github topic pages and retrieves information about the top repositories for each topic, such as the repository name, URL, number of stars, and the username of the repository owner.
Libraries used

The following libraries are used in this script:

    BeautifulSoup: for parsing HTML and XML documents.
    requests: for sending HTTP requests and receiving responses.
    pandas: for creating and manipulating dataframes.
    os: for file path and directory handling.

How to use

    1.Clone this repository to your local machine.
    2.Open a terminal and navigate to the cloned directory.
    3.Run the following command to install the required packages:

        pip install -r requirements.txt

 Run the following command to execute the script:

        python main.py

    The script will retrieve information about the top repositories for each topic and store it in CSV files in the data folder.

Functions in the script

    get_topic_page(topic_url): retrieves the HTML contents of the given topic URL.
    parse_star_count(stars_str): converts the star count string to an integer.
    get_repo_info(repo_tags, star_tag): retrieves the username, repository name, URL, and star count for a given repository.
    get_topic_repos(topic_doc): retrieves information about the top repositories for a given topic page.
    scrape_topic(topic_url, path): scrapes the top repositories for a given topic and saves the results to a CSV file.
    get_topic_titles(doc): retrieves the titles of the topics on a page.
    get_topic_descs(doc): retrieves the descriptions of the topics on a page.
    get_topic_urls(doc): retrieves the URLs of the topics on a page.
    scrape_topics(page_num): scrapes the top repositories for all topics on a given page and saves the results to CSV files in the data folder.
