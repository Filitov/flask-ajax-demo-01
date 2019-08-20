from flask import Flask

import werkzeug.serving
import threading
import time

import datetime   # 測試用 /api/test


def debug(message):
    print(message)
    # pass


data = 'aa'                 # for data suppily demo
data_suppily_thread = None


def data_suppily():
    global data
    data = str(datetime.datetime.now())
    register_background_thread()


# from https://github.com/rubenmak/PokemonGo-SlackBot/blob/master/example.py
def register_background_thread(initial_registration=False):
    debug('reg_bg_thread called')
    global data_suppily_thread

    if initial_registration:
        debug('reg_bg_thread: initial registration')
        if not werkzeug.serving.is_running_from_reloader():
            debug('reg_bg_thread: not start, because not running inside Flask')
            return
        if data_suppily_thread:
            debug('reg_bg_thread: thread already running')
            return
        data_suppily_thread = threading.Thread(target=data_suppily)
    else:
        debug('reg_bg_thread: queueing')
        data_suppily_thread = threading.Timer(3, data_suppily)  # delay in sec

    data_suppily_thread.daemon = True
    data_suppily_thread.name = 'data_suppily_thread'
    data_suppily_thread.start()


app = Flask(__name__)


@app.route('/')
def index_page():
    return app.send_static_file('index.html')


@app.route('/api/test')
def test_page():
    return data


if __name__ == "__main__":
    register_background_thread(initial_registration=True)
    app.run(debug=True)
    # app.run(debug=False, host=127.0.0.1, port=5000, threaded=True)
