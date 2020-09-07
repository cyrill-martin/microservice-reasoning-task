import os
import glob
import socket
import validators
import subprocess
import requests, json
from random import random
from flask_cors import CORS
from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"n3", "ttl"}

app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "super secret key"

# Check filename
def allowed_file(filename):
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def valid_url(url):
#     valid = validators.url(url)
#     if valid == True:
#         return True
#     else:
#         return False

def valid_url(url):
    return validators.url(url) # Same as above

def create_input_files(input_list, target_container, error_container, message): 
    for file in input_list: 
        if file and allowed_file(file["file"]):
            filename = secure_filename(file["file"])
            # Append data to data_input
            target_container.append(filename)

            f = open(os.path.join(app.config["UPLOAD_FOLDER"], filename), "w")
            f.write(file["content"])
            f.close()

            # file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            error_container.append("{}: upload .ttl and/or .n3 files only".format(message))

def create_input_urls(input_list, target_container, error_container, message):
    for url in input_list:
        if valid_url(url):
            target_container.append(url)
        else:
            error_container.append("{}: {} is invalid".format(message, url))


@app.route("/", methods=["POST","GET"])
def reasoningtask():
    template = "reasoning-task.html"

    # POST
    if request.method == "POST":

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # if POST is JSON
        if request.is_json:

            # Take the posted json data
            req = request.get_json()

            # List for error messages
            check_parts = []

            # Check if there are data files or URLs
            if not req["data"]["files"] and not req["data"]["urls"]: 
                check_parts.append("No data files selected or URLs listed")
            else:
                data_files = req["data"]["files"]
                data_urls = req["data"]["urls"]

            # Check if there are rule files or URLs
            if not req["rules"]["files"] and not req["rules"]["urls"]: 
                check_parts.append("No rule files selected or URLs listed")
            else:
                rule_files = req["rules"]["files"]
                rule_urls = req["rules"]["urls"]

            # Query files are optional
            query_files = req["queries"]["files"]
            query_urls = req["queries"]["urls"]

            # If errors, return message(s)
            if check_parts:
                return jsonify("\n".join(check_parts))

            # Containers for input files
            data_input = []
            rule_input = []
            query_input = []

            # Containers for file and url validation
            check_names = []
            check_urls = []

            # Handle data files if present
            if data_files:
                create_input_files(data_files, data_input, check_names, "Data files")

            # Handle data urls if present
            if data_urls:
                create_input_urls(data_urls, data_input, check_urls, "Data URLs")

            # Handle rule files if present
            if rule_files:
                create_input_files(rule_files, rule_input, check_names, "Rule files")

            # Handle rule urls if present
            if rule_urls:
                create_input_urls(rule_urls, rule_input, check_urls, "Rule URLs")

            # Handle query files if present
            if query_files:
                create_input_files(query_files, query_input, check_names, "Query files")

            # Handle query urls if present
            if query_urls:
                create_input_urls(query_urls, query_input, check_urls, "Query URLs")









            return jsonify(req)

        # if POST if FileObject
        else: 
            #############################
            # CHECK FOR FILES AND/OR URLs
            #############################

            check_parts = []
            # Fact parts
            if "upl_data" not in request.files:
                check_parts.append("No data files part")

            if "data_list" not in request.form:
                check_parts.append("No data urls part")

            # Rule parts
            if "upl_rules" not in request.files:
                check_parts.append("No rule files part")

            if "rule_list" not in request.form:
                check_parts.append("No rule urls part")

            # Query files are optional

            if check_parts:
                # There are no data or rule parts
                return render_template(template, output="\n".join(check_parts))

            # Get the file lists
            data_files = request.files.getlist("upl_data")
            rule_files = request.files.getlist("upl_rules")
            query_files = request.files.getlist("upl_queries")

            # Get the url lists. Split by line (i.e. \r\n) and remove any empty lines (i.e. "")
            data_urls = (request.form["data_list"]).split("\r\n")
            data_urls = list(filter(("").__ne__, data_urls))

            rule_urls = (request.form["rule_list"]).split("\r\n")
            rule_urls = list(filter(("").__ne__, rule_urls))

            query_urls = (request.form["query_list"]).split("\r\n")
            query_urls = list(filter(("").__ne__, query_urls))

            check_files = []
        
            if not data_files[0] and not data_urls:
                # Fact files or urls are missing
                check_files.append("No data files selected or URLs listed")

            if not rule_files[0] and not rule_urls:
                # Rule files or urls are missing
                check_files.append("No rule files selected or URLs listed")

            # Query files are optional

            if check_files:
                # Fact and/or rule files and/or urls are missing
                return render_template(template, output="\n".join(check_files))
            else:
                # Facts and rules are present
                check_names = []
                name_error = "upload .ttl and/or .n3 files only"
                check_urls = []

                data_input = []
                rule_input = []
                query_input = []

                # Handle data files if present
                if data_files[0]:
                    # Handle data files
                    for file in data_files:
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            # Append data to data_input
                            data_input.append(filename)
                            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                        else:
                            check_names.append("Data files: %s" % name_error)

                # Handle data urls if present
                if data_urls:
                    for url in data_urls:
                        if valid_url(url):
                            data_input.append(url)
                        else:
                            check_urls.append("Data urls: %s is invalid" % url)

                # Handle rule files if present
                if rule_files[0]: 
                    # Handle rule files
                    for file in rule_files:
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            # Append rule to rule_input
                            rule_input.append(filename)
                            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                        else:
                            check_names.append("Rule files: %s" % name_error)

                # Handle rule urls if present
                if rule_urls:
                    for url in rule_urls:
                        if valid_url(url):
                            rule_input.append(url)
                        else:
                            check_urls.append("Rule urls: %s is invalid" % url)

                # Handle query files if present
                if query_files[0]:
                    # Handle query files
                    for file in query_files:
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            # Append query to query_input
                            query_input.append(filename)
                            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                        else:
                            check_names.append("Query files: %s" % name_error)

                # Handle query urls if present
                if query_urls:
                    for url in query_urls:
                        if valid_url(url):
                            query_input.append(url)
                        else:
                            check_urls.append("Query urls: %s is invalid" % url)

                if check_names:
                    return render_template(template, output="\n".join(check_names))

                if check_urls:
                    return render_template(template, output="\n".join(check_urls))

                #################
                # START REASONING
                #################

                if query_input:
                    # Add the needed parameter for the reasoner
                    query_input.insert(0, "--query")

                # Enter uploads directory
                os.chdir("uploads")
                
                # Execution date Mi Apr 8 14:52:01 CEST 2020
                now = datetime.now()
                now_str = "#Execution date %s \r\n" % now.strftime("%Y-%m-%d %H:%M")
                now_str2 = now.strftime("reasoning_%Y%m%d%H%M")

                process = subprocess.run(
                    ["/opt/eye/bin/eye.sh",
                    "--nope"]
                    + data_input
                    + rule_input
                    + query_input,
                    universal_newlines=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)

                if process.returncode == 0:
                    # If run successfully, delete the uploaded files
                    files = glob.glob("*")
                    for f in files:
                        os.remove(f)
                    # Leave uploads directory
                    os.chdir("..")

                    # Return output
                    response = make_response(now_str + process.stdout)
                    response.headers["Content-type"] = "text/turtle"
                    response.headers["Content-Disposition"] = "inline; filename=%s.ttl" % now_str2

                    return response

                else:
                    # Delete uploaded files
                    files = glob.glob("*")
                    for f in files:
                        os.remove(f)
                    # Leave uploads directory
                    os.chdir("..")

                    return render_template(template, output=process.stderr)

    # GET
    else:
        return render_template(template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50001, debug=True)

