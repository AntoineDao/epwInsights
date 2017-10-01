import os
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from werkzeug.utils import secure_filename

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from windrose import *
import json
import EpwInsights

from os.path import join, dirname, realpath
UPLOAD = '\epw\uploads'
UPLOAD_FOLDER = join(dirname(realpath(__file__)), UPLOAD)

UPLOAD_FOLDER = "my_site\epw\uploads"

ALLOWED_EXTENSIONS = set(['epw'])

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def makefig(width, height):
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2*np.pi*t)
    fig = plt.figure(figsize=(width,height))
    plt.plot(t,s)
    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    json01 = json.dumps(mpld3.fig_to_dict(fig))

    return json01


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename))
            #return render_template("home.html")
            return redirect(url_for('epwviewer',epwfile=filename))
    return render_template("upload.html")
    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route("/epwviewer")
def epwviewer():
    from epwvisuals import *
    epwname = request.args.get("epwfile")
    epwpath = os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']),epwname)
    #html = "<h1>" + epwpath + "</h1>"

    output = print_epw_temp(epwpath)
    html = render_template('figure.html', city = epw_city(epwpath),input1=output,input2=makefig(3,3),input3=makefig(5,7), htmlfig = output)
    return(html)


@app.route("/figure")
def embed():

    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2*np.pi*t)
    fig = plt.figure(figsize=(2,2))
    plt.plot(t,s)
    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    output = mpld3.fig_to_html(fig)

    html = render_template('figure.html', input1=makefig(1,1),input2=makefig(3,3),input3=makefig(5,7), htmlfig = output)
    return html


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__ =="__main__":
    app.run(debug=True)
