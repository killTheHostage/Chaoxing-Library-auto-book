import libApi
import re

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
        seatInfo = []
        seatInfo.append(date[0])
        seatInfo.append(building[0])
        seatInfo.append(room[0])
        seatInfo.append(st[0])
        seatInfo.append(hour[0])
        seatInfo.append(et[0])
        seatInfo.append(power[0])
        seatInfo.append(window[0])
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
                self.seatId = un[0]
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
            self.bookAP()
        elif self.processType == 'bookB':
            self.bookBP()
        elif self.processType == 'autoBook':
            self.seatId
        elif self.processType == 'lock':
            self.seatId
        elif self.processType == 'normal':
            self.normalP()

    def normalP(self):
        loginHandle = libApi.login()
        htmlHandel = loginHandle.login()
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
                            print('---------------------------------------\nmaa fail\n---------------------------------------')
                    else:
                        print('The seat id is damaged')
                else:
                    print('The seat information is damaged')
            else:
                print('The login information is damaged')
        else:
            print('The user config is damaged')

def main():
    p = autoProcess()
    p.mainControl()

if __name__ == '__main__':
    main()