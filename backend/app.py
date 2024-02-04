from flask import Flask, request, jsonify
import mysql.connector
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="your_mysql_host",
    user="your_mysql_user",
    password="your_mysql_password",
    database="your_database_name",
)


@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        name = data["name"]
        email = data["email"]
        password = data["password"]

        # Insert user data into the database
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password),
        )
        db.commit()
        cursor.close()

        # Generate JWT token
        token_payload = {
            "name": name,
            "email": email,
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        auth_token = jwt.encode(token_payload, "your_secret_key", algorithm="HS256")

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "token": auth_token.decode("utf-8"),
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": "Failed to create user"}), 500


if __name__ == "__main__":
    app.run(debug=True)
