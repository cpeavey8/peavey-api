import json
import bcrypt
import unittest
from datetime import datetime 

from fastapi.testclient import TestClient
from icecream import ic
from main import app

class TestUserAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        '''run once'''

        self.client = TestClient(app)
        self.client.delete('/users/all')
        # res = self.client.get('/users/')
        # print(res.text)

    def setUp(self):
        pass
        # print(self.id())
        print()

    def tearDown(self):
        self.client.delete('/users/all')
        pass

    #-------------------- BASE ----------------

    def test_create_read_all(self):
        '''create user, read all 
        assert that user is there'''

        ms = datetime.now().microsecond
        un = f"user{ms}"

        res = self.client.post('/users',json={
            'username':un,
            'password':"pw"
        })

        uid = json.loads(res.text)

        res = self.client.get('/users/')
        res_data = json.loads(res.text)

        un_check = res_data.get('users')[-1].get('username')
        self.assertEqual(un_check,un)


    #-------------------- CREATE ----------------

    def test_bad_create(self):
        '''validating requests - automatically handled by fastAPI'''

        res = self.client.post('/users',json={
            'username':"user"
        })       
    
        self.assertEqual(res.status_code,422)

    def test_duplicate(self):
        '''duplicate username should return 409'''

        res = self.client.post('/users',json={
            'username':"admin",
            'password':"pw"
        })
        # print(res.text)
        self.assertEqual(res.status_code,409)

    #-------------------- READ ----------------

    def test_read_by_username(self):

        res = self.client.get('/users/admin')
        # print(res.status_code, res.text)

        self.assertEqual(res.status_code,200)        
        u = json.loads(res.text)
        self.assertEqual(u.get('username'),'admin')

    def test_read_by_id(self):
        # ''' read by id'''

        ms = datetime.now().microsecond
        un = f"user{ms}"

        res = self.client.post('/users',json={
            'username':un,
            'password':"pw"
        })
        self.assertEqual(res.status_code,200)
        id = json.loads(res.text)

        ic()
        ic(res.text, id)

        res = self.client.get('/users/',params={'id':id})
        # print(res.status_code, res.text)

        self.assertEqual(res.status_code,200)        
        u = json.loads(res.text)
        self.assertEqual(u.get('username'),un)        

    def test_user_not_found(self):
        '''user not found should return 404'''

        res = self.client.get('/users/notexist')
        # print(res.status_code, res.text)
        self.assertEqual(res.status_code,404)  

    #-------------------- UPDATE ----------------

    def test_update_password(self):

        ms = datetime.now().microsecond
        un = f"user{ms}"

        res = self.client.post('/users',json={
            'username':un,
            'password':"pw"
        })

        res = self.client.put(f'/users/{un}',
                                 json={'password':"new"})
        # print(res.status_code,res.text)
        # self.assertEqual(res.status_code,200)
        
        res = self.client.get(f'/users/{un}')
        # print(res.text)

        u = json.loads(res.text)
        # print(u.get("password"))

        b1 = u.get('password')=='new'
        b2 = verify_password('new',u.get('password'))

        if not(b1 or b2):
            self.fail("password doesn't match")  

    def test_update_by_id(self):

        ms = datetime.now().microsecond
        un = f"user{ms}"

        res = self.client.post('/users',json={
            'username':un,
            'password':"pw"
        })
        self.assertEqual(res.status_code,200)
        id = json.loads(res.text)

        res = self.client.put(f'/users/',
                                params={'id':id},
                                json={'password':"new"})

        res = self.client.get(f'/users/{un}')
        u = json.loads(res.text)

        b1 = u.get('password')=='new'
        b2 = verify_password('new',u.get('password'))

        if not(b1 or b2):
            self.fail("password doesn't match")        

    #-------------------- DELETE ----------------

    def test_delete_by_username(self):
        '''test delete user by username'''

        ms = datetime.now().microsecond
        un = f"user{ms}"

        res = self.client.post('/users',json={
            'username':un,
            'password':"pw"
        })

        res = self.client.delete(f'/users/{un}')
        self.assertEqual(res.text,"1")

        res = self.client.get('/users/')
        us = json.loads(res.text)
        self.assertEqual(len(us.get('users')),1)

    #-------------------- AUTHENTICATE ----------------

    def test_authenticate(self):
        res = self.client.post('/users/authenticate',json={
            'username':'admin',
            'password':'admin'
        })

        # ic()
        # ic(res.text)
        u = json.loads(res.text)
        self.assertEqual(u.get('username'),'admin')

# def hash_password(pw):
#     return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()) 

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

if __name__ == '__main__':
    unittest.main()


