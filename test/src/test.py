import unittest
import requests
import json
import sys
import re

class TestBookAPI(unittest.TestCase):
    def test_create_user(self):
        post_response = requests.post('http://api:5000/create_user', json={"email":"ryannowacoski@gmail.com", "first_name":"Ryan", "last_name":"Nowacoski", "password":"password"})
        self.assertEqual(post_response.status_code, 201)

        get_response = requests.get('http://api:5000/get_user/ryannowacoski@gmail.com')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.text, "('ryannowacoski@gmail.com', 'Ryan', 'Nowacoski')")

    def test_get_user_not_found(self):
        response = requests.get('http://api:5000/get_user/not@found.com')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, "None")

    def test_create_book(self):
        post_response = requests.post('http://api:5000/create_book', json={"isbn":"0-7475-3269-9", "title":"Harry Potter and the Sorcerers Stone", "author":"J. K. Rowling", "pub_date":"1 September 1998"})
        self.assertEqual(post_response.status_code, 201)

        get_response = requests.get('http://api:5000/get_book/0-7475-3269-9')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.text, "('0-7475-3269-9', 'Harry Potter and the Sorcerers Stone', 'J. K. Rowling', '1 September 1998')")

    def test_get_book_not_found(self):
        response = requests.get('http://api:5000/get_book/0000000000000')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, "None")

    def test_update_book(self):
        put_response = requests.put('http://api:5000/update_book', json={"isbn":"0-7475-3269-9", "title":"Harry Potter and the Philosophers Stone", "author":"J. K. Rowling", "pub_date":"1 September 1998"})
        self.assertEqual(put_response.status_code, 200)

        get_response = requests.get('http://api:5000/get_book/0-7475-3269-9')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.text, "('0-7475-3269-9', 'Harry Potter and the Philosophers Stone', 'J. K. Rowling', '1 September 1998')")

    def test_add_to_wishlist(self):
        post_response = requests.post('http://api:5000/add_to_wishlist', json={"isbn":"0-7475-3269-9", "user_email":"ryannowacoski@gmail.com", "notes":"BEST BOOK EVER"})
        self.assertEqual(post_response.status_code, 201)

        post_response = requests.post('http://api:5000/create_book', json={"isbn":"978-0439064873", "title":"Harry Potter And The Chamber Of Secrets", "author":"J. K. Rowling", "pub_date":"1 September 2000"})
        self.assertEqual(post_response.status_code, 201)

        post_response = requests.post('http://api:5000/add_to_wishlist', json={"isbn":"978-0439064873", "user_email":"ryannowacoski@gmail.com"})
        self.assertEqual(post_response.status_code, 201)

        #Added date is impossible to know so use regex to allow that field to be anything
        reg = re.compile('\A\[\(\'ryannowacoski@gmail.com\'\, \'0-7475-3269-9\'\, \'.*\'\, \'BEST BOOK EVER\'\)\, \(\'ryannowacoski@gmail.com\'\, \'978-0439064873\'\, \'.*\'\, None\)\]\Z')

        get_response = requests.get('http://192.168.99.100:5000/get_wishlist/ryannowacoski@gmail.com')
        self.assertEqual(get_response.status_code, 200)
        reg.match(get_response.text)
        self.assertNotEqual(reg.match(get_response.text), None)

    def test_delete_wishlist_item(self):
        delete_response = requests.delete('http://api:5000/delete_wishlist_item', json={"isbn":"978-0439064873", "user_email":"ryannowacoski@gmail.com"})
        self.assertEqual(delete_response.status_code, 200)

        #Added date is impossible to know so use regex to allow that field to be anything
        reg = re.compile('\A\[\(\'ryannowacoski@gmail.com\'\, \'0-7475-3269-9\'\, \'.*\'\, \'BEST BOOK EVER\'\)\]\Z')

        get_response = requests.get('http://192.168.99.100:5000/get_wishlist/ryannowacoski@gmail.com')
        self.assertEqual(get_response.status_code, 200)
        reg.match(get_response.text)
        self.assertNotEqual(reg.match(get_response.text), None)

    def test_delete_wishlist(self):
        post_response = requests.post('http://api:5000/add_to_wishlist', json={"isbn":"978-0439064873", "user_email":"ryannowacoski@gmail.com"})
        self.assertEqual(post_response.status_code, 201)

        #Added date is impossible to know so use regex to allow that field to be anything
        reg = re.compile('\A\[\(\'ryannowacoski@gmail.com\'\, \'0-7475-3269-9\'\, \'.*\'\, \'BEST BOOK EVER\'\)\, \(\'ryannowacoski@gmail.com\'\, \'978-0439064873\'\, \'.*\'\, None\)\]\Z')

        get_response = requests.get('http://192.168.99.100:5000/get_wishlist/ryannowacoski@gmail.com')
        self.assertEqual(get_response.status_code, 200)
        reg.match(get_response.text)
        self.assertNotEqual(reg.match(get_response.text), None)

        delete_response = requests.delete('http://api:5000/delete_wishlist/ryannowacoski@gmail.com')
        self.assertEqual(delete_response.status_code, 200)

        get_response = requests.get('http://192.168.99.100:5000/get_wishlist/ryannowacoski@gmail.com')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.text, "[]")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestBookAPI('test_create_user'))
    suite.addTest(TestBookAPI('test_get_user_not_found'))
    suite.addTest(TestBookAPI('test_create_book'))
    suite.addTest(TestBookAPI('test_get_book_not_found'))
    suite.addTest(TestBookAPI('test_update_book'))
    suite.addTest(TestBookAPI('test_add_to_wishlist'))
    suite.addTest(TestBookAPI('test_delete_wishlist_item'))
    suite.addTest(TestBookAPI('test_delete_wishlist'))
    return suite
        

if __name__ == "__main__":
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())