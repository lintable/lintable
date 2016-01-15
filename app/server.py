from flask import Flask, request

from lintball.lintball import lint_github

app = Flask(__name__)


def __init(self):
    super.__init__(self)


@app.route('/about')
def about():
    return 'About Lintball.'


@app.route('/payload', methods=['POST'])
def github_payload():
    payload = request.get_json()
    lint_github.delay(payload=payload)
    return

if __name__ == '__main__':
    app.run()
