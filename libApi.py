# -*- coding: utf-8 -*-
import requests
import time
import re
from lxml import etree

cookieJar = None

class login:
    def __init__(self):
        global cookieJar
        self.username = ''
        self.password = ''
        self.loginUrl = 'http://seat.ujn.edu.cn/login?targetUri=%2F'
        self.header = {
            'Host' : 'seat.ujn.edu.cn',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Accept-Encoding' : 'gzip, deflate',
            'Referer' : 'http://seat.ujn.edu.cn/login?targetUri=%2F',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Connection' : 'keep-alive',
            'Upgrade-Insecure-Requests' : '1'
        }


    def getCookies(self):
        global cookieJar
        self.html = requests.get(self.loginUrl, None, headers = self.header)
        cookieJar = requests.cookies.RequestsCookieJar()
        cookieJar.set('JSESSIONID',self.html.cookies['JSESSIONID'], path='/', domain=self.header['Host'])

    def getCaptcha(self):
        global cookieJar
        url = 'http://' + self.header['Host'] + '/simpleCaptcha/captcha'
        html = requests.get(url, cookies = cookieJar, headers = self.header)
        captcha = open('loginCaptcha.png','wb')
        captcha.write(html.content)
        captcha.close()

    def login(self):#main
        print('---------------------------------------\nconnecting to seat server,please wait\n---------------------------------------')
        self.username = input('please input your username : ')
        self.password = input('please input your password(while inputting your password please check your environment is safety) : ')
        return self.loginCore()

    def loginCore(self):
        self.getCookies()
        self.getCaptcha()
        captcha = input('please input captcha(captcha is in loginCaptcha.png) : ')
        data = {
            'username' : self.username,
            'password' : self.password,
            'captcha' : captcha
        }
        loginUrl = 'http://seat.ujn.edu.cn/auth/signIn'
        print('---------------------------------------\nlogin to seat server,please wait\n---------------------------------------')
        loginHtml = requests.post(loginUrl, data, cookies = cookieJar, headers = self.header)
        reStr = '<title>(.*?)</title>'
        titleName = re.findall(reStr,loginHtml.text,re.S)
        if(titleName[0] == '自选座位 :: 图书馆预约系统'):
            print('login success')
            return loginHtml
        else:
            print('login fail')
            return None

