from bs4 import BeautifulSoup
import os

# leave the first item blank
eventMission = [['Title', 'Period', 'Detail']]
challengeMission = [['Title', 'Period', 'Detail']]

def displayOption(soup):
    leave = False
    checkEvent_ImportData(soup)

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
                checkEvent(soup, eventMission) #type 0 = event, type 1 = challengeMission
            elif re == str(3):
                checkEvent(soup, challengeMission)
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
def checkEvent(soup, missionList):

    usrInput = 'NotZero'
    page = 1
    max_page = (len(missionList) // 10) + 1

    while usrInput != '0':
        # display page 1 by default
        os.system('cls' if os.name == 'nt' else 'clear')
        checkEvent_DisplayEvent(page, missionList)
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
            numberSet = list(range(len(missionList)))
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
            checkEvent_DisplayEventDetail(int(usrInput), missionList)
            
def checkEvent_ImportData(soup):
    # declare empty mission list
    missionList = None

    for missionType in range(2):
        if missionType == 0:
            temp = soup.find(class_='table2').find_all(class_='quest')
            missionList = eventMission
        elif missionType == 1:
            temp = soup.find(class_='table3').find_all(class_='quest')
            missionList = challengeMission

        # record events to arrays
        counter = 0
        for i in temp[1:]:
            # event no.
            counter += 1
            
            # reserve new space for an event
            missionList.append([])

            # record event title
            missionList[counter].append(i.find(class_='title').text.strip())
            
            # record event period
            if len(i.find(class_='terms').text[4:].strip()) > 25:
                firstPeriod = i.find(class_='terms').text[4:].strip()[:25].strip()
                secondPeriod = i.find(class_='terms').text[4:].strip()[26:].strip()
                missionList[counter].append(firstPeriod + '\n' +secondPeriod)
            
            else:
                missionList[counter].append(i.find(class_='terms').text[4:].strip()[:25])

            # record event detail
            missionList[counter].append(i.find(class_='txt').text.strip())

def checkEvent_DisplayEvent(page, missionList):
    delta = (page - 1) * 10
    print('總共有' + str(len(missionList)-1) + '個活動任務.')

    if 10 + delta > len(missionList):
        print('正顯示第 ' + str( 1 + delta) + ' 至第 ' + str(len(missionList)) + '個活動任務\n')
        for i in range(11 + delta)[ 1 + delta: len(missionList)]:
            print('[' + str(i) + ']\t' + missionList[i][0])

    else:
        print('正顯示第 ' + str( 1 + delta) + ' 至第 ' + str(10 + delta) + '個活動任務\n')
        for i in range(11 + delta)[ 1 + delta:]:
            print('[' + str(i) + ']\t' + missionList[i][0])

def checkEvent_DisplayEventDetail(no, missionList):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('任務名稱:\n' + missionList[no][0] + '\n')
    print('可供遊玩時段:\n' + missionList[no][1] + '\n')
    print('任務詳情:\n' + missionList[no][2] + '\n')
    print('Press Enter to go back')
    input()
