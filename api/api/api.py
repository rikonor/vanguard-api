from flask import Flask, request, jsonify
app = Flask(__name__)

from vanguard import Vanguard, config
import traceback

# Users Routes

@app.route("/register")
def register():
	# Register a user profile (user, password)
	pass

@app.route("/register_security_answer")
def register_security_answer():
	# given user, pass, and security q and a, register it
	pass

# Vanguard Routes

@app.route("/total")
def json():
	try:
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
	except Exception as e:
		print "Failed"
		traceback.print_exc()

if __name__ == "__main__":
	app.run()
