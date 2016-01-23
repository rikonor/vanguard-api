class VanguardUser(object):
    def __init__(self, user):
        service_info = user["services"]["vanguard"]

        self.username = service_info["username"]
        self.password = service_info["password"]
        self.security_questions = service_info["security_questions"]
