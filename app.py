from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from script import sourceComments
from flask import send_from_directory

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
uploadFolder = os.path.join(FILE_DIR,'uploadedFiles')

allowedExtensions = {'cs'}
maxFileSize = '10,400,000'  # 10 mb in bytes
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = uploadFolder
app.config['MAX_CONTENT_PATH'] = maxFileSize


def allowed_file(fname):
    return '.' in fname and \
        fname.rsplit('.', 1)[1].lower() in allowedExtensions
filename = ''

@app.route('/')
def landing_page():
   return render_template('index.html',filenamee = filename)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    # function to let user submit the .cs file
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)    
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_relativepath = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            sourceComments(file_relativepath, '//')  # return true
            #return redirect(url_for('return_file', filename=filename)) #downloads the file
            
        else:
            return "invalid file type"
    return render_template('index.html',filenamee = filename)
    



@app.route('/uploader/success/<path:filename>')
def return_file(filename):
    # return "success fully updated"
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename,  as_attachment=True)
        return redirect(url_for(landing_page))
    except FileNotFoundError:
        abort(404)
    else:
        os.remove(filename)

    

if __name__ == '__main__':
   app.run(debug = True)
