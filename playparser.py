from bs4 import BeautifulSoup
import requests
import json
base = "https://play.google.com/store/apps/collection/"
collections = ["topgrossing","topselling_free","topselling_paid","topselling_new_free","topselling_new_paid"]
apps = []
studios = dict()

for collection in collections:
    url = base + collection
    html_doc = requests.get(url)
    play_soup = BeautifulSoup(html_doc.text, 'html5lib')
    print collection,":"
    for rank,app in enumerate(play_soup.select(".snippet-list li")):
        app_pack = app.select('.title')[0]
        app_href = app_pack['href'].encode("ascii","ignore")
        app_name = app_pack.text.encode("ascii","ignore")
        studio_name = app.select('.attribution')[0].text

        app_details_url = "https://play.google.com/"+app_href
        sub_doc = requests.get(app_details_url)
        sub_soup = BeautifulSoup(sub_doc.text, 'html5lib')
        sub_soup.find('dd', itemprop="numDownloads").text

        apps.append((app_name,studio_name))
        print app_name,":::",studio_name
    print

#fh = open("/home/ec2-user/topapps/scrape.json","w+")
#json.dump(apps,fh)
#fh.close()
