from os import stat
import zipfile
from re import U, sub, subn
from shlex import quote
from sys import stderr, stdout
from flask import Flask,request, render_template, redirect
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import socket
import subprocess
from pathlib import Path
# import requests 

app = Flask(__name__)


# this code allows for executing docker commands and capturing the output 
def run_cmd(cmd) -> str:
    proc_out = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
    proc_data = proc_out.stdout.splitlines()
    return proc_data, proc_out.returncode

# showcase of all the API calls possible. Also, for sanity reasons, it prints out the `docker ps -a -s` to get size and other details about docker images
@app.route('/')
def index():
    # data_out = subprocess.run("docker ps -a -s ",shell=True,stdout = subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines = True)
    # data = data_out.stdout.splitlines()
    # print(data)
    data, status = run_cmd("docker ps -a -s ")
    print(data)
    return render_template('index.html',docker_ps = data)


# send over custom Dockerfile. Could be more secure by having random assigned data so other dockerfiles cannot be leaked...
@app.route('/upload/dockerfile',methods=["POST"])
def upload_dockerfile():
    # get file upload
    f = request.files['file']

    # get name of container to save under upload
    p = request.form.get('container-name')

    # make file upload path (even if it exists / does not exist)
    Path(f"uploads/"+ secure_filename(p)).mkdir(parents=True, exist_ok=True)

    # sanitize upload path, add it to the uploads directory
    f.save(f"uploads/"+ secure_filename(p) + secure_filename(f.filename))

    print(f.content_type)

    print(f"uploads/"+ secure_filename(p) + secure_filename(f.filename))
    if f.content_type == "application/zip":
        with zipfile.ZipFile(f"uploads/"+ secure_filename(p) + secure_filename(f.filename),"r") as zip_ref:
            zip_ref.extractall(f"uploads/"+secure_filename(p))        


    return render_template("index.html",upload_output = f"succesfully uploaded {p} ")

# build dockerfile. Do this before running
@app.route('/build/dockerfile',methods=["POST"])
def build_dockerfile():
    # ensure that no one can inject code into the shell with `quote`
    container_name = quote(request.form.get("container-name"))
    print(container_name)
    
    # build_out = subprocess.run(f"docker build uploads/{container_name}/ -t {container_name}:latest --build-arg MYPORT=8081",shell=True)
    build_out,status = run_cmd(f"docker build uploads/{container_name}/ -t {container_name}:latest --build-arg MYPORT=8081")
    # build_out = subprocess.run(f"docker build . -t {container_name}:latest --build-arg MYPORT={PORT}",shell=True)
    for output in build_out:
        print(output)

    if status == 0:
        return render_template("index.html",build_output=f"built the container {container_name}")
    else:
        return render_template("index.html",build_output=f"failed to build the container {container_name}")

# where the magic happens. Asks for an open port, launches container on that port
@app.route('/run/dockerfile',methods=["POST"])
def run_dockerfile():
    # Port to run on
    PORT = get_port()  
    
    container_name = quote(request.form.get("container-name"))
    container_user = quote(request.form.get("container-user"))
    # Can be python, login, etc.
    shell = quote(request.form.get("container-shell"))

    build_out, status = run_cmd(f"docker run -d --env MYPORT={PORT} -it -p {PORT}:{PORT} {container_name}:latest ttyd -p {PORT} -u {container_user} {shell}")

    for output in build_out:
        print(output)

    # build_out = subprocess.run(f"`docker run -d --env MYPORT=8082 -it -p {PORT}:{PORT} {container_name}:latest ttyd -p {PORT} {shell}`",shell=True)
    print(build_out)
    if status == 0:
        return render_template("index.html", run_output=f"launched {container_name} on port {PORT}. Enjoy :) \nContainer ID = {output}", latest_docker_running=f"http://localhost:{PORT}")
    else:
        return render_template("index.html",run_output=f"failed to launch {container_name}. Probably forgot to build first Here is the stacktrace: {build_out}")


@app.route('/stop/dockerfile',methods=["POST"])
def stop_dockerfile():

    container_id = request.form.get("container-id")
    # out = subprocess.run(f"docker stop {container_id}",shell=True)
    stop_out,status = run_cmd(f"docker stop {container_id}")
    # redirect(request.url)
    print(stop_out,status)
    
    return render_template("index.html",stop_output=stop_out)

@app.route('/data/dockerfile',methods=["POST"])
def data_dockerfile():
    
    name_of_container = request.form.get("container-id")

    stats, status = run_cmd(f"docker inspect {name_of_container}")
    print(stats)

    if status == 0:
        return "".join(stats)
    else:
        return "Error. Docker container might not exist"

    



@app.route('/build/port',methods=["GET"])
def get_port():
    """
    Use socket's built in ability to find an open port.
    Probably will cahnge later...
    """
    sock = socket.socket()
    sock.bind(('', 0))

    _, port = sock.getsockname()

    return str(port)




app.run(host='0.0.0.0', port=7777)