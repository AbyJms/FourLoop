from flask import Flask, request, jsonify

app = Flask(__name__)

# Example user loader function
def load_user(user_id):
    # Replace this with actual user lookup logic
    return {"id": user_id, "name": "Test User"}

# Register route
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    # Replace with actual registration logic
    username = data.get("username")
    password = data.get("password")
    return jsonify({"message": f"User {username} registered successfully!"})

# Login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    # Replace with actual login check
    return jsonify({"message": f"User {username} logged in successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
