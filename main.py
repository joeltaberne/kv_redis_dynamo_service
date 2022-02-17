from flask import Flask, jsonify, request
import redis

default_key_expiration_time = 120
r = redis.Redis(host='172.17.0.2', port=6379, db=0)
app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({"message": "pong"})

@app.route('/getAllKeys')
def getAllKeys():
    keysList = []
    for key in r.scan_iter():
        keysList.append({key.decode("utf-8"): r.get(key).decode("utf-8")})
    return jsonify(keysList)

@app.route('/getKey', methods=['POST'])
def getKey ():
    if 'key' in request.args:
        if r.get(request.args['key']) is not None:
            return jsonify(r.get(request.args['key']).decode("utf-8"))

@app.route('/putKey', methods=['POST'])
def putKey():
    expiration_time = default_key_expiration_time if request.args['expiration_time'] is None else request.args['expiration_time']
    if 'key' in request.args and 'value' in request.args:
        r.set(request.args['key'], request.args['value'], int(expiration_time))
        return jsonify({request.args['key']: request.args['value']})
    return 'Key or value are NULL'

if __name__ == '__main__':
    app.run(debug=True, port=8080)