from flask import Flask

import datetime   # /api/test 示範用


app = Flask(__name__)


@app.route('/')
def index_page():
    return app.send_static_file('index.html')


@app.route('/api/test')
def test_page():
    return str(datetime.datetime.now())  # 示範用


if __name__ == "__main__":
    app.run(debug=True)
