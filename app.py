from flask import Flask, request, jsonify, Response
import os
import logging
import time
import xml.etree.ElementTree as ET

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
    
    # Add query parameters if present
    if request.args:
        response_data["query_params"] = dict(request.args)
    
    # Add request body if present
    if request.is_json:
        response_data["body"] = request.get_json()
    elif request.data:
        try:
            response_data["body"] = request.data.decode('utf-8')
        except:
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

@app.route('/Common/CurrencyExchangeRate/Get/2.1', methods=['GET', 'POST'])
def currency_exchange_rate():
    """SOAP endpoint for currency exchange rate"""
    logger.info(f"Currency exchange rate request received - Method: {request.method}")
    
     
    if request.method == 'GET':
        return jsonify({
            "endpoint": "/Common/CurrencyExchangeRate/Get/2.1",
            "methods_allowed": ["GET", "POST"],
            "description": "SOAP endpoint for currency exchange rate",
            "test_command": "curl -X POST http://172.16.20.52/Common/CurrencyExchangeRate/Get/2.1 -H 'Content-Type: text/xml' -d '<?xml version=\"1.0\"?><test/>'",
            "note": "Use POST method with XML content for SOAP response"
        }), 200
    
    
    if request.data:
        logger.info(f"Request body: {request.data.decode('utf-8')}")
    
    soap_response = '''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns27="urn://co-opbank.co.ke/TS/Finacle/CurrencyExchangeRateList.1.0" xmlns:head="urn://co-opbank.co.ke/CommonServices/Data/Message/MessageHeader" xmlns:tns25="urn://co-opbank.co.ke/BS/Common/BSCurrencyExchangeRate.2.0" xmlns:ns10="urn://co-opbank.co.ke/Banking/CanonicalDataModel/ExchangeRate/2.0">
   <soapenv:Header>
      <head:ResponseHeader xmlns:tns26="urn://co-opbank.co.ke/BS/Account/CurrencyExchangeRate/Get/2.0" xmlns:tns3="urn://co-opbank.co.ke/CommonServices/Data/Common">
         <tns3:CorrelationID>975b1168-564b-4b67-a983-8c8f327de9b4</tns3:CorrelationID>
         <head:MessageID>3b319494-b302-4f05-9f18-2c3c94671e5c</head:MessageID>
         <head:StatusCode>S_001</head:StatusCode>
         <head:StatusDescription>Success</head:StatusDescription>
         <head:StatusMessages>
            <head:MessageCode>Y</head:MessageCode>
            <head:MessageDescription>SUCCESS</head:MessageDescription>
         </head:StatusMessages>
      </head:ResponseHeader>
   </soapenv:Header>
   <soapenv:Body>
      <tns25:ExchangeRateResponse>
         <tns25:ExchangeRate>13.33356</tns25:ExchangeRate>
         <tns25:FromCurrency>TZS</tns25:FromCurrency>
         <tns25:ToCurrency>KES</tns25:ToCurrency>
         <tns25:ConvertedAmount>14999.8</tns25:ConvertedAmount>
         <tns25:MultiplyDivide>D</tns25:MultiplyDivide>
      </tns25:ExchangeRateResponse>
   </soapenv:Body>
</soapenv:Envelope>'''
    
    return Response(soap_response, mimetype='text/xml'), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)