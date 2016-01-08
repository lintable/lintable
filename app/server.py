from uuid import UUID

import flask
from flask import Flask, request

from calc.entry import calc, get_group_results

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
    result = calc(xs)
    response = result
    return flask.jsonify(response)


@app.route('/lists/<task_id>', methods=['GET'])
def get_task_status_by_id(task_id: UUID):
    result = get_group_results(task_id)
    return flask.jsonify(result)

if __name__ == '__main__':
    app.run()
