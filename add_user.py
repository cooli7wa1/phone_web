import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'user'
MONGO_COLLECTION = 'user'

client = pymongo.MongoClient(MONGO_URL, connect=False)
collection = client[MONGO_DB][MONGO_COLLECTION]

input_msg = raw_input('Please input <username:password>: ')
username, password = input_msg.split(':')

if collection.find_one({'username': username}):
    print('Username already exist')
    exit(1)
else:
    collection.insert_one({'username': username, 'password': password})
    print('Add user success')
    exit(0)
