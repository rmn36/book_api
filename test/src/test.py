import unittest
import requests
import json
import sys

class TestBookAPI(unittest.TestCase):
    def test_create_user(self):
        put_response = requests.put('http://api:5000/create_user', json={"email":"ryannowacoski@gmail.com", "first_name":"Ryan", "last_name":"Nowacoski", "password":"password"})
        self.assertEqual(put_response.status_code, 200)

        get_response = requests.get('http://api:5000/get_user/ryannowacoski@gmail.com')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.text, "('ryannowacoski@gmail.com', 'Ryan', 'Nowacoski')")

    def test_get_user_not_found(self):
        response = requests.get('http://api:5000/get_user/not@found.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "None")

    def test_create_book(self):
        put_response = requests.put('http://api:5000/create_book', json={"isbn":"0-7475-3269-9", "title":"Harry Potter and the Sorcerers Stone", "author":"J. K. Rowling", "pub_date":"1 September 1998"})
        self.assertEqual(put_response.status_code, 200)

        get_response = requests.get('http://api:5000/get_book/0-7475-3269-9')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.text, "('0-7475-3269-9', 'Harry Potter and the Sorcerers Stone', 'J. K. Rowling', '1 September 1998')")

    def test_get_book_not_found(self):
        response = requests.get('http://api:5000/get_book/0000000000000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "None")

    def test_update_book(self):
        post_response = requests.post('http://api:5000/update_book', json={"isbn":"0-7475-3269-9", "title":"Harry Potter and the Philosophers Stone", "author":"J. K. Rowling", "pub_date":"1 September 1998"})
        self.assertEqual(post_response.status_code, 200)

        get_response = requests.get('http://api:5000/get_book/0-7475-3269-9')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.text, "('0-7475-3269-9', 'Harry Potter and the Philosophers Stone', 'J. K. Rowling', '1 September 1998')")
        


if __name__ == "__main__":
    unittest.main()