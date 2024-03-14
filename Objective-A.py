# Objective A -> Use the below API's to fetch Users and their corresponding posts data and store it in any Database of your choice.

from connection import db
import requests
import json

BASE_URL = "https://dummyapi.io/data/v1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'app-id': '65f185c7e5c046818b037545'
}

# Fetching Users data from dummyapi
def get_users():
    users_response = requests.get(f"{BASE_URL}/user", headers=headers)
    users_data = users_response.json()
    # Accessing the "data" key, defaulting to an empty list if key is not found
    data = users_data.get("data", [])  
    return data

# Storing Users data in database after fetching it
def store_users():
    users = get_users()
    db.users.insert_many(users)
    print("Users stored successfully.")

# Fetching all posts corresponding to the user with the user id from database
def get_posts():
    all_users = db['users'].find({})
    users_data = list(all_users)
    posts = []
    for user in users_data:
        user_posts_response = requests.get(f"{BASE_URL}/user/{user['id']}/post", headers=headers)
        user_posts_data = user_posts_response.json()
        posts.extend(user_posts_data.get("data", []))
    return posts

# Storing all the posts fetched from the database
def store_posts():
    posts = get_posts()
    db.posts.insert_many(posts)
    print("Posts saved to database successfully.")


if __name__ == '__main__':
    store_users()
    store_posts()
