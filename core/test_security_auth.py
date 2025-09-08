import unittest
from core.security_auth import AuthSystem

class TestAuthSystem(unittest.TestCase):

    def test_auth_system(self):
        auth = AuthSystem()
        self.assertTrue(auth.validate_user('admin', 'StarSon@2025'))
        self.assertFalse(auth.validate_user('admin', 'wrong_password'))
        auth.add_user('new_user', 'new_password')
        self.assertTrue(auth.validate_user('new_user', 'new_password'))

if __name__ == '__main__':
    unittest.main()
