from unittest import TestCase

from api.users import Users

def get_mock_user():
    username = "fake_user"
    email = "fake@email.com"
    password = "fake_password"
    Users.register_user(username, email, password)
    return Users.find_user(username)

def remove_mock_user():
    username = "fake_user"
    Users.delete_user(username)

class TestUsers(TestCase):
    def setUp(self):
        remove_mock_user()

    def tearDown(self):
        pass

    def test_gen_api_key(self):
        """Just check that the generated API key has 64 alphanumeric chars"""
        api_key = Users.gen_api_key()
        self.assertEqual(len(api_key), 64)
        self.assertTrue(api_key.isalnum())

    def test_can_hash_and_verify_password(self):
        """Hash a password, then verify it"""
        h = Users.hash_password("fake_password")
        self.assertFalse(Users.verify_password("even_faker_password", h))
        self.assertTrue(Users.verify_password("fake_password", h))

    def test_can_register_user(self):
        """Should be able to register a user"""
        username = "test_user_name"
        email = "test@password.com"
        password = "fake_password"

        Users.register_user(username, email, password)

        # Make sure the user now exists in the system
        user = Users.find_user(username)
        self.assertIsNotNone(user)

        # Clean up
        Users.delete_user(username)

    def test_cant_register_user_twice(self):
        """No duplicate usernames or emails"""
        username = "test_duplicate_user"
        email = "test@duplicate.com"
        password = "fake_password"

        Users.register_user(username, email, password)
        with self.assertRaises(RuntimeError):
            Users.register_user(username, email, password)

        # Clean up
        Users.delete_user(username)

    def test_can_delete_user(self):
        """Should be able to remove a user"""
        username = "test_user_to_delete"
        email = "test@delete.com"
        password = "fake_password"

        Users.register_user(username, email, password)
        Users.delete_user(username)

        # Make sure the user does not exist anymore
        user = Users.find_user(username)
        self.assertIsNone(user)

    def test_can_enroll_user_in_service(self):
        user = get_mock_user()

        service_info = dict(service_name="vanguard")
        service_info["username"] = "fake_user"
        service_info["password"] = "fake_password"
        security_questions = {
            "What was your first pet's name?": "poopie",
            "What is the name of your elementary school": "chewbaca"
        }
        service_info["security_questions"] = security_questions

        Users.enroll_in_service(user['user'], service_info)

        user = Users.find_user(user['user'])
        user_services = user.get("services", {})
        user_vanguard_service_info = user_services.get("vanguard")
        self.assertEqual(user_vanguard_service_info, service_info)

        remove_mock_user()

    def test_can_unenroll_user_in_service(self):
        user = get_mock_user()

        service_info = dict(service_name="vanguard")
        service_info["username"] = "fake_user"
        service_info["password"] = "fake_password"
        security_questions = {
            "What was your first pet's name?": "poopie",
            "What is the name of your elementary school": "chewbaca"
        }
        service_info["security_questions"] = security_questions

        Users.enroll_in_service(user['user'], service_info)
        Users.unenroll_from_service(user['user'], "vanguard")

        user = Users.find_user(user['user'])
        self.assertIsNone(user.get('services', {}).get("vanguard"))

        remove_mock_user()

    def test_cant_enroll_in_unsupported_service(self):
        user = get_mock_user()

        service_info = dict(service_name="unsupported_service")
        with self.assertRaises(RuntimeError):
            Users.enroll_in_service(user['user'], service_info)

        remove_mock_user()
