from flask import Flask

import lintable_web.views

app = Flask(__name__)

if __name__ == '__main__':
    app.run()
