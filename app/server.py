from flask import Flask, request, redirect

from lintball.lintball import lint_github
from git.github import github_oauth_response
from uuid import uuid4, UUID
import urllib

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


@app.route('/oauth/<accountid>')
def github_oauth(accountid=None):
    local_url = 'https://www.lintable.com/oauth/response/' + str(accountid)
    url = 'https://github.com/login/oauth/authorize'
    state = uuid4()
    #store uuid in DB under accountid
    params = {'client_id' : None,
              'redirect_uri' : None,
              'scope' : None,
              'state' : state}
    params = urllib.urlencode(params)
    url = '{}?{}'.format(url, params)
    return redirect(url, code=302)


@app.route('/oauth/response/<accountid>', methods=['POST'])
def github_oauth_response(accountid=None):
    payload = request.get_json()
    access_token = github_oauth_response(payload=payload, accountid=accountid)
    return

if __name__ == '__main__':
    app.run()
