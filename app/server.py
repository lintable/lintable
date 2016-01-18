from flask import Flask, request

from lintball.lintball import lint_github
from git.github import github_oauth_response

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


@app.route('/oauth', methods=['POST'])
def github_oauth():
    payload = request.get_json()
    access_token = github_oauth_response(payload=payload)
    return

if __name__ == '__main__':
    app.run()
