import os
from logging.config import dictConfig
from flask import Flask, request, jsonify
import requests


# Logs configuration
dictConfig({
    "version": 1,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] %(module)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "console"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
})


app = Flask(__name__)


@app.route("/")
def index():
    app.logger.info("Request to index action")
    return "https://www.github.com/daleal/executor/api"


@app.route("/execute", methods=["POST"])
def execute():
    try:
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

        # Execute the code
        response = requests.post(
            f"{os.environ['EXECUTOR_URL']}/execute",
            json=data
        )
        response_code = response.status_code
        response_body = response.json()

        # Log response
        if response_code == 200:
            app.logger.info(
                f"Code executed "
                f"{'correctly' if response_body['success'] else 'incorrectly'}"
                f" with response code {response_code} and "
                f"output:\n{response_body['response']}"
            )
        else:
            app.logger.info(
                f"Code executed incorrectly with response "
                f"code {response_code}"
            )

        # Return executed output
        return jsonify({
            "success": True,
            "response": response_body["response"]
        }), 200
    except Exception as err:
        # Log error
        app.logger.error(err)

        # Return error
        return jsonify({
            "success": False,
            "response": "Something went wrong!"
        }), 500
