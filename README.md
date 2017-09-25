# UJN-Library-auto-book
济南大学图书馆便捷预约，目前的阶段实现了登陆和预约的完整业务流程，并封装成简单API的形式存在于两个类中
##login API
login类为登陆类，需要进行实例化才能使用
self.username：登陆用户名
self.password：登陆密码
self.loginUrl：登陆验证网址
self.header：UA（如果更改了self.loginUrl这一部分也要做出相应修改）
getCookies()：获取维持连接的cookie
getCaptcha()：获取登录所需的验证码，保存在运行目录下
loginCore()：login核心部分（支持直接传递username和password进行登陆）-返回登录成功后的HTML页面，失败返回None
login()：执行常规登陆流程（需要自己输入用户名密码）
##maa API
maa类为预约类，需要进行实例化才能使用
self.loginHtml：login返回的HTML句柄
self.dateSet：从网页解析到的时间集
self.buildingSet：从网页解析到的校区集
self.roomSet：从网页解析到的阅览室集
self.hourSet：从网页解析到的时间集
self.startSet：从网页解析到的开始筛选的时间集
self.endSet：从网页解析到的结束筛选的时间集
self.powerSet：从网页解析到的是否有插座集
self.windowSet：从网页解析到的是否靠窗集
self.data：用户筛查信息
self.seatInfoSet：查找到的符合条件的座位集
self.allSeatCount：查找到的符合条件的座位数
self.header：UA（如果更改了login类中的self.loginUrl这一部分也要做出相应修改）
getSeatBaseInfo()：从login传入的HTML句柄解析筛选条件
printSingleSet(筛选集)：打印筛选集（前提函数：getSeatBaseInfo()）--包含在selectSeat()中，且不推荐单独调用
selectSeat()：文本交互性选座（前提函数：getSeatBaseInfo()）
getSeatInfo()：获取到的符合条件的座位（核心函数：getSeatJson(页面)）
getSeatJson(页面)：获取单个页面中所有符合条件的座位信息存入self.seatInfoSet（前提条件：self.data不能为空）--包含在getSeatInfo()中，且不推荐直接调用
showAllAvaibleSeat()：打印查找到的所有符合条件的座位（前提函数：getSeatInfo()，核心前提函数：getSeatJson(页面)）
getStartTime(座位id)：获取按照筛选条件查找后预约开始的全部时间（前提函数：getSeatInfo()，核心前提函数：getSeatJson(页面)，前提条件：座位ID和预约日期）
getEndTime(座位id,开始预约时间)：获取按照筛选条件查找后预约结束的全部时间（前提函数：getSeatInfo() getStartTime()，核心前提函数：getSeatJson(页面)，前提条件：座位ID、预约日期和开始预约时间）
maaCore(座位id,开始预约时间,结束预约时间)：预约座位核心函数（前提条件：预约日期）
maa()：预约函数--不可单独调用，需要按照上述函数给出的流程调用
##autoProcess
autoProcess类为流程类，需要实例化才能使用（如果使用autoProcess类，默认不需要实例化上述两类）
self.userConfigTxt：用户配置文件
self.unpw：用户名密码集
self.seatInfo：座位筛选条件集
self.autoSelect：自动选座标识
self.seatId：座位ID
self.processType：工作方式--目前暂时支持：常规方式（normal），根据配置文件中的搜索条件直接搜索对应座位（bookA），根据配置文件中的座位ID和预约日期直接预约指定的座位ID（bookB）；以后将实现的：登陆后根据配置文件自动查找符合条件的座位，自动预约（autoBook），长期锁定某个座位（lock）
checkConfig()：检查配置文件是否存在（此类的前导函数，必须检查配置文件是否存在）--文件存在返回True，不存在返回False
getLoginInfo()：从配置文件中读入用户名密码--文件中存在同时存在用户名密码返回True，否则返回False
getSeatInfo（）：从配置文件中读入座位筛选信息--文件中存在完整的作为筛选信息返回True，否则返回False
getAutoSelect()：从配置文件中读入自动筛选标识--文件中存在自动筛选标识返回True，否则返回False
getSeatId()：从配置文件中读入座位ID--文件中存在座位ID返回True，否则返回False
getProcessType()：从配置文件中读入工作模式--文件中存在对应的工作模式存入对应工作模式，否则存入常规方式
mainControl()：解析工作模式，启动对应工作函数，如果工作模式填写错误，默认启动常规方式
normalP()：normal方式
bookAP()：bookA方式
bookBP()：bookB方式

注：目前login和maa两个类测试无问题，autoProcess存在bug还在继续完善中
