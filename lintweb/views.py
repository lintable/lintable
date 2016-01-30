"""Supply the frontend pages."""

from flask import request, render_template
from lintweb import app
# from lintball.lintball import lint_github

debug = True

@app.route('/')
def index():
    """View the homepage."""
    if debug:
        return render_template('coming_soon.html')
    return render_template('index.html')

@app.route('/payload', methods=['POST'])
def github_payload():
    """Trigger processing of a JSON payload."""
    payload = request.get_json()
    # lint_github.delay(payload=payload)
    return
