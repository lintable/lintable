"""Supply the frontend pages."""

from datetime import datetime
from flask import request, render_template
from db import db
from lintweb import app
# from lintball.lintball import lint_github

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
    @app.route('/account/<identifier>')
    def account(identifier=None):
        """View details for an existing user account."""
        # TODO: Use logged in cookies to get user automatically
        # TODO: Only allowing viewing a user page for a logged in user
        #       (in the future we can extend this to an admin viewing any user)
        if identifier is not None:
            user = db.get_user(identifier)
            repos = db.get_repos_for_user(identifier)
            return render_template('account.html',
                                   username=user.username,
                                   repos=repos)
        else:
            user = None
            return render_template('account.html')

    @app.route('/register')
    def register():
        """Register a new user account."""
        return render_template('register.html')

    @app.route('/login')
    def login():
        """Log into an existing user account."""
        return render_template('login.html')

    @app.route('/status')
    @app.route('/status/<identifier>')
    def status(identifier=None):
        """Get a list of active jobs, or get the status of a job in progress."""
        if identifier is not None:
            job = db.get_job(identifier)
            if not job.endTime:
                currently_running = True
                duration = datetime.now() - job.startTime
            else:
                currently_running = False
                duration = job.endTime - job.startTime
            return render_template('status.html',
                                   identifier=job.id,
                                   repo_url=job.url,
                                   currently_running=currently_running,
                                   duration=duration,
                                   status=job.status)
        else:
            # TODO: Use logged in cookies to get jobs for user
            return render_template('status.html')

    @app.route('/terms')
    def terms():
        """View the terms of service."""
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
