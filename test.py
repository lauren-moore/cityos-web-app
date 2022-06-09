from server import app
import unittest

class FlaskTest(unittest.TestCase):

    
    def test_index(self):
        """Check for response 200."""
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)


    def test_index_content(self):
        """Check if content is text/html."""
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type,"text/html; charset=utf-8")


if __name__ == "__main__":
    unittest.main()
