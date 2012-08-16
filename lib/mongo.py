# -*- coding: utf-8 -*-

"""
class for easy accessing MongoDb databases

"""
#import pymongo
import json
#from bson import BSON
from bson import json_util
import pymongo


class MongoAccess(object):
    """class for easy accessing MongoDb databases

    """
    def __init__(self, host="localhost",port=27017):
        super(MongoAccess, self).__init__()
        #self.host = host
        #self.port=port
        self.connect(host,port)

    def connect(self, host="localhost",port=27017):
        """ connect to database """
        self.connection = pymongo.Connection(host, port)

    def setDatabase(self,db_name):
        self.db = self.connection[db_name]

    def getDbList(self):
        return self.connection.database_names()

    def getTableList(self):
        data= self.db.collection_names()
        return data

    def format_json(self):
        pass

    def getAll(self,table_name,data_filter={}):

        if self.connection is None:
            print "cannot get connection"
            return None

        data=self.db[table_name].find(data_filter)
        return data



    def getOne(self,table_name,data_filter={}):
        if self.db is None:
            print "cannot get connection"
            return None

        data=self.db[table_name].find_one(data_filter)
        return data

    def insert(self,table_name,row_data):
        # TODO: exception handling
        if self.db is None:
            print "cannot get connection"
            return None

        return self.db[table_name].save(row_data)

    def save(self,table_name,row_data):
        """inserts or updates data if _id is not given"""
        if self.db is None:
            print "cannot get connection"
            return None

        return self.db[table_name].save(row_data)


    def update(self,table_name,row_data):
        if self.db is None:
            print "cannot get connection"
            return None

        return self.db[table_name].update({"_id":row_data["_id"]}, row_data)

    def deleteOne(self,table_name, row_data):
        row_id=row_data["_id"]
        self.db[table_name].remove(row_id)

    def delete(self,table_name, data_filter):
        self.db[table_name].remove(data_filter)


    def dropTable(self,table_name):
        if self.db is None:
            return None
        self.db.drop_collection(table_name)

    def dropDatabase(self,db_name):
        self.connection.drop_database(db_name)

    def asJSON(self,data, sort_keys=True, indent=4):
        
        return json.dumps(list(data), default=json_util.default)



