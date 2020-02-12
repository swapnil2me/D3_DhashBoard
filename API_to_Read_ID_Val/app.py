import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Time
import pandas as pd
from flask_marshmallow import Marshmallow

# API settings
app = Flask(__name__)
app.debug = True

# DB settings
POSTGRES_URL = "localhost:5433"
POSTGRES_USER = "postgres"
POSTGRES_PW = "Astrome123"
POSTGRES_DB = "APIdb"

#DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
#app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
basedir = "/mnt/5a576321-1b84-46e6-ba92-46de6b117d92/GitHub/Alpha_Project/Alpha_Project/DB_seed"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Idmetric(db.Model):
    __tablename__ = 'idmetric'
    id = Column(Integer, primary_key=True)
    hostname = Column(String)
    metric = Column(String)
    location = Column(String)


class Idvalue(db.Model):
    __tablename__ = 'idvalue'
    time = Column(DateTime, primary_key=True)
    id = Column(Integer)
    value = Column(String)



class IdmetricSchema(ma.Schema):
    class Meta:
        fields = ('id','hostname','metric','location')


class IdvalueSchema(ma.Schema):
    class Meta:
        fields = ('id','value','time')


idmetric_schema = IdmetricSchema(many = True)
idvalue_schema = IdvalueSchema(many = True)


# Routes
@app.route('/getIDs')
def getIDs():
    table = Idmetric.query.all()
    result = idmetric_schema.dump(table)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    #return jsonify(result)


@app.route('/getData')
def getData():
    request_id = request.args.get('id')
    request_count = int(request.args.get('nVals'))
    table = Idvalue.query.filter_by(id=request_id)[-request_count:]
    result = idvalue_schema.dump(table)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    #return jsonify(result)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8001)
