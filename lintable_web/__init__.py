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
from flask import Flask, request, render_template, redirect, url_for, session, abort
from github import Github

from lintable_db.database import DatabaseHandler
from lintable_db.models import User
from lintable_settings.settings import LINTWEB_SETTINGS

app = Flask(__name__) # pylint: disable=invalid-name

LOGGER = logging.getLogger(__name__)
DEBUG = LINTWEB_SETTINGS['DEBUG']

################################################################################
# Define views
################################################################################

@app.route('/')
def index():
    """View the homepage."""

    if DEBUG:
        return render_template('coming_soon.html')

    if not DEBUG:
        return render_template('index.html')

if not DEBUG:
    @app.route('/account', methods=['GET', 'POST'])
    @app.route('/account/<identifier>', methods=['GET', 'POST'])
    def account(identifier=None):
        """View details for an existing user account."""

        if not session.get('logged_in') or not session.get('user_id'):
            abort(401)

        # In the future, we can extend this to an admin viewing any user.
        if session['user_id'] != identifier:
            abort(401)

        user = DatabaseHandler.get_user(session['user_id'])
        if user is None:
            abort(401)

        if request.method == 'POST':
            new_repo = request.form['repo-url-new']
            submit_value = request.form['submit']

            if new_repo != '':
                repo_url_to_add = new_repo
                # TODO: Add new repo here.

            if submit_value.startswith['delete-repo-']:
                repo_id_to_delete = submit_value[12:]
                # TODO: Delete repo here.

        return render_template('account.html',
                               user=user,
                               repos=user.repos)

    @app.route('/status')
    @app.route('/status/<identifier>')
    def status(identifier=None):
        """Get a list of active jobs, or get the status of a job in progress.

        :param identifier: A UUID identifying the job.
        """

        if identifier is not None:
            job = DatabaseHandler.get_job(identifier)
            if job is None:
                abort(404)

            if job.end_time is None:
                currently_running = True
                duration = datetime.now() - job.start_time
            else:
                currently_running = False
                duration = job.end_time - job.start_time

            return render_template('status.html',
                                   job=job,
                                   currently_running=currently_running,
                                   duration=duration)
        else:
            if not session.get('user_id'):
                abort(401)

            user = DatabaseHandler.get_user(session['user_id'])
            if user is None:
                abort(401)

            return render_template('status.html', user=user)

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

        params_str = urllib.parse.urlencode(params)
        url = '{}?{}'.format(url, params_str)

        return redirect(url, code=302)

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
                return 'You did not accept our permissions.'

        github_user = Github(access_token).get_user()
        github_user_id = github_user.id

        if DatabaseHandler.get_user(github_user_id) is None:
            user = User(github_id=github_user_id, token=access_token)
            user.save()

        # Save to active session to stay logged in.
        session['user_id'] = user.id

        return redirect(url_for('account'))

################################################################################
# Start the server
################################################################################

if __name__ == '__main__':
    print("running app: ", __name__)
    app.run()
