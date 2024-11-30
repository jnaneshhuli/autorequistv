from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

# MongoDB Collections
users = client['main']['users']
groups = client['main']['groups']

# Check if a user already exists in the database
def already_db(user_id):
    user = users.find_one({"user_id": str(user_id)})
    return user is not None

# Check if a group already exists in the database
def already_dbg(chat_id):
    group = groups.find_one({"chat_id": str(chat_id)})
    return group is not None

# Add a user to the database
def add_user(user_id):
    if not already_db(user_id):
        return users.insert_one({"user_id": str(user_id)})
    return None

# Remove a user from the database
def remove_user(user_id):
    if already_db(user_id):
        return users.delete_one({"user_id": str(user_id)})
    return None

# Add a group to the database
def add_group(chat_id):
    if not already_dbg(chat_id):
        return groups.insert_one({"chat_id": str(chat_id)})
    return None

# Get the total count of users
def all_users():
    user = users.find({})
    return len(list(user))

# Get the total count of groups
def all_groups():
    group = groups.find({})
    return len(list(group))
