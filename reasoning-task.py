import os
import glob
import socket
import shutil
import validators
import subprocess
import requests, json
from random import random
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, flash, redirect, url_for, make_response, jsonify

# App wide variables
UPLOAD_FOLDER = "uploads"
JSON_TEMPLATE = "json_template.html"
FORM_TEMPLATE = "form_template.html"
ALLOWED_EXTENSIONS = {"n3", "ttl", "nt"}

# Create app with CORS enabled
app = Flask(__name__)
CORS(app)

# Set app configuration
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["JSON_TEMPLATE"] = JSON_TEMPLATE
app.config["FORM_TEMPLATE"] = FORM_TEMPLATE
app.secret_key = "super secret key" # ?

# Function to check filenames
def allowed_file(filename):
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def valid_url(url):
#     valid = validators.url(url)
#     if valid == True:
#         return True
#     else:
#         return False

# Function to check URLs
def valid_url(url):
    return validators.url(url) # Same as above: returns True if valid :)

# Function to process 'files' POSTed as JSON data
def create_input_files(input_list, target_container, error_container, message_part): 
    for file in input_list:
        # Check if file extension is allowed (either .ttl of .n3)
        if file and allowed_file(file["file"]):
            # Allow secure filenames only
            filename = secure_filename(file["file"])
            # Append data to data_input
            target_container.append(filename)
            # Create and save file with content
            f = open(os.path.join(UPLOAD_FOLDER, filename), "w")
            f.write(file["content"])
            f.close()
        else:
            list_of_files = [str(s) for s in ALLOWED_EXTENSIONS]
            error_container.append("{}: upload {} files only".format(message_part, "/".join(list_of_files)))

