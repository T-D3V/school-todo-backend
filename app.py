from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources=r'/api/*')

# health check
@app.route('/api/health', methods=['GET'])
def health():
  return jsonify('API is answering!')

if __name__ == '__main__':
  app.run()