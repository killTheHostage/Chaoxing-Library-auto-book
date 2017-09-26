import libApi
import re
import datetime
import random

class autoProcess():
    def __init__(self):
        self.userConfigTxt = open('config.txt','r').read()
        self.userConfigTxt = self.userConfigTxt.replace('\n','')
        self.unpw = []
        self.seatInfo = []
        self.processInfo = []
        self.autoSelect = ''
        self.seatId = ''
        self.processType = ''

    def checkConfig(self):
        markStr = 'mask:(.*?);'
        mask = re.findall(markStr,self.userConfigTxt)
        if mask != []:
            if mask[0] == '1':
                return True
            else:
                return False
        else:
            return False

    def appendSetToSet(self,setW,setN):
        if setN != []:
            setW.append(setN[0])
        else:
            setW.append([])

    def getLoginInfo(self):
        unStr = 'username:(.*?);'
        un = re.findall(unStr,self.userConfigTxt)
        pwStr = 'password:(.*?);'
        pw = re.findall(pwStr,self.userConfigTxt)
        unpw = []
        unpw.append(un[0])
        unpw.append(pw[0])
        if unpw != []:
            if not [] in unpw:
                self.unpw = unpw
                return True
            else:
                return False
        else:
            return False

    def getSeatInfo(self):
        dateStr = 'date:(.*?);'
        buildingStr = 'building:(.*?);'
        roomStr = 'room:(.*?);'
        stStr = 'startTime:(.*?);'
        etStr = 'endTime:(.*?);'
        hourSrt = 'hour:(.*?);'
        powerSrt = 'power:(.*?);'
        winodwStr = 'winodw:(.*?);'
        date = re.findall(dateStr,self.userConfigTxt)
        building = re.findall(buildingStr,self.userConfigTxt)
        room = re.findall(roomStr,self.userConfigTxt)
        st = re.findall(stStr,self.userConfigTxt)
        et = re.findall(etStr,self.userConfigTxt)
        hour = re.findall(hourSrt,self.userConfigTxt)
        power = re.findall(powerSrt,self.userConfigTxt)
        window = re.findall(winodwStr,self.userConfigTxt)
        if date != []:
            if date[0] == 'today':
                date[0] = datetime.date.today()
            elif date[0] == 'tomorrow':
                date[0] = datetime.date.today() + datetime.timedelta(days=1)
        seatInfo = []
        self.appendSetToSet(seatInfo,date)
        self.appendSetToSet(seatInfo,building)
        self.appendSetToSet(seatInfo,room)
        self.appendSetToSet(seatInfo,st)
        self.appendSetToSet(seatInfo,hour)
        self.appendSetToSet(seatInfo,et)
        self.appendSetToSet(seatInfo,power)
        self.appendSetToSet(seatInfo,window)
        if seatInfo != []:
            if not [] in seatInfo:
                self.seatInfo = seatInfo
                return True
            else:
                return False
        else:
            return False

    def getAutoSelect(self):
        unStr = 'autoSelect:(.*?);'
        un = re.findall(unStr,self.userConfigTxt)
        if un != []:
            if un[0] != 'null':
                self.autoSelect = un[0]
                return True
            else:
                return False
        else:
            return False

    def getSeatId(self):
        seatIdStr = 'seatId:(.*?);'
        seatId = re.findall(seatIdStr,self.userConfigTxt)
        if seatId != []:
            if seatId[0] != 'null':
                self.seatId = seatId[0]
                return True
            else:
                return False
        else:
            return False

    def getProcessType(self):
        ptStr = 'processType:(.*?);'
        pt = re.findall(ptStr,self.userConfigTxt)
        if pt != []:
            self.processType = pt[0]
        else:
            self.processType = 'normal'

    def mainControl(self):
        self.getProcessType()
        if self.processType == 'bookA':
            print('---------------------------------------\nnow work on bookA model\n---------------------------------------')
            self.bookAP()
        elif self.processType == 'bookB':
            print('---------------------------------------\nnow work on bookB model\n---------------------------------------')
            self.bookBP()
        elif self.processType == 'autoBook':
            print('---------------------------------------\nnow work on autoBook model\n---------------------------------------')
            self.autoSelectP()
        elif self.processType == 'lock':
            print('---------------------------------------\nnow work on lock model\n---------------------------------------')
        elif self.processType == 'normal':
            print('---------------------------------------\nnow work on normal model\n---------------------------------------')
            self.normalP()
        else:
            print('---------------------------------------\ncant match any model\nnow work on normal model\n---------------------------------------')
            self.normalP()

    def normalP(self):
        loginHandle = libApi.login()
        htmlHandel = loginHandle.login()
        if htmlHandel == None:
            return
        maaHandle = libApi.maa(htmlHandel)
        maaHandle.getSeatBaseInfo()
        maaHandle.selectSeat()
        maaHandle.getSeatInfo()
        maaHandle.showAllAvaibleSeat()
        maaHandle.maa()

    def bookAP(self):
        if self.checkConfig():
            if self.getLoginInfo():
                loginHandle = libApi.login()
                loginHandle.username = self.unpw[0]
                loginHandle.password = self.unpw[1]
                htmlHandel = loginHandle.loginCore()
                if htmlHandel == None:
                    return
                if self.getSeatInfo():
                    maaHandle = libApi.maa(htmlHandel)
                    maaHandle.data = self.seatInfo
                    maaHandle.getSeatInfo()
                    maaHandle.showAllAvaibleSeat()
                    maaHandle.maa()
                else:
                    print('The seat information is damaged')
            else:
                print('The login information is damaged')
        else:
            print('The user config is damaged')

    def bookBP(self):
        if self.checkConfig():
            if self.getLoginInfo():
                loginHandle = libApi.login()
                loginHandle.username = self.unpw[0]
                loginHandle.password = self.unpw[1]
                htmlHandel = loginHandle.loginCore()
                if htmlHandel == None:
                    return
                if self.getSeatInfo():
                    if self.getSeatId():
                        maaHandle = libApi.maa(htmlHandel)
                        maaHandle.data = self.seatInfo
                        st = self.seatInfo[3]
                        et = int(st) + int(self.seatInfo[4]) * 60
                        mark = maaHandle.maaCore(self.seatId,st,str(et))
                        if mark:
                            print('---------------------------------------\nmaa success\n---------------------------------------')
                        else:
                            print('---------------------------------------\nnormal maa fail\ntrying auto maa\n---------------------------------------')
                            if self.getAutoSelect():
                                maaHandle.getSeatInfo()
                                length = len(maaHandle.seatInfoSet)
                                if not length == 0:
                                    rs = random.randint(0,length - 1)
                                    randomSeatId = maaHandle.seatInfoSet[rs][2]
                                    st = self.seatInfo[3]
                                    et = int(st) + int(self.seatInfo[4]) * 60
                                    mark = maaHandle.maaCore(randomSeatId,st,str(et))
                                    if mark:
                                        print('---------------------------------------\nauto maa success\n---------------------------------------')
                                        print('we have booked a seat in ' + maaHandle.seatInfoSet[rs][0] + ' ' + maaHandle.seatInfoSet[rs][1])
                                    else:
                                        print('---------------------------------------\nauto maa fail\nmaa core error\n----------------------------------------')
                                else:
                                    print('---------------------------------------\nauto maa fail\naccording to your condition we cant find any seat\n---------------------------------------')
                            else:
                                print('---------------------------------------\nauto maa is disable\nmaa fail\n---------------------------------------')
                    else:
                        print('The seat id is damaged')
                else:
                    print('The seat information is damaged')
            else:
                print('The login information is damaged')
        else:
            print('The user config is damaged')

    def autoSelectP(self):
        if self.checkConfig():
            if self.getLoginInfo():
                loginHandle = libApi.login()
                loginHandle.username = self.unpw[0]
                loginHandle.password = self.unpw[1]
                htmlHandel = loginHandle.loginCore()
                if htmlHandel == None:
                    return
                if self.getSeatInfo():
                    maaHandle = libApi.maa(htmlHandel)
                    maaHandle.data = self.seatInfo
                    maaHandle.getSeatInfo()
                    length = len(maaHandle.seatInfoSet)
                    if not length == 0:
                        rs = random.randint(0,length - 1)
                        randomSeatId = maaHandle.seatInfoSet[rs][2]
                        st = self.seatInfo[3]
                        et = int(st) + int(self.seatInfo[4]) * 60
                        mark = maaHandle.maaCore(randomSeatId,st,str(et))
                        if mark:
                            print('---------------------------------------\nmaa success\n---------------------------------------')
                            print('we have booked a seat in ' + maaHandle.seatInfoSet[rs][0] + ' ' + maaHandle.seatInfoSet[rs][1])
                        else:
                            print('---------------------------------------\nmaa fail\nmaa core error\n---------------------------------------')
                    else:
                        print('---------------------------------------\nmaa fail\naccording to your condition we cant find any seat\n---------------------------------------')
                else:
                    maaHandle = libApi.maa(htmlHandel)
                    maaHandle.getSeatBaseInfo()
                    maaHandle.selectSeat()
                    maaHandle.getSeatInfo()
                    length = len(maaHandle.seatInfoSet)
                    if not length == 0:
                        rs = random.randint(0,length - 1)
                        randomSeatId = maaHandle.seatInfoSet[rs][2]
                        st = self.seatInfo[3]
                        et = int(st) + int(self.seatInfo[4]) * 60
                        mark = maaHandle.maaCore(randomSeatId,st,str(et))
                        if mark:
                            print('---------------------------------------\nmaa success\n---------------------------------------')
                            print('we have booked a seat in ' + maaHandle.seatInfoSet[rs][0] + ' ' + maaHandle.seatInfoSet[rs][1])
                        else:
                            print('---------------------------------------\nmaa fail\nmaa core error\n----------------------------------------')
                    else:
                        print('---------------------------------------\nmaa fail\naccording to your condition we cant find any seat\n---------------------------------------')
            else:
                print('The login information is damaged')
        else:
            print('The user config is damaged')

def main():
    p = autoProcess()
    p.mainControl()


if __name__ == '__main__':
    main()