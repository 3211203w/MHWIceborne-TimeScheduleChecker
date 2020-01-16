import requests
from bs4 import BeautifulSoup
from supp import *

# For PS4 only
response = requests.get('http://game.capcom.com/world/hk/schedule-master.html')
if response.status_code != 200:
    print('Internet connection failure.')
    print('...Press Enter to leave...', end = '')
    input()
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
displayOption(soup)