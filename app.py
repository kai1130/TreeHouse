from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify(data='foobar')

@app.route('/ping')
def ping():
    return jsonify(data='pong')

@app.route('init', methods=['GET'])
def init_platform():
  pass

@app.route('/product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    manufacturer = request.form.get('manufacturer')
    addr = request.form.get('addr')
    weight = request.form.get('weight')
    materials_metal = request.form.get('materials_metal')
    materials_plastic = request.form.get('materials_plastic')
    options_seats = request.form.get('options_seats')
    options_wheels = request.form.get('options_wheels')

    # Perform database insertion or any other desired operation with the received data

    return jsonify(data='Product added successfully')

if __name__ == '__main__':
    app.run()