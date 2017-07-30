from flask import Flask, request, jsonify
app = Flask(__name__)

from vanguard import Vanguard, VanguardUser, config
from users import Users
from errors import *
from responses import *

# Users Routes

def get_from_request_data(desired_params):
    """
    Given a list of params, try and get them from the request
    """
    request_data = request.get_json(force=True)
    params = dict()
    for p in desired_params:
        p_value = request_data[p]
        if p_value is None:
            raise MissingRequestParams
        params[p] = p_value
    return params

def auth():
    """
    Call this in the beginning of a handler in order to authenticate the request
    """
    params = get_from_request_data(["username", "password"])

    user = Users.find_user(params["username"])
    if user is None:
        raise UserNotFound

    authenticated = Users.auth_user(params["username"], params["password"])
    if authenticated is not True:
        raise AuthenticationFailed

    return user

@app.route("/register", methods=['POST'])
def register():
    # Register a user profile (user, password)
    try:
        params = get_from_request_data(["username", "password", "email"])
    except MissingRequestParams:
        return rMissingParams(["username", "password", "email"])

    try:
        Users.register_user(params["username"],params["email"],params["password"])
    except RuntimeError as e:
        return rInternalServerError

    try:
        user = auth()
    except AuthenticationFailed:
        return rAuthError

    user = Users.clean_user(user)
    return jsonify(user)

@app.route("/my_details", methods=['GET'])
def user_details():
    user = auth()
    user = Users.clean_user(user)
    return jsonify(user)

@app.route("/enroll", methods=['POST'])
def enroll_in_service():
    # Lets assume for now the only service we support is vanguard
    # For that reason, all service info validation logic shall be in this sole handler

    # required: service_name, username, password
    request_data = request.get_json(force=True)

    try:
        user = auth()
    except AuthenticationFailed:
        return rAuthError

    service_info = request_data.get("service_info")
    if service_info is None:
        return "Please provide service information for enrollment\n", 400

    service_name = service_info.get("service_name")
    username = service_info.get("username")
    password = service_info.get("password")
    if None in [service_name, username, password]:
        return "Please provide service information for enrollment\n", 400

    try:
        Users.enroll_in_service(username, service_info)
    except RuntimeError as e:
        print "ERROR:", e
        return rInternalServerError

    return "OK\n"

@app.route("/register_security_answer", methods=['POST'])
def register_security_answer():
    #request_data = request.get_json(force=True)

    try:
        user = auth()
    except AuthenticationFailed:
        return rAuthError

    try:
        params = get_from_request_data(["username","service_info"])
        service_info = params["service_info"]
    except MissingRequestParams:
        #Missing username is handled by auth()
        return rMissingServiceInfo

    service_name = service_info.get("service_name")
    question = service_info.get("question")
    answer = service_info.get("answer")
    if None in [service_name, question, answer]:
        return rMissingParams(["service_name", "question", "answer"])

    try:
        Users.register_security_answer(params["username"], service_name, question, answer)
    except RuntimeError as e:
        return rInternalServerError

    return "OK\n"

# Vanguard Routes

@app.route("/vanguard/total_assets")
def vanguard_total_assets():
    try:
        user = auth()
    except AuthenticationFailed:
        return rAuthError

    try:
        vanguard_user = VanguardUser(user)
    except KeyError:
        return rNotEnrolled

    res = None
    try:
        v = Vanguard()
        v.login(vanguard_user.username, vanguard_user.password)
        question = v.get_security_question()
        answer = vanguard_user.security_questions.get(question)
        v.answer_security_question(answer)

        total_assets = v.get_total_assets()
        res = dict(total=total_assets)
    finally:
        v.close_browser()
        if res is None:
            return rInternalServerError

    return jsonify(res)

@app.route("/vanguard/current_holdings")
def vanguard_current_holdings():
    try:
        user = auth()
    except AuthenticationFailed:
        return rAuthError

    try:
        vanguard_user = VanguardUser(user)
    except KeyError:
        return rNotEnrolled

    res = None
    try:
        v = Vanguard()
        v.login(vanguard_user.username, vanguard_user.password)
        question = v.get_security_question()
        answer = vanguard_user.security_questions.get(question)
        v.answer_security_question(answer)

        current_holdings = v.get_current_holdings()
    finally:
        v.close_browser()
        if len(current_holdings) == 0:
            return rInternalServerError

    return jsonify(current_holdings)

@app.route("/vanguard/open_orders")
def vanguard_open_orders():
    raise NotImplementedError

@app.route("/vanguard/available_funds")
def vanguard_available_funds():
    raise NotImplementedError

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
