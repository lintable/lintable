"""Supply the frontend pages."""

from flask import request, render_template, redirect
from lintweb import app
from uuid import uuid4
from git import github
from settings.settings import LINTWEB_SETTINGS
import urllib.parse
from github import Github
# from lintball.lintball import lint_github

@app.route('/')
def index():
    """View the homepage."""
    return render_template('index.html')

@app.route('/account')
@app.route('/account/<accountid>')
def account(accountid=None):
    """View details for an existing user account."""
    return render_template('account.html', accountid=accountid)

@app.route('/register')
def register():
    """Register a new user account."""
    return render_template('register.html')

@app.route('/login')
def login():
    """Log into an existing user account."""
    return render_template('login.html')

@app.route('/status')
@app.route('/status/<jobid>')
def status(jobid=None):
    """Get the status of a given linting job in progress."""
    return render_template('status.html', jobid=jobid)

@app.route('/terms')
def terms():
    """View the terms of service.."""
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    """View the privacy policy."""
    return render_template('privacy.html')

@app.route('/security')
def security():
    """View the security info."""
    return render_template('security.html')

@app.route('/support')
def support():
    """View the support page."""
    return render_template('support.html')

@app.route('/payload', methods=['POST'])
def github_payload():
    """Trigger processing of a JSON payload."""
    payload = request.get_json()
    # lint_github.delay(payload=payload)
    return


@app.route('/register')
def github_oauth():
    # Gather data to send to Github
    url = LINTWEB_SETTINGS['github']['OAUTH_URL']
    params = {
        'client_id' : LINTWEB_SETTINGS['github']['CLIENT_ID'],
        'redirect_uri' : LINTWEB_SETTINGS['github']['CALLBACK'],
        'scope' : LINTWEB_SETTINGS['github']['SCOPES']
    }

    # Build query string and attach to URL
    params = urllib.parse.urlencode(params)
    url = '{}?{}'.format(url, params)

    return redirect(url, code=302)


@app.route('/oauth/callback')
def github_oauth_response():
    code = request.args.get('code')
    access_token = github.github_oauth_response(code=code)

    if access_token == None:
        return 'You did not accept our permissions.'

    user = Github(access_token).get_user()
    github_user_id = user.id

    # TODO: Store access token under accountid
    return 'Your Oauth token is: {} and your github id is: {}'.format(access_token, github_user_id)
