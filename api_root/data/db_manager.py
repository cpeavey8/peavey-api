from bson import ObjectId
import pymongo
from pydantic import BaseModel

# Cooper Peavey
# CS 518 - DB Manager
class DBManager:

    def __init__(self, conn_str:str, db, col):
        '''connect to db server and set self.col'''
        
        myclient = pymongo.MongoClient(conn_str)
        mydb = myclient[db]
        self.col = mydb[col]

    def create(self, d: dict):
        '''create user and return inserted_id'''

        d['_id'] = str(ObjectId())
        self.col.insert_one(d)
        return d['_id']
    

    def read_by_id(self, obj_id: str):
        '''read by id and return one'''
        
        doc = self.col.find_one({'_id': obj_id})
        if not doc:
            return None
        # Map _id to id for compatibility
        if '_id' in doc:
            doc['id'] = doc['_id']
        return doc

        
    def read(self,query:dict):
        '''read by query and return many'''
        query = {k: v for k, v in query.items() if v is not None}
        docs = list(self.col.find(query))
        # Map _id to id for compatibility
        for doc in docs:
            if '_id' in doc:
                doc['id'] = doc['_id']
        return docs
    
    def read_all(self):
        '''read all and return many'''

        docs = list(self.col.find({}))
        # Map _id to id for compatibility
        for doc in docs:
            if '_id' in doc:
                doc['id'] = doc['_id']
        return docs

    def update(self,obj_id,updates:dict):
        ''' update by id and return modified_count '''

        result = self.col.update_one({'_id': obj_id}, {'$set': updates})
        return result.modified_count
        

    def delete_by_id(self,obj_id):
        ''' delete by id and return deleted_count '''

        result = self.col.delete_one({'_id': obj_id})
        return result.deleted_count
    
    def delete(self,query:dict):
        ''' update by query and return deleted_count '''

        result = self.col.delete_many(query)
        return result.deleted_count
    
    def delete_all(self):
        result = self.col.delete_many({})
        return result.deleted_count        

    def authenticate(self, username:str, password:str):
        ''' authenticate username/password '''
        users = self.read({'username': username, 'password': password})
        if users and len(users) > 0:
            return users[0]
        return None      
