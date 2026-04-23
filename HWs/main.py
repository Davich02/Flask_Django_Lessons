#1.Find a mistake

#from flask import Flask
#app = Flask(__name__)

#@app.route('')  # Ошибка находится тут) В роуте не хватает слэша,пустая строка не является корректным URL-путём.
#def home():
#    return f'Hello, World!'

#if __name__ == '__main__':
#   app.run()


#2
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/user/<name>')
def user(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)
