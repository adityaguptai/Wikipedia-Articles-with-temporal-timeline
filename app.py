from flask import Flask,render_template, request,jsonify
from flask_restful import reqparse
import json
#ML imports
import main_ml as ml

app = Flask(__name__) #__name__ kind of a placeholder for current module

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/ml_engine',methods=['POST'])
def ml_engine():
    # data = json.loads(request.data)
    parser = reqparse.RequestParser()
    parser.add_argument("name")
    parser.add_argument('nsent')
    args = parser.parse_args()
    print(args['name'])
    ml_data = ml.timeline_sentences(str(args['name']),int(args['nsent']))
    # ml_data = ml.timeline_sentences("Gandhi")
    print(ml_data)
    # return jsonify(json.dumps({"items":ml_data}))
    return jsonify(json.dumps(str(ml_data)))

if __name__ == '__main__': #It means the above script gets executed
    app.run(debug=True)
