from flask import Flask, request

app = Flask(__name__)


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
    return 'The count was {count}'.format(count=len(xs))

if __name__ == '__main__':
    app.run()
