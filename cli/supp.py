from bs4 import BeautifulSoup
import os

# leave the first item blank
eventTitle = ['']
eventPeriod = ['']
eventDetail = ['']

def displayOption(soup):
    leave = False

    while not leave:
        os.system('cls' if os.name == 'nt' else 'clear')
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
            if re == str(1):
                checkRaid(soup)
            elif re == str(2):
                checkEvent(soup)
            elif re == str(3):
                checkChallenge(soup)
            elif re == str(4):
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
    os.system('cls' if os.name == 'nt' else 'clear')

    if soup.find(id='schedule').find(class_='tableTitle type1').string == '緊急任務【冥燈龍的成年體】':
        print('可以遊玩 緊急任務【冥燈龍的成年體】\n')

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

    print('Press Enter to go back.', end = '')
    input()

# check playable event mission
def checkEvent(soup):
    checkEvent_ImportData(soup)

    usrInput = 'NotZero'
    page = 1
    max_page = (len(eventTitle) // 10) + 1

    while usrInput != '0':
        # display page 1 by default
        os.system('cls' if os.name == 'nt' else 'clear')
        checkEvent_DisplayEvent(page)
        valid = False

        if page != 1:
            print('[,]\tLast page')
        if page != max_page:
            print('[.]\tNext page')
        print('[0]\tBack to home screen.\n')
        
        while not valid:
            valid = True
            print('選擇:', end='')
            usrInput = input()

            # option list
            numberSet = list(range(len(eventTitle)))
            for i in range(len(numberSet)):
                numberSet[i] = str(numberSet[i])
            
            # validate usrInput
            if not (usrInput in numberSet) and usrInput != ',' and usrInput != '.':
                valid = False
            
            if page == 1 and usrInput == ',':
                valid = False

            if page == max_page and usrInput == '.':
                valid = False
            
            if not valid:
                print('Input error.')
                print('Please try again.')
        
        if usrInput == ',':
            page -= 1
            continue
        
        elif usrInput == '.':
            page += 1
            continue

        elif usrInput == '0':
            break

        else:
            checkEvent_DisplayEventDetail(int(usrInput))
            
def checkEvent_ImportData(soup):
    temp = soup.find(class_='table2').find_all(class_='quest')

    # record events to arrays
    counter = 0
    for i in temp[1:]:
        # event no.
        counter += 1
        
        # record event title
        eventTitle.append(i.find(class_='title').text.strip())
        
        # record event period
        if len(i.find(class_='terms').text[4:].strip()) > 25:
            firstPeriod = i.find(class_='terms').text[4:].strip()[:25].strip()
            secondPeriod = i.find(class_='terms').text[4:].strip()[26:].strip()
            eventPeriod.append(firstPeriod + '\n' +secondPeriod)
        
        else:
            eventPeriod.append(i.find(class_='terms').text[4:].strip()[:25])

        # record event detail
        eventDetail.append(i.find(class_='txt').text.strip())

def checkEvent_DisplayEvent(page):
    delta = (page - 1) * 10
    print('總共有' + str(len(eventTitle)-1) + '個活動任務.')

    if 10 + delta > len(eventTitle):
        print('正顯示第 ' + str( 1 + delta) + ' 至第 ' + str(len(eventTitle)) + '個活動任務\n')
        for i in range(11 + delta)[ 1 + delta: len(eventTitle)]:
            print('[' + str(i) + ']\t' + eventTitle[i])

    else:
        print('正顯示第 ' + str( 1 + delta) + ' 至第 ' + str(10 + delta) + '個活動任務\n')
        for i in range(11 + delta)[ 1 + delta:]:
            print('[' + str(i) + ']\t' + eventTitle[i])

def checkEvent_DisplayEventDetail(no):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('任務名稱:\n' + eventTitle[no] + '\n')
    print('可供遊玩時段:\n' + eventPeriod[no] + '\n')
    print('任務詳情:\n' + eventDetail[no] + '\n')
    print('Press Enter to go back')
    input()

# check playable challenging mission
def checkChallenge(soup):
    return