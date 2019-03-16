# views.py
from flask import abort, jsonify, render_template, request, redirect, url_for, make_response, send_from_directory, send_file
import uuid

from app import app
import os
import glob
import json
import requests
import util

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "{}"

@app.route('/', methods=['GET'])
def classicnetworking():
    response = make_response(render_template('homepage.html'))
    response.set_cookie('sessionid', str(uuid.uuid4()))

    return response

@app.route('/upload1', methods=['POST'])
def upload_1():
    upload_string = util.save_single_file(request)


    return "{}"

@app.route('/convert', methods=['GET'])
def convert():
    sessionid = request.cookies.get('sessionid')
    summary_list = util.convert_all(sessionid)

    return json.dumps(summary_list)

"""Custom way to send files back to client"""
@app.route('/download', methods=['GET'])
def custom_static():
    sessionid = request.cookies.get('sessionid')
    return send_from_directory(os.path.join("/output", sessionid), "converted.tar")

@app.route('/summary', methods=['GET'])
def summary_file():
    sessionid = request.cookies.get('sessionid')
    filename = request.args.get("filename")

    return send_from_directory(os.path.join("/output", sessionid, "summary"), filename + ".html")
