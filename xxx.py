# for i in range(1, 3):
#     time.sleep(2)
#     automation.SendKeys('{Down}')
# for i in range(1, 6):
#     for x in range(1, 8):
#         automation.SendKeys('{Down}')
#     res = REDIS_GZ.hset('specify_account_session', {'session': 'true'})
#     if 'true' not in res['session']:
#         pyautogui.screenshot(IMGSRC)
#         imgobj = file + r'\th.jpg'
#         imsrc = ac.imread(IMGSRC)
#         imobj = ac.imread(imgobj)
#         match_result = ac.find_template(imsrc, imobj,
#                                         0.8)
#         if match_result:
#             automation.HyperlinkControl(Depth=17, Name='退回修改', foundIndex=i).Click()
#             time.sleep(5)
#             if self.gain_session(name='退回修改') == 2:
#                 print('165行')
#                 return 1
#             elif self.restart_login == True:
#                 print('168行')
#                 return 1
#             else:
#                 print('171行')
#                 self.lddb()
#         imgobj = file + r'\txcg.jpg'
#         imobj = ac.imread(imgobj)
#         match_result = ac.find_template(imsrc, imobj,
#                                         0.8)
#         print(189)
#         if match_result:
#             automation.HyperlinkControl(Depth=17, Name='填报成功（查看详情）').Click()
#             time.sleep(5)
#             if self.gain_session(name='填报成功') == 2:
#                 print('192')
#                 return 1
#             elif self.restart_login == True:
#                 print('190行')
#                 return 1
#             else:
#                 print(193)
#                 time.sleep(5)
#                 self.lddb()
#     else:
#         print(196)
#         continue
# # if name['getpage'] == name['total']:
# if name['getpage'] == '3':
#     print('205')
#     return 1
# else:
#     print(208)
#     return
# else:
# self.restart_login = True
# print('204行')
# return 1
#
import time
time.sleep(5)
import uiautomation as automation
automation.SendKeys('{End}')