# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7

import os
import requests
import re
from bs4 import BeautifulSoup
import sys

# function to get the html source text of the medium article
def get_page():
    global url
    
    url = input("Enter url of a medium article: ")  # Ask the user to input the URL
    
    # handling possible error
    if not re.match(r'https?://medium.com/', url):
        print('Please enter a valid website, or make sure it is a medium article')
        sys.exit(1)

    res = requests.get(url)  # Send request to the Medium URL
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text

# function to collect and extract text from the HTML
def collect_text(soup):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    for para in para_text:
        text += f"{para.text}\n\n"
    return text

# function to save the scraped text into a file
def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1]
    fname = f'scraped_articles/{name}.txt'
    
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f'File saved in directory {fname}')


if __name__ == '__main__':
    text = collect_text(get_page())
    save_file(text)


