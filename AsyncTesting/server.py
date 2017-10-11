from flask import Flask, request
import time
app = Flask(__name__)


@app.route('/some_endpoint')
def some_endpoint():
    time.sleep(int(request.args.get('delay')) * 0.001)
    return '200'
