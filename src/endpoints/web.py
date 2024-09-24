from flask_definitions import *


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/binarys/patched/LemnisGate-Win64-Shipping.exe', methods=['GET'])
def patched_shipping():
    return send_from_directory('static/files', 'LemnisGate-Win64-Shipping.exe')

@app.route('/binarys/patched/LemnisGate.exe', methods=['GET'])
def patched_launcher():
    return send_from_directory('static/files', 'LemnisGate.exe')