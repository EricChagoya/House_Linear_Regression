
import requests
from bs4 import BeautifulSoup
# This method no longer works for this website.


URL = "https://www.realtor.com/realestateandhomes-search/Dana-Point_CA"

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

saveFile= open("House_data.txt", 'w', encoding = 'utf-8')
for i in soup:
    saveFile.write(str(i))
    
saveFile.close()
