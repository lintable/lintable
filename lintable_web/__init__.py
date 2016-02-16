"""Supplies the frontend pages."""

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

import json
import logging
import urllib.parse
from datetime import datetime

import requests
from flask import (Flask, request, render_template, redirect, url_for, session,
                   abort, flash)
from flask_login import (LoginManager, login_user, login_required, logout_user,
                         current_user)
from github import Github

from lintable_db.database import DatabaseHandler
from lintable_db.models import User
from lintable_settings.settings import LINTWEB_SETTINGS

app = Flask(__name__) # pylint: disable=invalid-name
app.secret_key = LINTWEB_SETTINGS['SESSIONS_SECRET']

login_manager = LoginManager()
login_manager.login_view = 'github_oauth'
login_manager.init_app(app)

LOGGER = logging.getLogger(__name__)
DEBUG = LINTWEB_SETTINGS['DEBUG']

################################################################################
# Authentication helpers
################################################################################

@login_manager.user_loader
def load_user(identifier: str) -> User:
    """Return a User object based on the given identifier."""

    return DatabaseHandler.get_user(int(identifier))

################################################################################
# Views
################################################################################

@app.route('/')
def index():
    """View the homepage."""

    if DEBUG:
        return render_template('coming_soon.html')

    if not DEBUG:
        return render_template('index.html')

if not DEBUG:
    @app.route('/account')
    @login_required
    def account():
        """View details for an existing user account."""

        return render_template('account.html')

    @app.route('/status')
    @app.route('/status/<identifier>')
    @login_required
    def status(identifier=None):
        """Get active jobs for the current user, or status of a job in progress.

        :param identifier: A UUID identifying the job.
        """

        if identifier is None:
            return render_template('status.html')

        job = DatabaseHandler.get_job(identifier)
        if job is None:
            abort(404)

        if job.user is not current_user:
            abort(403)

        return render_template('status.html', job=job)

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

    @app.route('/login')
    def login():
        return redirect(url_for('github_oauth'))

    @app.route('/register')
    def github_oauth():
        """Redirect user to github OAuth registeration page."""

        url = LINTWEB_SETTINGS['github']['OAUTH_URL']
        params = {
            'client_id': LINTWEB_SETTINGS['github']['CLIENT_ID'],
            'redirect_uri': LINTWEB_SETTINGS['github']['CALLBACK'],
            'scope': LINTWEB_SETTINGS['github']['SCOPES']
        }

        params_str = urllib.parse.urlencode(params)
        url = '{}?{}'.format(url, params_str)

        return redirect(url, code=302)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/callback')
    def github_oauth_response():
        """Receive OAuth code and retrieve token."""

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
        except requests.exceptions.RequestException as ex:
            LOGGER.error('Error posting to github: %s', ex)

        payload = json.loads(github_request.text)
        access_token = payload['access_token']
        scope_given = payload['scope'].split(',')

        # Check if we were given the right permissions
        scope_needed = LINTWEB_SETTINGS['github']['SCOPES'].split(',')
        for perm in scope_needed:
            if perm not in scope_given:
                flash('You did not accept our permissions.')
                return redirect(url_for('index'))

        github_user = Github(access_token).get_user()
        github_user_id = github_user.id

        user = DatabaseHandler.get_user(github_user_id)
        if user is None:
            user = User(github_id=github_user_id, token=access_token)
            user.save()

        login_user(user)

        flash('Logged in successfully.')
        return redirect(request.args.get('next') or url_for('account'))

################################################################################
# Start the server
################################################################################

if __name__ == '__main__':
    print("running app: ", __name__)
    app.run()
