from flask import Flask, request, jsonify
app = Flask(__name__)

from vanguard import Vanguard, config
from users import Users

# Users Routes

@app.route("/register", methods=['POST'])
def register():
	# Register a user profile (user, password)
	username = request.form.get("username")
	password = request.form.get("password")
	email = request.form.get("email")
	if None in [username, password, email]:
		return "Please provide username, password and email", 400

	try:
		Users.register_user(username, email, password)
		user = Users.find_user(username)
		user = Users.clean_user(user)
		return jsonify(user)
	except RuntimeError as e:
		print "ERROR:", e
		return "Internal Server Error", 500

@app.route("/my_details", methods=['GET'])
def user_details():
	username = request.form.get("username")
	password = request.form.get("password")
	if None in [username, password]:
		return "Please provide username and password", 400

	try:
		# TODO: Auth the user, idiot
		user = Users.find_user(username)
		if user is None:
			return "Not found", 404
		user = Users.clean_user(user)
		return jsonify(user)
	except RuntimeError as e:
		print "ERROR:", e
		return "Internal Server Error", 500

@app.route("/enroll", methods=['POST'])
def enroll_in_service():
	# Lets assume for now the only service we support is vanguard
	# For that reason, all service info validation logic shall be in this sole handler

	# required: service_name, username, password
	request_data = request.get_json(force=True)

	username = request_data.get("username")
	password = request_data.get("password")
	if None in [username, password]:
		return "Please provide username and password", 400

	if Users.auth_user(username, password) is not True:
		return "Authorization failed", 401

	service_info = request_data.get("service_info")
	if service_info is None:
		return "Please provide service information for enrollment", 400

	service_name = service_info.get("service_name")
	username = service_info.get("username")
	password = service_info.get("password")
	if None in [service_name, username, password]:
		return "Please provide service information for enrollment", 400

	try:
		Users.enroll_in_service(username, service_info)
	except RuntimeError as e:
		print "ERROR:", e
		return "Internal Server Error", 500

	return "OK"

@app.route("/register_security_answer", methods=['POST'])
def register_security_answer():
	# auth user
	request_data = request.get_json(force=True)

	username = request_data.get("username")
	password = request_data.get("password")
	if None in [username, password]:
		return "Please provide username and password", 400

	if Users.auth_user(username, password) is not True:
		return "Authorization failed", 401

	service_info = request_data.get("service_info")
	if service_info is None:
		return "Please provide service information for security question registration", 400

	service_name = service_info.get("service_name")
	question = service_info.get("question")
	answer = service_info.get("answer")
	if None in [service_name, question, answer]:
		return "Please provide service information for security question registration", 400

	try:
		Users.register_security_answer(username, service_name, question, answer)
	except RuntimeError as e:
		print "ERROR:", e
		return "Internal Server Error", 500

	return "OK"

# Vanguard Routes

@app.route("/total")
def json():
	v = Vanguard()
	v.login(config.TEST_USER, config.TEST_PASSWORD)

	question = v.get_security_question()
	answer = config.TEST_SECURITY_QUESTIONS.get(question)
	v.answer_security_question(answer)

	total_assets = v.get_total_assets()
	res = {
		"total": total_assets
	}

	v.close_browser()
	return jsonify(res)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