# Function to process files POSTed in FileList
def take_input_files(input_list, target_container, error_container, message_part): 
    for file in input_list:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Append data to data_input
            target_container.append(filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            error_container.append("{}: upload {} files only".format(message_part, "/".join(list_of_files)))

# Function to create URL list based on POSTed JSON data 
def create_input_urls(input_list, target_container, error_container, message):
    for url in input_list:
        if valid_url(url):
            target_container.append(url)
        else:
            error_container.append("{}: {} is invalid".format(message, url))

# Function to use the EYE reasoner
def reason(data_input, rule_input, query_input, **kwargs):
    # Enter uploads directory
    os.chdir(UPLOAD_FOLDER)

    # Create date strings for final reasoning output file
    now = datetime.now()
    now_str1 = "#Execution date {} \r\n".format(now.strftime("%Y-%m-%d %H:%M"))
    now_str2 = now.strftime("reasoning_%Y%m%d%H%M")

    # Reason with the EYE reasoner
    process = subprocess.run(
        ["/opt/eye/bin/eye.sh",
        "--nope"]
        + data_input
        + rule_input
        + query_input,
        universal_newlines=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)

    # If run successfully
    if process.returncode == 0:
        # Leave uploads directory
        os.chdir("..")
        # Delete upload folder and files
        shutil.rmtree(UPLOAD_FOLDER)

        # Return output
        response = make_response(now_str1 + process.stdout)
        response.headers["Content-type"] = "text/turtle"
        response.headers["Content-Disposition"] = "inline; filename={}.ttl".format(now_str2)

        # Return results as turtle file
        return response

    else:
        # Leave uploads directory
        os.chdir("..")
        # Delete upload folder and files
        shutil.rmtree(UPLOAD_FOLDER)

        # return output
        if kwargs["gui"] == True: 
            return render_template(kwargs["template"], output=process.stderr)
        else: 
            return jsonify(process.stderr)


@app.route("/", methods=["POST","GET"])
def reasoningtask():

    # POST
    if request.method == "POST":
        
        gui = False

        if "gui" in request.args:

            gui = True

            if request.args.get("gui") == "form":
                TEMPLATE = FORM_TEMPLATE

            if request.args.get("gui") == "json":
                TEMPLATE = JSON_TEMPLATE
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        #######################################
        ########### if POST is JSON ###########
        #######################################
        if request.is_json:

            # Take the posted json data
            req = request.get_json()

            # List for error messages
            check_parts = []

            # Check JSON structure !!!

            # Check if there are data files or URLs
            if not req["data"]["files"] and not req["data"]["urls"]: 
                check_parts.append("No data files or URLs posted")
            else:
                data_files = req["data"]["files"]
                data_urls = req["data"]["urls"]

            # Check if there are rule files or URLs
            if not req["rules"]["files"] and not req["rules"]["urls"]: 
                check_parts.append("No rule files or URLs posted")
            else:
                rule_files = req["rules"]["files"]
                rule_urls = req["rules"]["urls"]

            # Query files are optional
            query_files = req["queries"]["files"]
            query_urls = req["queries"]["urls"]


            # If errors, return message(s)
            if check_parts:
                if gui == True:
                    return "\n".join(check_parts)
                else:  
                    return jsonify("EYE Reasoner: " + " | ".join(check_parts))

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

            # Exit if there are forbidden files
            if check_names:
                shutil.rmtree(UPLOAD_FOLDER)
                if gui == True: 
                    return "\n".join(check_names)
                else: 
                    return jsonify("EYE Reasoner: " + " | ".join(check_names))

            # Exit if there are invalid URLs
            if check_urls:
                shutil.rmtree(UPLOAD_FOLDER)
                if gui == True: 
                    return "\n".join(check_urls)
                else: 
                    return jsonify("EYE Reasoner: " + " | ".join(check_urls))

            if query_input:
                # Add the needed parameter for the reasoner
                query_input.insert(0, "--query")

            ###################
            # START REASONING #
            ###################
            if gui:
                reasoning = reason(data_input, rule_input, query_input, gui=gui, template=TEMPLATE)
            else:
                reasoning = reason(data_input, rule_input, query_input)

            return reasoning

        #######################################
        ######### if POST is FileList #########
        #######################################
        else: 

            check_parts = []
            # Fact parts
            if "upl_data" not in request.files:
                check_parts.append("No data files form part")

            if "data_list" not in request.form:
                check_parts.append("No data urls form part")

            # Rule parts
            if "upl_rules" not in request.files:
                check_parts.append("No rule files form part")

            if "rule_list" not in request.form:
                check_parts.append("No rule urls form part")

            # Query files are optional

            if check_parts:
                # There are no data or rule parts
                if gui == True: 
                    return render_template(FORM_TEMPLATE, output="\n".join(check_parts))
                else: 
                    return "EYE Reasoner: " + " | ".join(check_parts)

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
                if gui == True: 
                    return render_template(FORM_TEMPLATE, output="\n".join(check_files))
                else: 
                    return "EYE Reasoner: " + " | ".join(check_files)
            else:
                # Facts and rules are present
                check_names = []
                check_urls = []

                data_input = []
                rule_input = []
                query_input = []

                # Handle data files if present
                if data_files[0]:
                    take_input_files(data_files, data_input, check_names, "Data files") 

                # Handle data urls if present
                if data_urls:
                    create_input_urls(data_urls, data_input, check_urls, "Data URLs")

                # Handle rule files if present
                if rule_files[0]: 
                    take_input_files(rule_files, rule_input, check_names, "Rule files")

                # Handle rule urls if present
                if rule_urls:
                    create_input_urls(rule_urls, rule_input, check_urls, "Rule URLs")

                # Handle query files if present
                if query_files[0]:
                    take_input_files(query_files, query_input, check_names, "Query files")

                # Handle query urls if present
                if query_urls:
                    create_input_urls(query_urls, query_input, check_urls, "Query URLs")

                # Exit if there are forbidden files
                if check_names:
                    if gui == True: 
                        return render_template(FORM_TEMPLATE, output="\n".join(check_names))
                    else: 
                        return "EYE Reasoner: " + " | ".join(check_names)

                # Exit if there are invalid URLs
                if check_urls:
                    if gui == True: 
                        return render_template(FORM_TEMPLATE, output="\n".join(check_urls))
                    else:
                        return "EYE Reasoner: " + " | ".join(check_names)

                if query_input:
                    # Add the needed parameter for the reasoner
                    query_input.insert(0, "--query")

                ###################
                # START REASONING #
                ###################
                if gui:
                    reasoning = reason(data_input, rule_input, query_input, gui=gui, template=TEMPLATE)
                else:
                    reasoning = reason(data_input, rule_input, query_input)

                return reasoning

    # GET
    else:
        gui_type = request.args.get("gui", default = "form", type = str)
        if gui_type == "json":
            return render_template(JSON_TEMPLATE)
        else: 
            return render_template(FORM_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50001, debug=True)
