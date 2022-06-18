#importing libraries
import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

#creating instance of the class
app=Flask(__name__)

#to tell flask what url should trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')
    #return "Hello World"

#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,8)
    loaded_model = pickle.load(open("model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

def ValuePredictor2(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,8)
    loaded_model = pickle.load(open("model.pkl","rb"))
    result2 = loaded_model.predict_proba(to_predict)
    return result2


@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        result2 = ValuePredictor2(to_predict_list)
        result2 = result2.tolist()
        if int(result)==1:
            
            prediction="%"+str(int(100* result2[0][1]))+" ihtimalle diyabetsin,"
            prediction2="bir doktora görünmelisin."

        else:
            prediction="%"+str(int(100* result2[0][0]))+" ihtimalle sağlıklısın."
            prediction2=""
            
        return render_template("result.html",prediction=prediction,prediction2=prediction2)

if __name__ == "__main__":
	app.run(debug=True)