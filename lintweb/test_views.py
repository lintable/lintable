from lintweb import app
import unittest

class ViewsTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_register_status_code(self):
        result = self.app.get('/register')
        self.assertEqual(result.status_code, 302)

    def test_index_status_code(self):
        result = self.app.get('/callback')
        self.assertEqual(result.status_code, 200)
