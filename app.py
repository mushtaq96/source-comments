from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from script import sourceComments
from flask import send_from_directory

uploadFolder = "/home/mushtaq/Projects/uploadedFiles"
allowedExtensions = {'cs'}
maxFileSize = '10,400,000'  # 10 mb in bytes
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowedExtensions


@app.route('/')
def landing_page():
   return render_template('index.html')


app.config['UPLOAD_FOLDER'] = uploadFolder
app.config['MAX_CONTENT_PATH'] = maxFileSize
filename = ''

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    # function to let user submit the .cs file
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_relativepath = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            sourceComments(file_relativepath, '//')  # return true
            #return redirect(url_for('return_file', filename=filename))

        else:
            return "invalid file type"
    return redirect(url_for('landing_page'))

@app.route('/uploader/success/<path:filename>')
def return_file(filename):
    # return "success fully updated"
    # return render_template("download.html")
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename,  as_attachment=True)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
   app.run(debug = True)
