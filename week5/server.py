from flask import Flask
from flask_cors import CORS
import ssl

app = Flask(__name__)
CORS(app)    # 모바일기기 에서 돌리려면 필요할 수도 있대


@app.route('/tlqkf', methods=['GET'])
def send_json():
    return "tlqkf"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')    #ssl 인증서 받아오고 염병 떨어야 될거 같은데
