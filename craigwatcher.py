from bs4 import BeautifulSoup
import requests
import json
url = "http://sfbay.craigslist.org/search/apa/sfc?query=&srchType=A&minAsk=&maxAsk=4000&bedrooms=3&nh=1&nh=3&nh=8&nh=18&nh=25"

html_doc = requests.get(url)
post_soup = BeautifulSoup(html_doc.text, 'html5lib')

with open(old_postings.txt) as oldies:
    old_posts = oldies.read()
    for post in play_soup.find_all("p","row"):
        posting_url = post.find("a")["href"].encode('ascii')
        #new post
        if posting_url not in old_posts:

            #insert into text file

            #email

