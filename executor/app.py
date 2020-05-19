import os
import sys
from io import StringIO
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    app.logger.info("Request to index action")
    return "https://www.github.com/daleal/executor/executor"


@app.route("/execute", methods=["POST"])
def execute():
    try:
        # Store reference to stdout
        old_stdout = sys.stdout

        app.logger.info("POST request to execute action")
        data = request.get_json(force=True)

        if set(["content"]) != set(data.keys()):
            app.logger.info(f"Invalid request body keys {data.keys()}")
            return jsonify({
                "success": False,
                "response": "Something went wrong!"
            }), 400

        # Log code
        app.logger.info(
            f"Executing the following code:\n{data['content']}")

        # Change stdout
        response = StringIO()
        sys.stdout = response

        # Execute the code
        exec(data["content"], {"__name__": "__main__"})

        # Restore stdout
        sys.stdout = old_stdout
        response_content = response.getvalue()

        # Log response
        app.logger.info(f"Code executed with output:\n{response_content}")

        # Return executed output
        return jsonify({"success": True, "response": response_content}), 200
    except Exception as err:
        # Restore stdout
        sys.stdout = old_stdout

        # Log error
        app.logger.error(err)

        # Return error
        return jsonify({"success": False, "response": err}), 500
