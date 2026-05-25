from flask import Flask, request, send_file
import os

app = Flask(__name__)
BASE_DIR = "/app/public"

@app.route('/download')
def download():
    filename = request.args.get('file', '')
    # Уязвимость: нет проверки пути
    path = os.path.join(BASE_DIR, filename)
    return send_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