class maa:
    def __init__(self,loginHtml):
        self.loginHtml = loginHtml
        self.dateSet = None
        self.buildingSet = None
        self.roomSet = None
        self.hourSet = None
        self.startSet = None
        self.endSet = None
        self.powerSet = None
        self.windowSet = None
        self.data = None
        self.seatInfoSet = []
        self.allSeatCount = 0
        self.header = {
            'Host': 'seat.ujn.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://seat.ujn.edu.cn/',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'keep-alive'
        }

    def getSeatBaseInfo(self):
        dateStrValue = "//p[@id='options_onDate']/a/@value"
        dateStr = "//p[@id='options_onDate']/a/text()"
        buildingStrValue = "//p[@id='options_building']/a/@value"
        buildingStr = "//p[@id='options_building']/a/text()"
        roomStrValue = "//p[@id='options_room']/a/@value"
        roomStr = "//p[@id='options_room']/a/text()"
        hourStrValue = "//p[@id='options_hour']/a/@value"
        hourStr = "//p[@id='options_hour']/a/text()"
        startStrValue = "//p[@id='options_startMin']/a/@value"
        startStr = "//p[@id='options_startMin']/a/text()"
        endStrValue = "//p[@id='options_endMin']/a/@value"
        endStr = "//p[@id='options_endMin']/a/text()"
        powerStrValue = "//p[@id='options_power']/a/@value"
        powerStr = "//p[@id='options_power']/a/text()"
        windowStrValue = "//p[@id='options_window']/a/@value"
        windowStr = "//p[@id='options_window']/a/text()"
        seatHtml = self.loginHtml.text
        seatDomTree = etree.HTML(seatHtml)
        self.dateSet = list(zip(seatDomTree.xpath(dateStr),seatDomTree.xpath(dateStrValue)))
        self.buildingSet = list(zip(seatDomTree.xpath(buildingStr),seatDomTree.xpath(buildingStrValue)))
        self.roomSet = list(zip(seatDomTree.xpath(roomStr),seatDomTree.xpath(roomStrValue)))
        self.hourSet = list(zip(seatDomTree.xpath(hourStr),seatDomTree.xpath(hourStrValue)))
        self.startSet = list(zip(seatDomTree.xpath(startStr),seatDomTree.xpath(startStrValue)))
        self.endSet = list(zip(seatDomTree.xpath(endStr),seatDomTree.xpath(endStrValue)))
        self.powerSet = list(zip(seatDomTree.xpath(powerStr),seatDomTree.xpath(powerStrValue)))
        self.windowSet = list(zip(seatDomTree.xpath(windowStr),seatDomTree.xpath(windowStrValue)))

    def printSingleSet(self,set):
        for l in set:
            print(l[0] + ' : ' + l[1])

    def selectSeat(self):
        data = []
        print('---------------------------------------\nplease choose a date when you want to maa')
        self.printSingleSet(self.dateSet)#1
        data.append(input('please input a date : '))
        print('---------------------------------------\nplease choose a building where you want to maa')
        self.printSingleSet(self.buildingSet)#2
        data.append(input('please input a building : '))
        print('---------------------------------------\nplease choose a room where you want to maa')
        self.printSingleSet(self.roomSet)#3
        data.append(input('please input a room : '))
        print('---------------------------------------\nplease choose a start time when you want to maa')
        self.printSingleSet(self.startSet)#4
        startTime = input('please input a start time : ')
        data.append(startTime)
        print('---------------------------------------\nplease choose a hour how long you want to maa')
        self.printSingleSet(self.hourSet)#5
        data.append(input('please input a hour : '))
        self.printSingleSet(self.endSet)#6
        print('---------------------------------------\nplease choose a end time when you want to maa')
        data.append(input('please input a end time : '))
        print('---------------------------------------\nplease choose a power status which you want to maa')
        self.printSingleSet(self.powerSet)#7
        data.append(input('please input a power status : '))
        print('---------------------------------------\nplease choose a window status which you want to maa')
        self.printSingleSet(self.windowSet)#8
        data.append(input('please input a window status : '))
        self.data = data

    def getSeatInfo(self):
        print('---------------------------------------\nhandling\n---------------------------------------')
        page = 0
        while(self.getSeatJson(page)):
            page += 1
        print('according to your ask we have found ' + str(self.allSeatCount) + ' seats')

    def getSeatJson(self,page):
        global cookieJar
        postData = {
            'onDate' : self.data[0],
            'building' : self.data[1],
            'room' : self.data[2],
            'hour' : self.data[4],
            'power' : self.data[6],
            'startMin' : self.data[3],
            'endMin' : self.data[5],
            'offset' : page
        }
        url = 'http://seat.ujn.edu.cn/freeBook/ajaxSearch'
        seatInfoHtml = requests.post(url,postData,cookies = cookieJar,headers = self.header)
        json = seatInfoHtml.json()
        if(json['seatNum'] == 0):
            return False
        jsonStr = json['seatStr']
        statusStr = 'id=\"seat_(.*?)\" title=\"(.*?)\"'
        seatLocStr = '<dd>(.*?)</dd>'
        seatNumStr = '<dt>(.*?)</dt>'
        statusSet = re.findall(statusStr,jsonStr,re.S)
        seatLocSet = re.findall(seatLocStr,jsonStr,re.S)
        seatNumSet = re.findall(seatNumStr,jsonStr,re.S)
        mark = 0
        for i in statusSet:
            if statusSet[mark][1] == '座位空闲':
                self.allSeatCount += 1
                set = []
                set.append(seatLocSet[mark])
                set.append(seatNumSet[mark])
                set.append(statusSet[mark][0])
                set.append(statusSet[mark][1])
                self.seatInfoSet.append(tuple(set))
                mark += 1
            time.sleep(0.5)
        return True

    def showAllAvaibleSeat(self):
        for item in self.seatInfoSet:
            print(item)

    def getCaptcha(self):
        global cookieJar
        url = 'http://' + self.header['Host'] + '/simpleCaptcha/captcha'
        html = requests.get(url, cookies = cookieJar, headers = self.header)
        captcha = open('bookCaptcha.png','wb')
        captcha.write(html.content)
        captcha.close()

    def getStartTime(self,seatId):
        global cookieJar
        header = {
            'Host' : 'seat.ujn.edu.cn',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Accept' : '*/*',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Accept-Encoding' : 'gzip, deflate',
            'Referer' : 'http://seat.ujn.edu.cn/',
            'Content-Type' : 'application/x-www-form-urlencoded;',
            'X-Requested-With' : 'XMLHttpRequest',
            'Connection' : 'keep-alive',
            'charset' : 'UTF-8',
            'Upgrade-Insecure-Requests' : '1'
        }
        url = 'http://seat.ujn.edu.cn/freeBook/ajaxGetTime'
        postData = {
            'id' : seatId,
            'date' : self.data[0]
        }
        startTimeHtml = requests.post(url, postData ,cookies = cookieJar,headers = header)
        reStr = '<li><a href="#" time="(.*?)">'
        startTimeSet = re.findall(reStr,startTimeHtml.text,re.S)
        return startTimeSet

    def getEndTime(self,seatId,startTime):
        global cookieJar
        header = {
            'Host' : 'seat.ujn.edu.cn',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Accept' : '*/*',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Accept-Encoding' : 'gzip, deflate',
            'Referer' : 'http://seat.ujn.edu.cn/',
            'Content-Type' : 'application/x-www-form-urlencoded;',
            'X-Requested-With' : 'XMLHttpRequest',
            'Connection' : 'keep-alive'
        }
        url = 'http://seat.ujn.edu.cn/freeBook/ajaxGetEndTime'
        postData={
            'seat' : seatId,
            'start' : startTime,
            'date' : self.data[0]
        }
        endTimeHtml = requests.post(url,postData,cookies = cookieJar,headers = header)
        reStr = '<li><a href="#" time="(.*?)">'
        endTimeSet = re.findall(reStr,endTimeHtml.text,re.S)
        return endTimeSet

    def maaCore(self,seatId,startTime,endTime):
        self.getCaptcha()
        captcha = input('please input captcha(captcha is in loginCaptcha.png) : ')
        global cookieJar
        url = 'http://seat.ujn.edu.cn/selfRes'
        postData = {
            'date' : self.data[0],
            'seat' : seatId,
            'start' : startTime,
            'end' : endTime,
            'captcha' : captcha
        }
        maaHtml = requests.post(url,postData,cookies = cookieJar,headers = self.header)
        failStr = '<div class="layoutSeat"><dl><dd>(.*?)</dd>'
        result = re.findall(failStr,maaHtml.text,re.S)
        if result == []:
            successStr = '<dt>系统已经为您预定好了<span style="color:red">座位</span></dt>'
            result = re.findall(successStr,maaHtml.text,re.S)
            if result != []:
                if result[0] == '<dt>系统已经为您预定好了<span style="color:red">座位</span></dt>':
                    return True
            else:
                return False
        return False

    def maa(self):#main
        seatId = input('please input seat id : ')
        startSet = self.getStartTime(seatId)
        for st in startSet:
            if self.data[3] <= st <= self.data[5]:
                endSet = self.getEndTime(seatId,st)
                et = int(st) + int(self.data[4]) * 60
                if not str(et) in endSet:
                    et = endSet[-1]
                mark = self.maaCore(seatId,st,str(et))
                if mark:
                    print('---------------------------------------\nmaa success\n---------------------------------------')
                    return
                else:
                    continue
        print('---------------------------------------\nmaa fail\n---------------------------------------')