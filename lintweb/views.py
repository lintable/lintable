"""Supply the frontend pages."""

from flask import request, render_template
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
