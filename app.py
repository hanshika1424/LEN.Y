from flask import Flask, request, jsonify  #Used AI to use these functions
from verifier import full_verification
app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response
@app.route("/verify", methods=["POST"])
def verify():
    """
    This function runs every time the frontend submits a message to check.
    """
    request_data = request.get_json()
    try:
        message_body = request_data.get("message_body", "") #Self Written Code
        sender_id = request_data.get("sender_id", "")
        phone_number = request_data.get("phone_number", "")
        timestamp = request_data.get("timestamp", "")

        # These three are OPTIONAL - they may not always be extractable
        # from every message, so we allow them to be empty/missing.
        message_id = request_data.get("message_id", None)
        customer_id = request_data.get("customer_id", None)
        department = request_data.get("department", None)

        # ---- STEP 1: Basic validation ----
        if message_body.strip() == "" or sender_id.strip() == "":
            return jsonify({
                "error": "message_body and sender_id are required fields."
            }), 400   # 400 = HTTP code for "bad request" (ADVANCED, web concept)

        # ---- STEP 2: Call the verification logic (verifier.py) ----
        # This is just a normal function call, passing our variables in
        # as arguments.
        result = full_verification(
            message_body, sender_id, phone_number, timestamp,
            message_id, customer_id, department,
        )

        # ---- STEP 3: Send the result back to the frontend ----
        # jsonify() converts our Python dictionary into JSON text that
        # JavaScript can understand. (ADVANCED: JSON conversion)
        return jsonify(result)

    except Exception as error:
        # Catches ANY unexpected error so the server doesn't crash,
        # and reports it back instead of just failing silently.
        return jsonify({
            "error": "Something went wrong while verifying the message.",
            "details": str(error)
        }), 500   # 500 = HTTP code for "server error"


# ---------- SIMPLE TEST ROUTE ----------
# Visiting http://localhost:5000/ in a browser should show this message.
# Useful to quickly check the backend is actually running.
@app.route("/", methods=["GET"])
def home():
    return "Zero Trust backend is running."


# ---------- RUN THE SERVER ----------
# when the file is executed directly (not when imported elsewhere).
if __name__ == "__main__":
    # debug=True auto-restarts the server when you save changes - very
    # useful while developing, should be turned off for a real deployment.
    app.run(debug=True, port=5000)