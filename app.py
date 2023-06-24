from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify(data='foobar')

@app.route('/ping')
def ping():
    return jsonify(data='pong')

if __name__ == '__main__':
    app.run()