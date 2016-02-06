#Copyright 2015-2016 Capstone Team G
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

"""Supply the frontend pages."""
import json

import requests
import logging
from flask import request, render_template, redirect, url_for
from lintweb import app
from settings.settings import LINTWEB_SETTINGS
import urllib.parse
from github import Github
from db.database import database_handler
from db.models import User
# from lintball.lintball import lint_github
logger = logging.getLogger(__name__)

DEBUG = True

if DEBUG:
    @app.route('/')
    def index():
        """View the 'coming soon' version of the homepage."""
        return render_template('coming_soon.html')

if not DEBUG:
    @app.route('/')
    def index():
        """View the homepage."""
        return render_template('index.html')

    @app.route('/account')
    @app.route('/account/<accountid>')
    def account(accountid=None):
        """View details for an existing user account."""
        return render_template('account.html', accountid=accountid)

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
        """Redirect user to github OAuth registeration page."""
        url = LINTWEB_SETTINGS['github']['OAUTH_URL']
        params = {
            'client_id' : LINTWEB_SETTINGS['github']['CLIENT_ID'],
            'redirect_uri' : LINTWEB_SETTINGS['github']['CALLBACK'],
            'scope' : LINTWEB_SETTINGS['github']['SCOPES']
        }

        params = urllib.parse.urlencode(params)
        url = '{}?{}'.format(url, params)

        return redirect(url, code=302)

    @app.route('/callback')
    def github_oauth_response():
        """Receive OAuth code and retrieve token"""
        code = request.args.get('code')
        url = LINTWEB_SETTINGS['github']['OAUTH_URL_POST']

        if code is None:
            return "No github code found"

        # Construct outgoing data and a header
        outgoing = {
            'client_id' : LINTWEB_SETTINGS['github']['CLIENT_ID'],
            'client_secret': LINTWEB_SETTINGS['github']['CLIENT_SECRET'],
            'code': code,
            'redirect_url': LINTWEB_SETTINGS['github']['CALLBACK']
        }
        headers = {'Accept': 'application/json'}

        # Post data to github and capture response then parse returned JSON
        try:
            github_request = requests.post(url, data=outgoing, headers=headers)
        except requests.exceptions.RequestException as e:
            logger.error('Error posting to github: {}'.format(e))

        payload = json.loads(github_request.text)
        access_token = payload['access_token']
        scope_given = payload['scope'].split(',')

        # Check if we were given the right permissions
        scope_needed = LINTWEB_SETTINGS['github']['SCOPES'].split(',')
        for perm in scope_needed:
            if perm not in scope_given:
                return 'You did not accept our permissions.'

        github_user = Github(access_token).get_user()
        github_user_id = github_user.id

        if database_handler.get_user(github_user_id) is None:
            user = User(github_id=str(github_user_id), token=access_token)
            user.save()

        return redirect(url_for('account'))
