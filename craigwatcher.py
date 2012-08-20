from bs4 import BeautifulSoup
import os
import requests
import smtplib
from email.mime.text import MIMEText

url = "http://sfbay.craigslist.org/search/apa/sfc?query=&srchType=A&minAsk=&maxAsk=4000&bedrooms=3&nh=1&nh=3&nh=8&nh=18&nh=25"

html_doc = requests.get(url)
post_soup = BeautifulSoup(html_doc.text, 'html5lib')

old_posts = []
old_postings = '/home/ec2-user/craigslist/old_postings.txt'
with open(old_postings,'r') as old_posts_file:
    old_posts = old_posts_file.readlines()

new_posts = []

for post in post_soup.find_all("p","row"):
    posting_url = post.find("a")["href"].encode('ascii')
    price = post.find("span","itemph").text.encode("ascii")
    title =  post.find("a").text.encode("ascii")
    #new post
    if posting_url+"\n" not in old_posts:
        #insert into text file
        with open(old_postings,'a') as oldies:
            oldies.write(posting_url+"\n")
        new_posts.append((title+": "+price+" || "+posting_url))
        print posting_url
if len(new_posts) > 0:
    msg = MIMEText("\n".join(new_posts)+"\n")
    recipients = ["tossrock@gmail.com","jeffawang@gmail.com","adamrhine@gmail.com"] 
    msg['Subject'] = "New Craigslist postings"
    msg['from']    = "Craigwatcher"
    msg['to']      = ",".join(recipients)
    s = smtplib.SMTP('localhost')
    s.sendmail("Craigwatcher@ec2-23-20-227-25.compute-1.amazonaws.com",recipients,msg.as_string())
    s.quit()
