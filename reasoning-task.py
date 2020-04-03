import os
import glob
import socket
import subprocess
import requests, json
from random import random
from flask_cors import CORS
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'n3', 'ttl'}


app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

# Check filename
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/reasoning-task", methods=["POST","GET"])
def reasoningtask():
    template = "reasoning-task.html"

    # POST
    if request.method == "POST":

        ###############################
        # CHECK FOR FILES AND/OR URLs #
        ###############################

        if "upl_facts" not in request.files:
            return render_template(template, output="No fact files uploaded")

        if "upl_rules" not in request.files:
            return render_template(template, output="No rule files uploaded")

        fact_files = request.files["upl_facts"]
        rule_files = request.files["upl_rules"]
        query_file = request.files["upl_query"]

        if fact_files.filename == "":
            return render_template(template, output="No fact files selected")

        if rule_files.filename == "":
            return render_template(template, output="No rule files selected")
    # GET
    else:
        return render_template(template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

