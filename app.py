import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Azure Cosmos DB Connection String
# Azure will provide this in the 'AZURE_COSMOS_CONNECTIONSTRING' variable
app.config["MONGO_URI"] = os.environ.get(
    "AZURE_COSMOS_CONNECTIONSTRING", 
    "mongodb://localhost:27017/local_notes_db" # Fallback for local testing
)

# Initialize PyMongo
mongo = PyMongo(app)
db = mongo.db.notes # This creates/uses a 'notes' collection

@app.route('/')
def index():
    # Fetch all notes from Cosmos DB
    all_notes = db.find()
    return render_template('index.html', notes=all_notes)

@app.route('/add', methods=['POST'])
def add_note():
    content = request.form.get('content')
    if content:
        # Insert into NoSQL collection
        db.insert_one({'content': content})
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_note(id):
    # Delete using the unique NoSQL ObjectId
    db.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
