import unittest
import json
from another_version import app, get_db_connection

class TestFlaskMySQLApp(unittest.TestCase):
    def test_get_books(self):
        response = self.client.get('/api/books')
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        response = self.client.get('/api/books/1')
        self.assertEqual(response.status_code, 200)

    def test_create_book(self):
        response = self.client.post('/api/books', json={
            'title': 'New Book',
            'author': 'Author',
            'year': 2024
        })
        self.assertEqual(response.status_code, 201)

    def test_update_book(self):
        response = self.client.put('/api/books/1', json={
            'title': 'Updated Title'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        response = self.client.delete('/api/books/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
