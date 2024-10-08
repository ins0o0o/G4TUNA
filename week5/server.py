from flask import Flask
from flask_cors import CORS
import ssl

app = Flask(__name__)
CORS(app)    


@app.route('/tlqkf', methods=['GET'])
def send_json():
    return "tlqkf"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')   
