from flask import Flask, jsonify

import config
from models import session, Result

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return "<center>alhamdulillah... its working!</center>"
    
@app.route('/<int:r>')
def roll(r):
    s = session.query(Result).filter_by(roll=r).first()
    if s:
        return jsonify({"messages": [{"text": "{}".format(s.res)}]})
    else:
        return jsonify({"messages": [{"text": "result not found"}]})

if __name__ == '__main__':
    app.run()
    
