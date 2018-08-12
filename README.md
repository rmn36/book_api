# Book Wishlist API

## Overview
This is a basic REST API written in Python3 using Flask as the REST framework, SQLite as the backing store and Docker for portabability and ease of testing. This API represents a User's book wishlist. The SQLite db is per instance of the API container therefore when the container is stopped and removed all the information is as well. Below are the supported operations and associated endpoints. 

## Endpoints
- POST `/create_user`
    ```json
    {
        "email": "USER_EMAIL",
        "first_name": "USER_FIRST_NAME",
        "last_name": "USER_LAST_NAME",
        "password": "USER_PASSWORD"
    } 
    ```
- PUT `/update_user`
    ```json
    {
        "email": "USER_EMAIL",
        "first_name": "USER_FIRST_NAME",
        "last_name": "USER_LAST_NAME",
        "password": "USER_PASSWORD"
    } 
    ```
- GET `/get_user/<user_email>`
- POST `/create_book`
    ```json
        {
            "isbn":"ISBN10/13",
            "title":"TITLE",
            "author":"AUTHOR",
            "pub_date":"PUB_DATE"
        }
    ```
- PUT `/update_book`
    ```json
        {
            "isbn":"ISBN10/13",
            "title":"TITLE",
            "author":"AUTHOR",
            "pub_date":"PUB_DATE"
        }
    ```
- GET `/get_book/<isbn>`
- POST `/add_to_wishlist`
    ```json
        {
            "user_email":"USER_EMAIL",
            "isbn":"ISBN",
            "notes":"NOTES" #optional
        }
    ```
- PUT `/update_wishlist`
    ```json
        {
            "user_email":"USER_EMAIL",
            "isbn":"ISBN",
            "notes":"NOTES"
        }
    ```
- DELETE `/delete_wishlist_item`
    ```json
        {
            "user_email":"USER_EMAIL",
            "isbn":"ISBN"
        }
    ```
- DELETE `/delete_wishlist/<user_email>`
- GET `/get_wishlist/<user_email>`

## Running and Testing
To run the api run `docker-compose up -d` from the root dir of this project. There are some sample requests in the `sample_request.txt` file. These requests assume the api is litening on `localhost`, if you're using docker-machine or k8s this might be different. 

To run the tests run the `run.sh` script in the `test/` dir. This will start an instance of the API container and run the test cases in `test/src/test.py` against that instance. These tests exercise all the basic functions. 