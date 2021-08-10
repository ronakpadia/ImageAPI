# Image manipulation API
from flask import Flask, render_template, redirect
import os
from PIL import Image
from flask.globals import request
from io import BytesIO
import base64
from fuzzywuzzy import fuzz

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# default access redirects to API documentation
@app.route("/")
def main():
    return "This is Image manipulation API"


# rotate filename the specified degrees
@app.route("/rotate", methods=["POST"])
def rotate_image():  
    angle = int(request.form.get('degrees'))
    file = request.files.get('files')
    # check for valid angle
    angle = int(angle)
    if not -360 < angle < 360:
        return render_template("error.html", message="Invalid angle parameter (-359 to 359)"), 400

    # open and process image
    target = os.path.join(APP_ROOT, 'static\\images')
    destination = "\\".join([target, file.filename])

    file.save(os.path.join(target, file.filename))

    img = Image.open(destination)
    img = img.rotate(-1*angle)

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str

# crop image
@app.route("/crop", methods=["POST"])
def crop_image():
    x1 = int(request.form.get('x1'))
    x2 = int(request.form.get('x2'))
    y1 = int(request.form.get('y1'))
    y2 = int(request.form.get('y2'))
    file = request.files.get('files')
    target = os.path.join(APP_ROOT, 'static/images')
    destination = "/".join([target, file.filename])
    file.save(os.path.join(target, file.filename))
    img = Image.open(destination)
    width = img.size[0]
    height = img.size[1]

    # check for valid crop parameters
    [x1, y1, x2, y2] = [int(x1), int(y1), int(x2), int(y2)]

    crop_possible = True
    
    while True:
        if not 0 <= x1 < width:
            crop_possible = False
            break
        if not 0 < x2 <= width:
            crop_possible = False
            break
        if not 0 <= y1 < height:
            crop_possible = False
            break
        if not 0 < y2 <= height:
            crop_possible = False
            break
        if not x1 < x2:
            crop_possible = False
            break
        if not y1 < y2:
            crop_possible = False
            break
        break

    # process image
    if crop_possible:
        img = img.crop((x1, y1, x2, y2))
    else:
        return render_template("error.html", message="Crop dimensions not valid"), 400

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str


@app.route("/name", methods=["POST"])
def name_match():
    string1 = request.form.get('string1')
    string2 = request.form.get('string2')
    fuzzratio = fuzz.ratio(string1, string2)
    if fuzzratio >= 90:
        resp = {
            "success":True,
            "data":{"is_name_match":"yes","name_match_conf":str(fuzzratio)+"%"}
        }
    else:
        resp = {
            "success":False,
            "data":{"is_name_match":"no","name_match_conf":str(fuzzratio)+"%"}
        }
    return resp

if __name__ == "__main__":
    app.run()