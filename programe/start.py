from flask import Blueprint, render_template, request, jsonify, g

from gz_yct_pynex import Iter_Task

gengzong = Blueprint('gengzong', __name__)
Iter = Iter_Task()


@gengzong.route('/action', methods=['GET'])
def gengzong_run():
    '''运行跟踪'''
    res = dict(request.args)
    if res['state'] == '手动':
        '''调用手动函数'''
        result = Iter.breadth_first(STATE=res['state'])
        if result:
            return jsonify({'msg': '成功完成进度跟踪', 'code': 0})
        elif not result:
            return jsonify({'msg': '身份失效请重新点击登录', 'code': 1})


jinru = Blueprint('jinru', __name__)


@jinru.route('/', methods=['GET'])
def index():
    '''进入界面'''
    if g.result:
        # vnc_url = 'http://116.228.76.163:3240/yct_vnc.html?path=?token=yuanqu2016'
        vnc_url = 'http://192.168.130.27:5000/yct_vnc.html?path=?token=yuanqu2016'
        return render_template('JsBasePage.html', vnc_url=vnc_url)
    else:
        return render_template('unable.html')
