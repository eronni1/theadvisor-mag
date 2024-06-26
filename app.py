from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient('localhost', 11111)
db = client['theadvisor']
collection = db['mag']

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

@app.route('/papers', methods=['GET'])
def get_papers():
    papers_list = list(collection.aggregate([{"$sample": {"size": 50}}]))
    # Manually ensure that ObjectId is converted to string for each document
    for paper in papers_list:
        paper['_id'] = str(paper['_id'])
    return jsonify(papers_list)

if __name__ == '__main__':
    app.run(debug=True)
