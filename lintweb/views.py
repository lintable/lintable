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

# from datetime import datetime
from flask import request, render_template

# from db import database
# from lintball import lintball
from lintweb import app

DEBUG = True

# TODO: Instance a database connection here using database.database_handler()
app_database = None

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
            # TODO: Use these once there's an actual db to connect to
            # user = app_database.get_user(identifier)
            # repos = app_database.get_repos_for_user(identifier)

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
            # TODO: Actually pull the job from the database
            # job = app_database.get_job(identifier)
            #
            # TODO: Do math here with start/end times
            # if not job.endTime:
            #     currently_running = True
            #     duration = datetime.now() - job.startTime
            # else:
            #     currently_running = False
            #     duration = job.endTime - job.startTime

            return render_template('status.html')
            # return render_template('status.html',
            #                        identifier=job.id,
            #                        repo_url=job.url,
            #                        currently_running=currently_running,
            #                        duration=duration,
            #                        status=job.status)
        else:
            # TODO: Use logged in cookies to get jobs for user
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
