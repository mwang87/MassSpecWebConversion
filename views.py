# views.py
from flask import abort, jsonify, render_template, request, redirect, url_for, make_response
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

    return response

@app.route('/upload1', methods=['POST'])
def upload_1():
    upload_string = util.convert_single_file(request)

    return "{}"
