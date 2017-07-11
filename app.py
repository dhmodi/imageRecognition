import os
from flask import Flask, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from flask_session import Session
from keras.models import load_model
from keras.utils import plot_model
import cv2
import numpy as np
import gc
gc.collect()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()
sess.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('upload_file',
            #                         filename=filename))
            model = load_model('model.h5')
            #
            # model.compile(loss='binary_crossentropy',
            #               optimizer='rmsprop',
            #               metrics=['accuracy'])

            model.compile(loss='categorical_crossentropy',
                          optimizer='rmsprop',
                          metrics=['accuracy'])

            #   print (file)
            img = cv2.imread(UPLOAD_FOLDER + "/" + filename)
            img = cv2.resize(img, (224, 224))
            img = np.reshape(img, [1, 3, 224, 224])

            classes = model.predict_classes(img)
            if (classes[0] == 0):
                return (filename + ": AFS")
            elif (classes[0] == 1):
                return (filename + ": FI")
            else:
                return (filename + ": SP")
    #
    return 'AFS'