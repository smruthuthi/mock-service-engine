from flask import Flask, request, jsonify
import os
import logging
import time

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def handle_all():
    """Handle all HTTP methods on root endpoint"""
    response_data = {
        "status": "success",
        "message": "Request processed successfully",
        "method": request.method,
        "path": request.path,
        "headers": dict(request.headers),
        "timestamp": time.time(),
        "service_version": os.getenv('SERVICE_VERSION', '1.0.0')
    }

    if request.args:
        response_data["query_params"] = dict(request.args)

    if request.is_json:
        response_data["body"] = request.get_json()
    elif request.data:
        try:
            response_data["body"] = request.data.decode('utf-8')
        except UnicodeDecodeError:
            response_data["body"] = str(request.data)

    logger.info(f"Request received: {request.method} {request.path}")
    return jsonify(response_data), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "service": "mock-service"
    }), 200


@app.route('/echo', methods=['POST'])
def echo():
    """Echo endpoint that returns the request body"""
    data = request.get_json() if request.is_json else request.data.decode('utf-8')
    return jsonify({
        "echo": data,
        "timestamp": time.time()
    }), 200


@app.route('/status/<int:code>', methods=['GET'])
def custom_status(code):
    """Return custom status code"""
    return jsonify({
        "status_code": code,
        "message": f"Returning status {code}",
        "timestamp": time.time()
    }), code


@app.route('/delay/<int:seconds>', methods=['GET'])
def delayed_response(seconds):
    """Simulate a delayed response"""
    if seconds > 10:  # Limit delay to 10 seconds
        seconds = 10
    time.sleep(seconds)
    return jsonify({
        "delay_seconds": seconds,
        "message": f"Response delayed by {seconds} seconds",
        "timestamp": time.time()
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)