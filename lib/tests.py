import random
import unittest
import pymongo
from mongo import MongoAccess


class TestMongoConnect(unittest.TestCase):

    def setUp(self):
        pass

    def test_connect(self):
        """Testing connection behavior."""
        db=MongoAccess()
        self.assertEqual(db.connection.host, "localhost")


    def test_getDbList(self):
        db=MongoAccess()
        db.setDatabase("test_db")
        db_list=db.getDbList()
        # "local" database should always be in MongoDb server
        self.assertEqual("local" in db_list,True)


    def test_getDbListJson(self):
        db=MongoAccess()
        db_list=db.getDbList()
        # "local" database should always be in MongoDb server
        self.assertEqual("local" in db_list,True)

    def test_insert(self):
        db=MongoAccess()
        db.setDatabase("test_db")
        post = {"author": "Mike","text": "My first blog post!"}
        db.insert("test_table",post)
        #db.posts.insert(post);

    def test_dropDb(self):
        db=MongoAccess()
        db.dropDatabase("test_db")

    def test_dropDbNotExists(self):
        """Testing how do trying to drop non existing db works """
        pass




class TestMongoAccess(unittest.TestCase):

    def setUp(self):
        self.db=MongoAccess()
        self.test_db_name="test_accees_db"
        self.test_table_name="test_table"
        self.db.setDatabase(self.test_db_name)

        post = {"author": "Mike","text": "My first blog post!"}
        self.db.insert(self.test_table_name,post)
        post2 = {"author": "John","text": "Testing as secong post!"}
        self.db.insert(self.test_table_name,post2)
        post3 = {"author": "John","text": "Testing as third post!"}
        self.db.insert(self.test_table_name,post3)


    def test_getTableList(self):
        tables=self.db.getTableList()
        self.assertEqual(len(tables)>0 ,True)

    def test_getTableListNoDb(self):
        """need to exit gracefully, if no db is set """
        my_db=MongoAccess()
        tables=my_db.getTableList()
        self.assertEqual(len(tables),0)

    def test_getAll(self):
        data=self.db.getAll(self.test_table_name)
        self.assertEqual(data.count(),3)

    def test_getAllNoDbSet(self):
        """testing get all data if no database is set"""
        my_db=MongoAccess()
        data=my_db.getAll(self.test_db_name)
        self.assertEqual(data ,None)


    def test_getTableColumns(self):
        post2 = {"author": "John","text": "Testing as secong post!"}
        self.db.insert(self.test_table_name,post2)
        post = {"co-author": "John","text": "Testing as third post!"}
        self.db.insert(self.test_table_name,post)

        col_data=self.db.getTableColumns(self.test_table_name)
        #print col_data
        sample_col_names=['_id', 'author', 'co-author', 'text']
        self.assertEqual(col_data ,sample_col_names)






    def test_getOne(self):
        data=self.db.getOne(self.test_table_name)
        self.assertEqual(data["author"],"Mike")

    def test_getOneFilter(self):
        data=self.db.getOne(self.test_table_name,{"text":"Testing as third post!"})
        self.assertEqual(data["author"],"John")

    def test_insertDuplicate(self):
        """tests if data is the same, will it be inserted or not. It have to be inserted """
        post3 = {"author": "John","text": "Testing as third post!"}
        self.db.insert(self.test_table_name,post3)
        data=self.db.getAll(self.test_table_name)
        self.assertEqual(data.count(),4)

    def test_saveWithId(self):
        post = {"author": "John","text": "Testing as third post!"}
        data=self.db.getOne(self.test_table_name,post)
        data["author"]="Jim"
        jims_text="Jims blog post"
        data["text"]=jims_text
        self.db.save(self.test_table_name,data)
        data=self.db.getOne(self.test_table_name,{"text":jims_text})
        self.assertEqual(data["author"],"Jim")

    def test_update(self):
        post = {"author": "John","text": "Testing as secong post!"}
        data=self.db.getOne(self.test_table_name,post)
        jims_text="Jims secong blog post"
        data["text"]=jims_text

        self.db.update(self.test_table_name,data)

        data=self.db.getOne(self.test_table_name,{"text":jims_text})
        self.assertEqual(data["text"],jims_text)
        
    def test_delete(self):
        row_count=self.db.getAll(self.test_table_name).count()
        row_to_delete=self.db.getOne(self.test_table_name)
        self.db.delete(self.test_table_name,row_to_delete)
        row_count_after=self.db.getAll(self.test_table_name).count()
        #print "before "+str(row_count)+" after "+str(row_count_after)
        self.assertEqual(row_count-1,row_count_after)


    def test_dropTable(self):
        pass

    def test_asJSON(self):
        data=self.db.getAll(self.test_table_name)
        json_data=self.db.asJSON(data)
        import json
        self.assertEqual(type(json.loads(json_data)),type([]))


    def test_changeTable(self):
        "testing if data is displayed properly after changing table"
        pass




    def tearDown(self):
        self.db.dropDatabase(self.test_db_name)
        pass


if __name__ == '__main__':
    unittest.main()