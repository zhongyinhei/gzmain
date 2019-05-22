# -*- coding:utf-8 -*-
import re
import time
from collections import deque

import aircv as ac
# from pywinauto import application
import pyautogui
import uiautomation as automation

from database.redis_mangager import RedisDB

# 初始化当前模板环境
REDIS_GZ = RedisDB()
dirs = r'C:\Program Files\Mozilla Firefox\firefox.exe'


class YCTGZ():
    def __init__(self):
        self.restart_login = False
        self.get_session = False
        self.change_account = False

    def yzdl(self):
        '''用于验证登录匹配是否有办理进度跟踪字样，如果有返回1说明登录成功'''
        # result = automation.ButtonControl(Depth=3, Name='继续')
        # if automation.WaitForExist(result, 5):
        #     automation.SendKeys('{Ctrl}k{Ctrl}k')
        #     automation.SendKeys('{Enter}')
        result = automation.CustomControl(Depth=9, Name='办理进度跟踪')
        if automation.WaitForExist(result, 5):
            print('yzdl 成功')
            return 1
        else:
            print('办理进度跟踪木有')
            self.restart_login = True

    def gain_session(self):
        '''获取点击暂存以后得到的session'''
        time.sleep(5)
        for i in range(1, 3):
            automation.SendKeys('{Down}')
        time.sleep(8)
        pyautogui.screenshot('./screen.png')
        imgsrc = './screen.png'
        imgobj = './YCTGZ_CS/thyj.png'
        imsrc = ac.imread(imgsrc)
        imobj = ac.imread(imgobj)
        match_result = ac.find_template(imsrc, imobj,
                                        0.7)
        if match_result:
            result = REDIS_GZ.hget('specify_account_yctAppNo_page')
            if result['total'] == result['getpage'] and result['total']:
                self.get_session = False
                return 2
            automation.SendKeys('{Ctrl}k{Ctrl}k')
            time.sleep(2)
            automation.SendKeys(
                'http://yct.sh.gov.cn/portal_yct/webportal/handle_progress.do{Enter}')
            pyautogui.screenshot('./screenshot.jpg')
            imsrc = ac.imread('./screenshot.jpg')
            imobj = ac.imread('./YCTGZ_CS/bljdgz.jpg')
            match_result = ac.find_template(imsrc, imobj,
                                            0.8)
            if match_result:
                self.get_session = False
                return 1
            else:
                self.restart_login = True
                return 1
        else:
            self.restart_login = True
            return 1

    def lddb(self):
        # 判断页数是否是相同不相同则继续点击下一页
        print('进入第二页')
        pyautogui.screenshot('./screenshot.jpg')
        imsrc = ac.imread('./screenshot.jpg')
        imobj = ac.imread('./YCTGZ_CS/bljdgz.jpg')
        match_result = ac.find_template(imsrc, imobj,
                                        0.8)
        if match_result:
            result = automation.EditControl(Depth=14, foundIndex=10)
            print('下一页 成功', self.get_session)
            name = re.compile('\d+').findall(result.Name)
            for i in range(1, 3):
                automation.SendKeys('{Down}')
            for i in range(1, 6):
                for x in range(1, 8):
                    automation.SendKeys('{Down}')
                if not self.get_session:
                    print('判断次数{}'.format(i))
                    # res = automation.HyperlinkControl(Depth=17, Name='退回修改', foundIndex=i)
                    pyautogui.screenshot('./screen.png')
                    imgsrc = './screen.png'
                    imgobj = './YCTGZ_CS/th.jpg'
                    imsrc = ac.imread(imgsrc)
                    imobj = ac.imread(imgobj)
                    match_result = ac.find_template(imsrc, imobj,
                                                    0.8)
                    if match_result:
                        automation.HyperlinkControl(Depth=17, Name='退回修改', foundIndex=i).Click()
                        time.sleep(5)
                        if self.gain_session() == 2:
                            return 1
                        elif self.restart_login == True:
                            return 1
                        else:
                            self.lddb()
                else:
                    continue
            x, y = name[:2]
            if x == y:
                return 1
            else:
                return
        else:
            self.restart_login = True
            return 1

    def djxyy(self):
        '''根据当前是否有下一页,如果有则点击如果没有下一页就返回1'''
        print('点击进入下一页,成功')
        automation.ButtonControl(Depth=14, foundIndex=4).Click()
        time.sleep(10)

    def pjurl(self):
        '''控制鼠标到url栏，删除，重写，按enter键'''
        specify_account_yctAppNo = REDIS_GZ.hget('specify_account_yctAppNo')
        print(specify_account_yctAppNo, 'i am specify_account_yctAppNo')
        if specify_account_yctAppNo:
            for yctAppNo in specify_account_yctAppNo:
                print(yctAppNo, 'yctAppNo')
                automation.SendKeys('{Ctrl}k{Ctrl}k')
                automation.SendKeys(
                    '%s{Enter}' % (
                        'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/print?yctAppNo={}'.format(yctAppNo)))
                time.sleep(5)
                break
        else:
            return 1

    def pcontent(self):
        '''celery调度broker做任务从代理中获取文本内容'''
        time.sleep(5)
        pyautogui.screenshot('./screen.png')
        imgsrc = './screen.png'
        imgobj = './YCTGZ_CS/ysjg_thxg.png'
        imsrc = ac.imread(imgsrc)
        imobj = ac.imread(imgobj)
        match_result = ac.find_template(imsrc, imobj,
                                        0.8)
        if match_result:
            return
        else:
            self.restart_login = True
            return 1

    def yztc_dl(self):
        '''判断当前是否跳转重新登录的提示'''
        result = automation.HyperlinkControl(Depth=11, Name='账号密码登录')
        if automation.WaitForExist(result, 5):
            result.Click()
            return 1
        else:
            raise ('yztc_dl异常')

    def portal_yct(self):
        '''第一次跳转到登录页'''
        result = automation.EditControl(Depth=11, Name='开办企业申请信息填写人需进行实名认证，系统将跳转至“一网通办”总门户进行用户注册和认证')
        if automation.WaitForExist(result, 5):
            automation.HyperlinkControl(Depth=10, Name='确定').Click()
        else:
            raise ('portal_yct异常')


