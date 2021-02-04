from flask import Flask, render_template, request, redirect, url_for, flash, json,jsonify
from werkzeug.utils import secure_filename
import os
from script import sourceComments
from flask import send_from_directory
import re

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

@app.route('/jlpt',methods=['POST'])
def posted_input():
    if request.method == 'POST':
        gvariable={}
        japanese_text = request.form['japaneseText']
        japanese_text = japanese_text.strip()#strip whiespace including new line
        japanese_text = japanese_text.replace(" ","")#remove whitespaces in between
        japanese_text_kanji = filter_kanji_function(japanese_text)
        split_list = split(japanese_text_kanji)
        json_url = os.path.join(FILE_DIR,"static","kanji.json")
        data = json.load(open(json_url, encoding="utf-8_sig"))
        for each_character in split_list:
            value = kanji_details_function(data, each_character)
            isN3 = N3check_function(value)
            if(isN3):
                gvariable[each_character]=value #add the particular cases for N3
    return render_template('jlpt.html',N3ResultDic = gvariable)#send the final paragraph with jlpt n3 kanji result

def filter_kanji_function(text):
    hiragana_full = r'[ぁ-ゟ]'
    katakana_full = r'[゠-ヿ]'
    kanji = r'[㐀-䶵一-鿋豈-頻]'
    radicals = r'[⺀-⿕]'
    katakana_half_width = r'[｟-ﾟ]'
    alphanum_full = r'[！-～]'
    symbols_punct = r'[、-〿]'
    misc_symbols = r'[ㇰ-ㇿ㈠-㉃㊀-㋾㌀-㍿]'
    ascii_char = r'[ -~]'
    modfied_text = remove_unicode_block(hiragana_full, text)
    modfied_text = remove_unicode_block(alphanum_full,modfied_text)
    modfied_text = remove_unicode_block(katakana_full, modfied_text)
    modfied_text = remove_unicode_block(katakana_half_width,modfied_text)
    modfied_text = remove_unicode_block(symbols_punct,modfied_text)
    modfied_text = remove_unicode_block(ascii_char,modfied_text)
    modfied_text = remove_unicode_block(misc_symbols,modfied_text)
    ###need some attention
    return modfied_text

def remove_unicode_block(unicode_block, string):
    ''' removes all chaacters from a unicode block and returns all remaining texts from string argument.
    Note that you must use the unicode blocks defined above, or patterns of similar form '''
    return re.sub( unicode_block, '', string)
    
def split(ip_string):#split the string into individual characters
    return [char for char in ip_string]

def kanji_details_function(json_obj, key):#get the details for individual kanji
    if key in json_obj.keys():
        return json_obj[key]

def N3check_function(dictionary):#check for N3 Kanji 
    my_key = 'jlpt_new'
    if my_key in dictionary.keys():
        if dictionary[my_key]==3:
            return True
        else:
            return False


if __name__ == '__main__':
   app.run(debug = True,host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))
