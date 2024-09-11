#!/usr/bin/env python3
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()  # Instantiate the Auth object


@app.route("/", methods=["GET"])
def welcome():
    """Return a JSON response with a welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Register a user via POST request with 'email' and 'password'"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:  # If the user already exists, raise an error
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
