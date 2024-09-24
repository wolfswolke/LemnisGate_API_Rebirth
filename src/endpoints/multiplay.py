from flask_definitions import *

@app.route('/v1/fleets/9cdbc466-0e52-4c6c-9525-52354f45f81d/servers', methods=['GET'])
def servers():
    return jsonify({"servers": []}), 200
# This has not been patched into the game