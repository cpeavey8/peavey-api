class USER_API_CONFIG:
    API_URL = "http://localhost:7071"

class TEST_CONFIG:

    DB_URL = "mongodb+srv://cooppeavey_db_user:M00per4545%23@cluster0.cd3lhwy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    #DB_URL = "mongodb://localhost:27017"

    TEST_DB = "test_db"
    TEST_COL = "items"  

class USER_CONFIG(TEST_CONFIG):

    USER_DB = "user_db"
    USER_COL = "users"
