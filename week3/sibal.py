from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get-json', methods=['GET'])
def send_json():
    # 응답할 데이터 (Python 딕셔너리)
    data = {
        'name': 'John Doe',
        'age': 30,
        'city': 'Seoul'
    }
    # JSON 형식으로 변환하여 응답
    return jsonify(data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
