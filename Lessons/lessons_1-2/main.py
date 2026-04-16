from flask import Flask


app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World!11'

@app.route('/user_name/<user>')
def hello_user(user):
    return f'Hello {user}!'

@app.route('/<int:number>')
def numbers(number):
    return f'{number}!'

@app.route('/files/<path:filepath>')
def show_file(filepath):
    return f'File: {filepath}'


@app.route('/user/<uuid:user_id>')
def show_user_profile_by_uuid(user_id):
    return f'User with uuid: {user_id}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)