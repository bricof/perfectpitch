from flask import Flask, make_response
from pandas import *
import numpy as np
import json
import perfectpitch

app = Flask(__name__)

@app.route('/')
def index():
    return make_response(open('demo-web.html').read())

@app.route('/api/<int:id>')
def api(id):

    p, amp, frq, signal = perfectpitch.get_audio()
    
    data = [ DataFrame({'x': range(len(signal)), 'y': signal.tolist() }), 
             DataFrame({'x': frq.tolist(), 'y': amp.tolist() })
           ]
    
    jsout = json.dumps([ json.loads(data[0].to_json(orient='records')), 
                         json.loads(data[1].to_json(orient='records')),
                         p ])
    
    return make_response(jsout)

if __name__ == '__main__':
    app.run(debug = True)
