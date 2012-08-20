from flask import Flask, jsonify
from flask import render_template
from flask import request

from lib.mongo import MongoAccess
import json

app = Flask(__name__)

db=MongoAccess()
table_name=""
#db.connect()
#db.set_database("truckroutes")

@app.route('/')
def index():
    return render_template('main.html')        


@app.route('/dblist')
def dblist():
    db_data=db.getDbList()
    return json.dumps(db_data)


@app.route('/tablelist/<db_name>')
def tablelist(db_name):

    db.setDatabase(db_name)
    table_data=db.getTableList(db_name)
    return json.dumps(table_data)

#@app.route('/get_all/<table_name>', method='POST')
@app.route('/get_all/<table_name>')
def get_all(table_name):
    #request.form['table_name']
    data= db.getAll(table_name)
    print data


    if data is not None:
        return db.asJSON(data)
    else:
        return "{}"


if __name__ == '__main__':
    app.debug = True
    app.run()