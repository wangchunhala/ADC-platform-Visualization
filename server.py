#!/usr/bin/env python
#encoding=utf-8

import sys
from flask import Flask, render_template, request, url_for, Response
import json
###############
# python script
###############

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',result=404)

@app.route('/py_login',methods=['GET','POST'])
def py_login():
    if request.method == 'GET':

        print(request.form)
        txtname = request.args.get('username')
        txtpswd = request.args.get('userpswd')

        if(txtname=="neo4j" and txtpswd=="123"):
            return "SUCCESS!"  # get可以到这里
            print(url_for('/index1'))
            # return redirect(url_for('/testhtm'))
        else:
            return "FAIL!"

@app.route('/index1')
def f_infor():
    return render_template('index1.html')



from demo import demo1
app.register_blueprint(demo1.mod1)
from demo import demo2
app.register_blueprint(demo2.mod2)
from demo import demo3
app.register_blueprint(demo3.mod3)

if __name__ == "__main__":
    app.run(debug = True)