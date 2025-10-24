from icecream import ic
from pymongo.errors import DuplicateKeyError

from fastapi import FastAPI, HTTPException
import uvicorn

from data.user_models import *
from data.db_manager import DBManager
from data.user_manager import UserManager
from config import USER_CONFIG

db_manager = DBManager(USER_CONFIG.DB_URL, USER_CONFIG.USER_DB, USER_CONFIG.USER_COL)
user_manager = UserManager(db_manager)

app = FastAPI()

try:
    user_manager.delete({'username': 'admin'})
except Exception:
    pass

try:
    admin = User(username='admin', password='admin', admin=True)
    user_manager.create_user(admin)
except Exception:
    pass  

print('INFO: server loaded')

@app.get('/info')
async def get_info()->str:
    return "fastapi server"

#---------------- create -------------------

@app.post('/users')
async def create_user(user: User) -> str | None:
    '''create user and return result.

    :param user: User to create
    :returns: user id
    :raises HTTPException: 422 if username equals 'all' 
    :raises HTTPException: 409 if username is taken'''

    if user.username == "all":
        raise HTTPException(status_code=422, detail="username 'all' is reserved")   
    try:
        uid = user_manager.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
    else:
        return uid

#----------------------- READ --------------------------

@app.get('/users/')
async def read_users(id:str = None) -> UserCollection | User | None:
    '''
    if id is given, return user by id
    else return all users

    :param id: str id
    :returns: 
        User if valid id
        UserCollection if no id
    :raises: HTTPException 404 if user not found
    '''
    if id:
        user = user_manager.read_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        return user
    else:
        users = user_manager.read_all()
        return UserCollection(users=users)

@app.get("/users/{userName}")
async def read_user(userName:str) -> User | None:
    '''read user and return result.

    :param userName: str username
    :returns: User if valid username
    :raises HTTPException: 404 if user is not found'''
    user = user_manager.read_by_username(userName)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

#------------------------ update and delete ------------------

@app.put('/users/{userName}')
async def update_user(userName:str,user:UserUpdate) -> int:
    ''' update user by username and return result
    
    :param userName: str username
    :param user: UserUpdate fields to update
    :returns int modified_count
    :raises HTTPException: 404 user not found'''
    target_user = user_manager.read_by_username(userName)
    if not target_user:
        raise HTTPException(status_code=404, detail="user not found")
    result = user_manager.update(target_user.id, user)
    return result

@app.put('/users/')
async def update_user_by_id(id:str,user:UserUpdate) -> int:
    ''' update user by id and return result'''
    target_user = user_manager.read_by_id(id)
    if not target_user:
        raise HTTPException(status_code=404, detail="user not found")
    return user_manager.update(id,user)

#---------------- DELETE ----------------

@app.delete('/users/{username}')
async def delete_user(username: str) -> int:
    '''delete user by username

    :param username: delete by username
        if username == "all" delete all
    :raises HTTPException: 404 user not found
    '''
    if username == "all":
        deleted_count = user_manager.delete_all()
        return deleted_count
    user = user_manager.read_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    result = user_manager.delete({'username': username})
    return result


@app.delete('/users/')
async def delete_users(id:str) -> int:
    '''delete user by id

    :param uid: str id
    :returns: int deleted_count
    :raises HTTPException: 404 if user not found
    '''
    result = user_manager.delete({'_id': id})
    if result == 0:
        raise HTTPException(status_code=404, detail="user not found")
    return result 

#--------------- AUTH ----------------


@app.post('/users/authenticate')
async def authenticate_user(ua:UserAuth) -> User:
    '''authenticate user
    if userAuth is valid, return User
    
    :param ui: UserAuth with credentials
    :returns: User 
    :raises: 401 if authentication fails'''
    user = user_manager.authenticate(ua.username, ua.password)
    if not user:
        raise HTTPException(status_code=401, detail="authentication failed")
    return user

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
