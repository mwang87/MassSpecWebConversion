
import os
from app import app
import json
import requests
import errno
from werkzeug.utils import secure_filename
import glob

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

def save_single_file(request):
    sessionid = request.cookies.get('sessionid')
    request_file = request.files['file']

    filename = ""

    save_dir = "/output"
    if "fullPath" in request.form:
        local_filename = os.path.join(save_dir, sessionid, request.form["fullPath"])
    else:
        filename = secure_filename(request_file.filename)
        local_filename = os.path.join(save_dir, sessionid, filename)

    if 'file' not in request.files:
        return "{}"

    if not os.path.exists(os.path.dirname(local_filename)):
        try:
            os.makedirs(os.path.dirname(local_filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


    request_file.save(local_filename)

    print(request_file.filename)

def convert_all(sessionid):
    save_dir = "/output"
    output_conversion_folder = os.path.join(save_dir, sessionid, "converted")
    all_bruker_files = glob.glob(os.path.join(save_dir, sessionid, "*.d"))
    all_thermo_files = glob.glob(os.path.join(save_dir, sessionid, "*.raw"))
    all_mzXML_files = glob.glob(os.path.join(save_dir, sessionid, "*.mzXML"))
    all_mzML_files = glob.glob(os.path.join(save_dir, sessionid, "*.mzML"))
    

    print(all_thermo_files)

    """Bruker Conversion"""
    for filename in all_bruker_files:
        cmd = 'wine msconvert %s --32 --zlib --filter "peakPicking true 1-" --outdir %s' % (filename, output_conversion_folder)
        os.system(cmd)

    """Thermo Conversion"""
    for filename in all_thermo_files:
        cmd = 'wine msconvert %s --32 --zlib --filter "peakPicking true 1-" --outdir %s' % (filename, output_conversion_folder)
        os.system(cmd)

    #tar_path = output_conversion_folder = os.path.join(save_dir, sessionid, "converted.tar")
    cmd = "cd %s && tar -cvf %s %s" % (os.path.join(save_dir, sessionid), "converted.tar", "converted")
    print(cmd)
    os.system(cmd)
