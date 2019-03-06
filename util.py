
import os
from app import app
import json
import requests
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['mgf', 'mzxml', 'mzml', 'csv', 'txt', "raw"])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_localfile(input_filename, save_dir):
    extension = input_filename.rsplit('.', 1)[-1].lower()
    print(extension)

    """Do Nothing"""
    if extension != "raw":
        return input_filename

    """Perform Conversion"""
    cmd = "mono /src/bin/x64/Debug/ThermoRawFileParser.exe -i=%s -o=%s -f=1" % (input_filename, save_dir)
    os.system(cmd)
    os.remove(input_filename)
    output_filename = os.path.join(save_dir, os.path.basename(input_filename).replace(".raw", ".mzML"))
    return output_filename

def convert_single_file(request):
    filename = ""

    if 'file' not in request.files:
        return "{}"
    request_file = request.files['file']

    if request_file and allowed_file(request_file.filename):
        filename = secure_filename(request_file.filename)
        save_dir = "/output"
        local_filename = os.path.join(save_dir,filename)
        request_file.save(local_filename)
        local_filename = process_localfile(local_filename, save_dir)
        os.chmod(local_filename, 0o666)


        return local_filename

    return None
