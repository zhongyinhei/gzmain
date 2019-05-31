from flask import Blueprint, render_template, request, jsonify, g

from database.sqllite_operate import session
from gz_yct_pynex import Iter_Task

gengzong = Blueprint('gengzong', __name__)


@gengzong.route('/action', methods=['GET'])
def gengzong_run():
    '''运行跟踪'''
    res = dict(request.args)
    Iter = Iter_Task()
    if '手动' in res:
        import time
        time.sleep(10)
        '''调用手动函数'''
        result = Iter.breadth_first(STATE='手动')
        if result:
            return jsonify({'msg': 'success_gz', 'code': 0})
        elif not result:
            return jsonify({'msg': 'session_expire', 'code': 1})


jinru = Blueprint('jinru', __name__)


@jinru.route('/', methods=['GET'])
def index():
    '''进入界面'''
    if request.args.get('state') == 'finsh':
        try:
            session.execute(
                'update yctjdugip set state="unuse"')
        except Exception as e:
            session.rollback()
            raise e
        else:
            text = '"已完成跟踪任务，成功退出，谢谢！"'
            return render_template('unable.html', text=text)
    if g.result:
        vnc_url = 'http://116.228.76.163:3240/yct_vnc.html?path=?token=yuanqu2016'
        # vnc_url = 'http://192.168.130.27:5000/yct_vnc.html?path=?token=yuanqu2016'
        try:
            session.execute(
                'update yctjdugip set state="used"')
        except Exception as e:
            session.rollback()
            raise e
        return render_template('JsBasePage.html', vnc_url=vnc_url)
    else:
        text = '"进度跟踪机器正在使用中，请稍后再试，谢谢！"'
        return render_template('unable.html', text=text)