class Iter_Task(YCTGZ):
    def __init__(self):
        YCTGZ.__init__(self)

    def breadth_first(self, STATE):
        '''获取一个账号然后分别轮询login，trace_list和detail事件'''
        self.STATE = STATE
        # app = application.Application()
        # app.connect(path=dirs, timeout=20)
        while not self.change_account:
            while self.restart_login:
                for process_bar in ['request_login']:
                    eval('self.{}()'.format(process_bar))
                    if not self.restart_login:
                        return False
                    else:
                        pass
            self.run_step()
            if not self.restart_login:
                self.change_account = True
        return True

    def run_step(self):
        for process_bar in ['login', 'trace_list', 'detail', 'changeaccount']:
            try:
                eval('self.{}()'.format(process_bar))
            except Exception as e:
                print(e, '地203行')
            if self.restart_login:
                automation.SendKeys('{Ctrl}k{Ctrl}k')
                automation.SendKeys(
                    '%s{Enter}' % (
                        'http://yct.sh.gov.cn/portal_yct/webportal/handle_progress.do?x=11'))
                # 如果是这样点击一般mitmproxy就不需要在去拦截了
                break
        try:
            REDIS_GZ.hset('specify_account_yctAppNo_page', {'getpage': '', 'total': ''})
        except Exception as e:
            print(e, '地212行')
        return 'success'

    def Intelligent_verification(self, zip_key):
        '''定义了一个双向队列，用于步骤的依次轮询，每次会去取出一个键，
        如果返回的值为1则跳出否则从字典里面拿到对应键的值'''
        global q_q
        q_q = zip_key.pop('q_q')
        circle = zip_key.pop('circle')
        while q_q:
            token_plugin_cls = q_q.popleft()
            try:
                if eval('self.{}()'.format(token_plugin_cls)) == 1:
                    break
                else:
                    q_q += circle[token_plugin_cls]
            except Exception as e:
                print(e)
                raise e
        return True

    def request_login(self):
        '''请求url页面'''
        q_q = deque()
        circle = {}
        circle['order'] = ['portal_yct']
        circle['protal_yct'] = ['yztc_dl']
        q_q += circle['order']
        zip_key = {'q_q': q_q, 'circle': circle}
        return self.Intelligent_verification(zip_key)

    def login(self):
        # 轮询login的步骤
        q_q = deque()
        circle = {}
        circle['order'] = ['yzdl']
        q_q += circle['order']
        zip_key = {'q_q': q_q, 'circle': circle}
        return self.Intelligent_verification(zip_key)

    def trace_list(self):
        # 轮询trace_list的步骤f
        q_q = deque()
        circle = {}
        circle['order'] = ['lddb']
        circle['lddb'] = ['djxyy']
        circle['djxyy'] = ['lddb']
        q_q += circle['order']
        zip_key = {'q_q': q_q, 'circle': circle}
        return self.Intelligent_verification(zip_key)

    def detail(self):
        # 轮询所有detail的步骤  03079c59a5714ca9a9ff2349efb66877
        specify_account_yctAppNo = REDIS_GZ.hget('specify_account_yctAppNo')
        # 判断specify_account_yctAppNo如果<0说明yctAppNo全部都拼接成功 ，则返回1，否则将一直轮询
        if specify_account_yctAppNo:
            q_q = deque()
            circle = {}
            circle['order'] = ['pjurl']
            circle['pjurl'] = ['pcontent']
            circle['pcontent'] = ['pjurl']
            q_q += circle['order']
            zip_key = {'q_q': q_q, 'circle': circle}
            return self.Intelligent_verification(zip_key)

    def changeaccount(self):
        time.sleep(2)
        try:
            automation.SendKeys('{Ctrl}k{Ctrl}k')
            time.sleep(2)
            automation.SendKeys(
                'http://yct.sh.gov.cn/portal_yct/webportal/handle_progress.do{Enter}')
        except Exception as e:
            print(e)
        else:
            time.sleep(5)
            pyautogui.screenshot('./screen.png')
            imgsrc = './screen.png'
            imgobj = './YCTGZ_CS/tc.png'
            imsrc = ac.imread(imgsrc)
            imobj = ac.imread(imgobj)
            match_result = ac.find_template(imsrc, imobj,
                                            0.8)
            automation.HyperlinkControl(Depth=12, Name='退出').Click()
            time.sleep(5)
            if match_result:
                print('终于结束')
                automation.HyperlinkControl(Depth=11, Name='账号密码登录').Click()
            else:
                print('终于结束了!!!!!!!1')

# https://zwdtuser.sh.gov.cn/uc/login/login.jsp?self=self&type=1&jump=&redirect_uri=http://yct.sh.gov.cn/portal_yct/webportal/handle_progress.do
# Iter_Task().breadth_first('手动')

# 500服务器内部错误
