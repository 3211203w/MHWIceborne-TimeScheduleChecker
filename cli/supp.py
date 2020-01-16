import requests
from bs4 import BeautifulSoup
import os

def displayOption(soup):
    leave = False

    while not leave:
        os.system('cls')
        print('歡迎使用 MHWI任務時間表查看器.')
        print('請選擇服務:\n')
        print('[1]  查看可遊玩的多人副本戰役')
        print('[2]  查看可遊玩的活動任務')
        print('[3]  查看可遊玩的鬥技場任務')
        print('[4]  離開\n')
        valid = False
        while not valid:
            print('選擇: ', end = '')
            re = input()
            valid = True
            re = int(re)
            if re == 1:
                checkRaid(soup)
            elif re == 2:
                checkEvent(soup)
            elif re == 3:
                checkChallenge(soup)
            elif re == 4:
                leave = True
                print('Press Enter to say Goodbye.')
                input()
                exit()
            else:
                print('Input error.')
                print('Please try again.')
                valid = False
    

# check if Raid is playable
def checkRaid(soup):
    os.system('cls')

    if soup.find(id='schedule').find(class_='tableTitle type1').string == '緊急任務【冥燈龍的成年體】':
        print('可以遊玩 緊急任務【冥燈龍的成年體】')

        # check the period that the Raid is playable
        temp = soup.find(class_='table1').find_all(class_='term') # three terms shown on the official website
        playable_period = [] # prepared list for multiple term
        count = 0

        for i in temp:
            if '可承接' in i.text:
                playable_period.append(count)
            count += 1

        print('可供遊玩時段:')
        for i in playable_period:
            print(temp[i].find('span').text + '\n')

    else:
        print('沒有可以遊玩的多人副本戰役')

    print("Press Enter to go back.", end = '')
    input()

# check playable event mission
def checkEvent(soup):
    return
# check playable challenging mission
def checkChallenge(soup):
    return