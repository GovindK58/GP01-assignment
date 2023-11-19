import requests
from bs4 import BeautifulSoup as bs
from time import strptime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("username", type=str)
parser.add_argument("password", type=str)
parser.add_argument("TA", type=str) # name of the TA
args = parser.parse_args()

course = "CS 406-2022-2" # Course Code as it appears on moodle, must be a current course

s = requests.Session()

# login into moodle
site = s.get("https://moodle.iitb.ac.in/2022/login/index.php")
bs_content = bs(site.content, "html.parser")
token = bs_content.find("input", {"name":"logintoken"})["value"]
login_data = {"username":args.username,"password":args.password, "logintoken":token}
s.post("https://moodle.iitb.ac.in/2022/login/",login_data)

# finding course page
site = s.get("https://moodle.iitb.ac.in/2022/my/")
bs_content = bs(site.content, "html.parser")
for i in bs_content.find_all("a", class_="list-group-item list-group-item-action"):
    if(i.text.find(course) != -1):
        new_link = i.get('href')

# finding Announcemets tab
site = s.get(new_link)
bs_content = bs(site.content, "html.parser")
for i in bs_content.find_all("a", class_="aalink"):
    if(i.text.find("Announcements") != -1):
        new_link = i.get('href')

# iterating thru the announcements and adding reqd content to annoucemenst dict
site = s.get(new_link)
bs_content = bs(site.content, "html.parser")
announcements = {}
for i, thread in enumerate(bs_content.find("table", class_="table discussion-list").find_all("a")):
    if(i<4): continue
    if(i%5==0): 
        new_link = thread.get('href')
        site = s.get(new_link)
        bs_content = bs(site.content, "html.parser")
        for ann in bs_content.find("article").find_all("header"):
            ta_name = ann.a.text
            timestamp = ann.time.text
            subject = ann.h3.text
            if(ta_name.find(args.TA) != -1):
                announcements[strptime(timestamp, r"%A, %d %B %Y, %I:%M %p")] = (timestamp + "; "+ subject)

file = open("announcements.txt", "a")
for a in sorted(announcements.items()):
    file.write(a[1] + "\n")
file.close()
