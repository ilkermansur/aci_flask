from dotenv import load_dotenv
import os
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
from aci_functions import login, create_tenant, create_vrf, create_bd, create_app, create_epg, create_bulk
import json
import requests
import urllib3
import time
import re
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)

load_dotenv()  # This loads the environment variables from .env

# Now you can access the environment variables using os.getenv
default_host = os.getenv('HOST')
default_username = os.getenv('USERNAME')
default_password = os.getenv('PASSWORD')

@app.route ("/")
def instruction ():
   return render_template ("instructions.html")

@app.route("/crt_tenant", methods = ["POST", "GET"])
def crt_tenant():
     
    if request.method == "POST":
        # get token 
        host = request.form["host"]
        username = request.form["username"]
        password = request.form["password"]
        # create tenant
        tn_name = request.form["tn_name"]
        tn_alias = request.form["tn_alias"]
        tn_desc = request.form["tn_desc"]

        if host and username and password and tn_name and tn_alias and tn_desc:

            token = login(ip=host, username=username, password=password)
            result = create_tenant(
                                    ip=host,
                                    tn_name=tn_name,
                                    tn_alias=tn_alias,
                                    tn_desc=tn_desc,
                                    token=token
                                    )

            return render_template ("crt_tenant.html", result=result)
        else:
            return render_template ("crt_tenant.html", host=default_host, username=default_username, password=default_password)
    else:
        return render_template ("crt_tenant.html", host=default_host, username=default_username, password=default_password)

@app.route("/create_vrf", methods = ["POST", "GET"])
def crt_vrf():

    if request.method == "POST" :
        # get token
        host = request.form["host"]
        username = request.form["username"]
        password = request.form["password"]
        # create VRF
        tn_name = request.form["tn_name"]
        vrf_name = request.form["vrf_name"]
        vrf_alias = request.form["vrf_alias"]
        vrf_desc = request.form["vrf_desc"]

        if host and username and password and tn_name and vrf_name and vrf_alias and vrf_desc:
            token = login(ip=host, username=username, password=password)
            result = create_vrf (
                                    ip = host,
                                    tn_name=tn_name,
                                    vrf_name=vrf_name,
                                    vrf_alias=vrf_alias,
                                    vrf_desc=vrf_desc,
                                    token=token
                                    )

            return render_template ("crt_vrf.html", result=result)
        else:
            return render_template ("crt_vrf.html")
    else:
        return render_template ("crt_vrf.html")


@app.route("/create_bd", methods = ["POST", "GET"])
def crt_bd():
        if request.method == "POST" :
        # get token
            host = request.form["host"]
            username = request.form["username"]
            password = request.form["password"]
            # create BD
            tn_name = request.form["tn_name"]
            vrf_name = request.form["vrf_name"]
            bridge_domain_name = request.form["bridge_domain_name"]
            bridge_domain_alias = request.form["bridge_domain_alias"]
            bridge_domain_desc = request.form["bridge_domain_desc"]

            if host and username and password and tn_name and vrf_name and bridge_domain_name and bridge_domain_alias and bridge_domain_desc:
                token = login(
                            ip=host,
                            username=username,
                            password=password
                            )
                result = create_bd (
                                    ip = host,
                                    tn_name=tn_name,
                                    vrf_name=vrf_name,
                                    bd_name=bridge_domain_name,
                                    bd_alias=bridge_domain_alias,
                                    bd_desc=bridge_domain_desc,
                                    token=token
                                    )
            else:
                return render_template ("crt_bd.html") 
        else:
            return render_template ("crt_bd.html")

@app.route("/create_app", methods = ["POST", "GET"])
def crt_app():

    if request.method == "POST":
    # get token 
        host = request.form["host"]
        username = request.form["username"]
        password = request.form["password"]
        # create APP
        tn_name = request.form["tn_name"]
        app_name = request.form["app_name"]
        app_alias = request.form["app_alias"]
        app_desc = request.form["app_desc"]

        if host and username and password and tn_name and app_name and app_alias and app_desc:

            token = login(ip=host, username=username, password=password)
            result = create_app(
                            ip=host,
                            tn_name=tn_name,
                            app_name=app_name,
                            app_alias=app_alias,
                            app_desc=app_desc,
                            token=token
                            )

            return render_template ("crt_app.html", result=result)
        else:
            return render_template ("crt_app.html")
    else:
        return render_template ("crt_app.html")

@app.route("/create_epg", methods = ["POST", "GET"])
def crt_epg():
    if request.method == "POST":
        # get token 
        host = request.form["host"]
        username = request.form["username"]
        password = request.form["password"]
        # create EPG
        tn_name = request.form["tn_name"]
        app_name = request.form["app_name"]
        bd_name = request.form["bd_name"]
        epg_name = request.form["epg_name"]
        epg_alias = request.form["epg_alias"]
        epg_desc = request.form["epg_desc"]

        if host and username and password and tn_name and app_name and bd_name and epg_name and epg_alias and epg_desc:

            token = login(ip=host, username=username, password=password)
            result = create_epg(
                            ip=host,
                            tn_name=tn_name,
                            app_name=app_name,
                            bd_name=bd_name,
                            epg_name=epg_name,
                            epg_alias=epg_alias,
                            epg_desc=epg_desc,
                            token=token
                            )

            return render_template ("crt_epg.html", result=result)
        else:
            return render_template ("crt_epg.html")
    else:
        return render_template ("crt_epg.html")
    
@app.route("/create_bulk", methods = ["POST", "GET"])
def crt_bulk():
    if request.method == "POST":
        # get token 
        host = request.form["host"]
        username = request.form["username"]
        password = request.form["password"]

        token = login (ip=host, username=username, password=password)

        # create bulk

        file = request.files["crt_bulk"]
        filename = file.filename
        base_directory = os.path.dirname(__file__)

        file_path = os.path.join(base_directory, filename)
        file.save(file_path)

        # Change directory
        os.chdir(base_directory)
        result = create_bulk (file=file, host=host, token=token)
        if result is not None:
            return render_template ("crt_bulk.html", result = result)
        try: 
            os.remove(file_path)
        except Exception as e:
            print (e)

    return render_template ("crt_bulk.html")

# Download bulk template
@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=5001, debug=True)
