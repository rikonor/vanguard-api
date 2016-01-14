from unittest import TestCase

from vanguard import Vanguard, config

class TestBrowser(TestCase):
    def setUp(self):
        self.v = Vanguard()

    def tearDown(self):
        self.v.close_browser()

    def test_can_login(self):
        self.v.login(config.TEST_USER, config.TEST_PASSWORD)

    def test_can_get_security_question(self):
        self.v.login(config.TEST_USER, config.TEST_PASSWORD)
        question = self.v.get_security_question()

    def test_can_answer_security_question(self):
        self.v.login(config.TEST_USER, config.TEST_PASSWORD)
        question = self.v.get_security_question()

        answer = config.TEST_SECURITY_QUESTIONS.get(question)
        assert answer is not None

        self.v.answer_security_question(answer)

    def test_can_go_to_balances_and_holdings(self):
        self.v.login(config.TEST_USER, config.TEST_PASSWORD)

        question = self.v.get_security_question()
        answer = config.TEST_SECURITY_QUESTIONS.get(question)
        self.v.answer_security_question(answer)

        self.v.go_to_balances_and_holdings()
        assert self.v.browser.title is "Balances and holdings"

    def test_can_get_total_assets(self):
        self.v.login(config.TEST_USER, config.TEST_PASSWORD)

        question = self.v.get_security_question()
        answer = config.TEST_SECURITY_QUESTIONS.get(question)
        self.v.answer_security_question(answer)

        self.v.get_total_assets()
