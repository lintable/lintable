# Copyright 2015-2016 Capstone Team G
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Supply the frontend pages."""

import json
import logging
import urllib.parse

import requests
from flask import request, render_template, redirect, url_for
from github import Github
from datetime import datetime

from lintable_db.database import DatabaseHandler
from lintable_db.models import User
from lintable_web.__init__ import app
from lintable_settings.settings import LINTWEB_SETTINGS

logger = logging.getLogger(__name__)

DEBUG = LINTWEB_SETTINGS['DEBUG']

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
    @app.route('/account/<identifier>')
    def account(identifier=None):
        """View details for an existing user account."""
        # TODO: Use logged in cookies to get user automatically
        # TODO: Only allowing viewing a user page for a logged in user
        #       (in the future we can extend this to an admin viewing any user)
        if identifier is not None:
            user = DatabaseHandler.get_user(identifier)
            if user is not None:
                repos = user.repos
            else:
                repos = None
            return render_template('account.html')
            # return render_template('account.html',
            #                        username=user.username,
            #                        repos=repos)
        else:
            user = None
            return render_template('account.html')


    @app.route('/login')
    def login():
        """Log into an account, or trigger OAuth with a new account."""
        # TODO: Wire this into OAuth
        return render_template('login.html')


    @app.route('/status')
    @app.route('/status/<identifier>')
    def status(identifier=None):
        """Get a list of active jobs, or get the status of a job in progress."""
        if identifier is not None:
            job = DatabaseHandler.get_job(identifier)
            if not job.endTime:
                currently_running = True
                duration = datetime.now() - job.startTime
            else:
                currently_running = False
                duration = job.endTime - job.startTime

            return render_template('status.html')
            # return render_template('status.html',
            #                        identifier=job.id,
            #                        repo_url=job.url,
            #                        currently_running=currently_running,
            #                        duration=duration,
            #                        status=job.status)
        else:
            # TODO: Use logged in cookies to get jobs for user
            # user_id = cookie.get_id()
            # user = DatabaseHandler.get_user(user_id)
            # if user is not None:
            #   jobs = user.jobs
            return render_template('status.html')


    @app.route('/terms')
    def terms():
        """View the terms of service."""
        # TODO: Possibly pull content from Markdown file
        return render_template('terms.html')


    @app.route('/privacy')
    def privacy():
        """View the privacy policy."""
        # TODO: Possibly pull content from Markdown file
        return render_template('privacy.html')


    @app.route('/security')
    def security():
        """View the security info."""
        # TODO: Possibly pull content from Markdown file
        return render_template('security.html')


    @app.route('/support')
    def support():
        """View the support page."""
        return render_template('support.html')


    @app.route('/payload', methods=['POST'])
    def github_payload():
        """Trigger processing of a JSON payload."""
        payload = request.get_json()
        # TODO: Make this actually work. Currently, lintball crashes on import.
        # lintball.lint_github.delay(payload=payload)
        return


    @app.route('/register')
    def github_oauth():
        """Redirect user to github OAuth registeration page."""
        url = LINTWEB_SETTINGS['github']['OAUTH_URL']
        params = {
            'client_id': LINTWEB_SETTINGS['github']['CLIENT_ID'],
            'redirect_uri': LINTWEB_SETTINGS['github']['CALLBACK'],
            'scope': LINTWEB_SETTINGS['github']['SCOPES']
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
            'client_id': LINTWEB_SETTINGS['github']['CLIENT_ID'],
            'client_secret': LINTWEB_SETTINGS['github']['CLIENT_SECRET'],
            'code': code,
            'redirect_url': LINTWEB_SETTINGS['github']['CALLBACK']
        }
        headers = {'Accept': 'application/json'}

        # Post data to github and capture response then parse returned JSON
        github_request = None
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

        if DatabaseHandler.get_user(github_user_id) is None:
            user = User(github_id=github_user_id, token=access_token)
            user.save()

        return redirect(url_for('account'))
