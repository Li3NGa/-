from flask import jsonify


def health_response():
    return jsonify({"status": "ok"})
