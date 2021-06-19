import os
import base64
from io import BytesIO
from datetime import datetime

from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from PIL import Image
import RPi.GPIO as GPIO
import time
from implementasi import process_image
GPIO.setmode(GPIO.BOARD)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   22 : {'name' : 'GPIO 25', 'state' : GPIO.LOW}
   }

pins2 = {
	18 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}
}

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

for pin in pins2:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Request path to pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload') 
def upload():
    return render_template('upload.html')
    
@app.route('/camera')
def camera():
		# For each pin, read the pin state and store it in the pins dictionary:
	for pin in pins:
		pins[pin]['state'] = GPIO.input(pin)
	# Put the pin dictionary into the template data dictionary:
	templateData = {
		'pins' : pins
		}
	return render_template('camera.html', **templateData)

@app.route('/camera/upload', methods=['POST'])
def upload_snapshot():
	base64_img = request.form['img'].replace('data:image/jpeg;base64,', '')
	base64_bytes = base64_img.encode('ascii')
	filename = datetime.now().strftime('%Y%m%d_%H%M%S.png')
	im = Image.open(BytesIO(base64.decodebytes(base64_bytes)))
	im.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'PNG')
	return render_template('camera.html')

@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('camera.html', **templateData)

@app.route('/timer') 
def timer():
		# For each pin, read the pin state and store it in the pins dictionary:
	for pin in pins2:
		pins2[pin]['state'] = GPIO.input(pin)
	# Put the pin dictionary into the template data dictionary:
	templateData2 = {
		'pins2' : pins2
		}
	return render_template('timer.html', **templateData2)

@app.route("/timer/<changePin2>/<action2>")
def action2(changePin2, action2):
   # Convert the pin from the URL into an integer:
   changePin2 = int(changePin2)
   # Get the device name for the pin being changed:
   deviceName2 = pins2[changePin2]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action2 == "on":
      # Set the pin high:
      GPIO.output(changePin2, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName2 + " on."
   if action2 == "off":
      GPIO.output(changePin2, GPIO.LOW)
      message = "Turned " + deviceName2 + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins2:
      pins2[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData2 = {
      'pins2' : pins2
   }

   return render_template('timer.html', **templateData2)

@app.route('/imaging')
def imaging():

	return render_template('imaging.html')

@app.route('/imaging/<filename>')
def before_imaging(filename):

   return render_template('imaging.html', filename=filename)

@app.route('/upload/image', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		# flash('Image successfully uploaded and displayed')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect('/upload')

@app.route('/result/<filename>')
def result_on(filename):
    final_img = process_image(filename)
    return render_template('result.html', filename=final_img)

@app.route('/<filename>')
def display_result(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run('127.0.0.1', debug=True, port=5000, ssl_context=('server.crt','server.key'))
