import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("code", type=str, help="course code, eg: CS228")
args = parser.parse_args()

code = args.code

r = requests.get('https://www.cse.iitb.ac.in/academics/courses.php')
soup = BeautifulSoup(r.content, 'html5lib')
s = soup.findAll('table')

result = []
for i in s:
    if(i.text.find(code) != -1):
        # print(i, "\n******************\n")
        univ = i.find('th').text[13:]
        for j in i.findAll('tr'):
            if(j.text.find(code) != -1):
                # print(j.findAll('td'), "\n-------------\n")
                new_code = j.find('td').text.strip()
                if(j.findAll('td')[1].text.find(code) != -1):
                    result.append(univ + ':' + new_code + ';')

# print(result)
if(len(result) == 0 or len(code) != 5 or code[:2] != "CS"):
    print("NOT FOUND")
else:
    result.sort()
    result[-1] = result[-1][:-1]
    print("".join(result))
