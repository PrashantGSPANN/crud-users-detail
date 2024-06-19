from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import pymysql

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
    
data_base = client['flask_crud']
CORS(app)

@app.route('/')
def index():
    # data = db['users'].get('')
    return render_template('index.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    
    # Add data to database using PUT method
    if request.method == 'POST':
        body = request.json
        name = body['name']
        age = body['age']

        # db.users.insert_one({
        data_base['users'].insert_one({
            "name": name,
            "age": age
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'name': name,
            'age': age
        })
    
    # Method used to fetch all the users data from database
    if request.method == 'GET':
        allData = data_base['users'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            name = data['name']
            age = data['age']
            dataDict = {
                'id': str(id),
                'name': name,
                'age': age
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # search for specific user data
    if request.method == 'GET':
        data = data_base['users'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        name = data['name']
        age = data['age']
        dataDict = {
            'id': str(id),
            'name': name,
            'age': age
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # method to delete a user data object
    if request.method == 'DELETE':
        data_base['users'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # update a user data object
    if request.method == 'PUT':
        body = request.json
        name = body['name']
        age = body['age']

        data_base['users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "name":name,
                    "age":age
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})

if __name__ == '__main__':
    app.debug = True
    app.run()