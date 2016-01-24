from unittest import TestCase

from vanguard import Vanguard, config, tests_config

class TestBrowser(TestCase):
    def setUp(self):
        self.v = Vanguard()

    def tearDown(self):
        self.v.close_browser()

    def test_can_login(self):
        self.v.login(tests_config.TEST_USER, tests_config.TEST_PASSWORD)

    def test_can_get_security_question(self):
        self.v.login(tests_config.TEST_USER, tests_config.TEST_PASSWORD)
        question = self.v.get_security_question()

    def test_can_answer_security_question(self):
        self.v.login(tests_config.TEST_USER, tests_config.TEST_PASSWORD)
        question = self.v.get_security_question()

        answer = tests_config.TEST_SECURITY_QUESTIONS.get(question)
        self.assertIsNotNone(answer)

        self.v.answer_security_question(answer)

    def test_can_go_to_balances_and_holdings(self):
        self.v.login(tests_config.TEST_USER, tests_config.TEST_PASSWORD)

        question = self.v.get_security_question()
        answer = tests_config.TEST_SECURITY_QUESTIONS.get(question)
        self.v.answer_security_question(answer)

        self.v.go_to_balances_and_holdings()
        self.assertEqual(self.v.browser.title, "Balances and holdings")

    def test_can_get_total_assets(self):
        self.v.login(tests_config.TEST_USER, tests_config.TEST_PASSWORD)

        question = self.v.get_security_question()
        answer = tests_config.TEST_SECURITY_QUESTIONS.get(question)
        self.v.answer_security_question(answer)

        self.v.get_total_assets()

    def test_can_get_current_holdings(self):
        self.v.login(tests_config.TEST_USER, tests_config.TEST_PASSWORD)

        question = self.v.get_security_question()
        answer = tests_config.TEST_SECURITY_QUESTIONS.get(question)
        self.v.answer_security_question(answer)

        self.v.get_current_holdings()
