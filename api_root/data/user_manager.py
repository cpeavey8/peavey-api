from .db_manager import DBManager
from .user_models import *
import bcrypt

# from pymongo.errors import DuplicateKeyError

class UserManager:
    '''The UserManager takes model objects from the UserAPI.  It dumps them and passes them to DBManager for db operations.
    DBManager returns python objects (e.g. dicts, lists).
    UserManager converts those to model objects and passes back to the UserAPI.
    '''

    #------------------ init and reset ----------

    def __init__(self, dbm: DBManager):
        '''connect to db server and set self.col'''

        self.dbm = dbm
        self.dbm.col.create_index('username' , unique=True)

    def delete_all(self):
        ''' delete all users except admin (for testing)'''

        count = self.dbm.delete({'username': {'$ne': 'admin'}})
        return count    
    
    #----------------- CRUD ----------------------

    def create_user(self,user:User) -> str:
        ''' create user
        :returns: id as str'''

        ud = user.model_dump(exclude_none=True)
        # Hash password with bcrypt
        if 'password' in ud:
            hashed = bcrypt.hashpw(ud['password'].encode('utf-8'), bcrypt.gensalt())
            ud['password'] = hashed.decode('utf-8')
        id = self.dbm.create(ud)
        return str(id)

    def read_all(self) -> list[User]:
        ''' read users '''
        users = self.dbm.read_all()
        return [User(**user) for user in users]


    def read_by_id(self,id: str) -> User:
        ''' read by id
        :returns: User or None'''

        r = self.dbm.read_by_id(id)
        if r:
            return User(**r)
        else:
            return None

    def read_by_username(self,username: str) -> User:
        '''read by username
        :returns: User or None'''

        r = self.dbm.read({'username':username})
        if r:
            return User(**r[0])
        else:
            return None

    def update(self,id,q:UserUpdate) -> int:
        '''update user
        :returns: modified_count'''
        updates = q.model_dump(exclude_none=True)
        # Hash password with bcrypt if being updated
        if 'password' in updates:
            hashed = bcrypt.hashpw(updates['password'].encode('utf-8'), bcrypt.gensalt())
            updates['password'] = hashed.decode('utf-8')
        n = self.dbm.update(id,updates)
        return n
        
    def delete(self, query: dict) -> int:
        '''delete user
        :returns: deleted_count'''
        count = self.dbm.delete(query)
        return count

    def read(self, query: dict) -> list[User]:
        '''read users by query
        :returns: list of Users'''
        results = self.dbm.read(query)
        if results:
            return [User(**user) for user in results]
        return []

    def authenticate(self, username:str, password:str) -> User:
        ''' authenticate username/password
        :returns: User or None ''' 
        user = self.read_by_username(username)
        if user:
            # Check bcrypt hashed password
            try:
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    return user
            except (ValueError, AttributeError):
                # Fall back to plain text comparison
                if user.password == password:
                    return user
        return None

   
