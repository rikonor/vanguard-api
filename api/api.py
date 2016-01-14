from flask import Flask, request, jsonify
app = Flask(__name__)

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
	print config
	res = dict(name="Or", age=27)
	return jsonify(res)

if __name__ == "__main__":
	app.run()
