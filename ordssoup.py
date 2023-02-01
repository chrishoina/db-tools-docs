from bs4 import BeautifulSoup
import requests

url = "https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/22.4/ordig/installing-REST-data-services.html#GUID-B5048C9D-5C8A-4591-AD9B-4B145DE20E1E"

r = requests.get(url)
newhtml = r.text

with open('1-ords-installation-checklist.html', "a") as f: 
    f.write(newhtml)

# print(r.text)
