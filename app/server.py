import flask
from flask import Flask, request

from calc.entry import calc

app = Flask(__name__)


def __init(self):
    super.__init__(self)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hi/<person>')
def hi_there(person):
    return 'Hi there {person}'.format(person=person)


# you can test this in postman by posting with {"list":[1, 2, 3]}
@app.route('/lists', methods=['POST'])
def print_list():
    data = request.get_json()
    xs = data['list']
    result = calc.delay(xs)
    response = result.wait()
    return flask.jsonify(response)


if __name__ == '__main__':
    app.run()
