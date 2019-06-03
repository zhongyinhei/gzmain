# -*- coding:utf-8 -*-
from flask import Flask, g
from retrying import retry
# from flask_cors import *

from database.sqllite_operate import YCTGZIP, session
from programe.start import gengzong
from programe.start import jinru

app = Flask(__name__)
# CORS(app, supports_credentials=True)
from raven.contrib.flask import Sentry

# sentry = Sentry(app,
#                 dsn='https://96dfc306047645a68bb09c0f3f96a7f8:4326c716db4541158fe0e737ea20c23c@sentry.cicjust.com//11')


@retry(stop_max_attempt_number=3)
@app.before_request
def before_first():
    '''查看当前的园区对应的ip'''
    try:
        result = session.query(YCTGZIP).filter_by(token='yuanqu2016').first()
        session.close()
    except Exception as e:
        session.rollback()
        raise e
    else:
        state = result.state
        if 'unuse' in state:
            g.result = 1
        elif 'used' in state:
            g.result = 0


app.register_blueprint(jinru, url_prefix='/jinru')
app.register_blueprint(gengzong, url_prefix='/gengzong')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=7777)
