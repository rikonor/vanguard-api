msg = """In order to run the tests, you need to provide some credentials to your Vanguard account under vanguard/tests_config.py

IMPORTANT NOTICE:
    The tests are non-destructive and by definition must only perform querying operation.
    Under no circumstances shall a test be designed to perform a data altering operation.

Example tests_config.py

    TEST_USER = "<USER>"
    TEST_PASSWORD = "<PASSWORD>"
    TEST_SECURITY_QUESTIONS = {
        "<QUESTION1>": "<ANSWER1>",
        "<QUESTION2>": "<ANSWER2>",
        "<QUESTION3>": "<ANSWER3>"
    }

"""

# To run tests - remove the exception throwing and replace with credentials (as shown above)
raise EnvironmentError, msg
