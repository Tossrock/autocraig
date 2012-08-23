from bs4 import BeautifulSoup
import os
import requests
import smtplib
from email.mime.text import MIMEText

# Retrieve the entire relevant CL site.
url = 'http://sfbay.craigslist.org/search/apa/sfc?query=&srchType=A&minAsk=1500&maxAsk=4000&bedrooms=3&nh=1&nh=3&nh=8&nh=18&nh=25'
html_doc = requests.get(url)

# Initialize the soup.
post_soup = BeautifulSoup(html_doc.text, 'html5lib')

# Remember the old posts.
old_posts = []
old_postings = '/home/ec2-user/craigslist/old_postings.txt'
with open(old_postings,'r') as old_posts_file:
    old_posts = old_posts_file.readlines()

# Initialize a list for the new posts.
new_posts = []

# Iterate through posts to find novelties.
for post in post_soup.find_all('p','row'):
    # Retrieve the URL for the post.
    posting_url = post.find('a')['href'].encode('ascii','ignore')
    # See if it's new.
    if posting_url+'\n' not in old_posts:
        # It's new!  Gather its data.
        price = post.find('span','itemph').text.encode('ascii','ignore')
        title =  post.find('a').text.encode('ascii','ignore')
        # Remember it for later.
        with open(old_postings,'a') as oldies:
            oldies.write(posting_url+'\n')
        # Format it all pretty-like
        post_content = '{price} <a href="{url}">{title}</a>'.format(price=price, url=posting_url, title=title)
        new_posts.append(post_content)

        # Output for debugging
        print posting_url

# Finished searching.
# Send out the new posts via email.
if len(new_posts) > 0:
    msg = MIMEText('<br />'.join(new_posts), 'html')
    recipients = ['tossrock@gmail.com','jeffawang@gmail.com','adamrhine@gmail.com'] 
    msg['Subject'] = 'New Craigslist postings'
    msg['from']    = 'Craigwatcher'
    msg['to']      = ','.join(recipients)
    s = smtplib.SMTP('localhost')
    s.sendmail('Craigwatcher@ec2-23-20-227-25.compute-1.amazonaws.com',recipients,msg.as_string())
    s.quit()
