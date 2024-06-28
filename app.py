import os
from flask import Flask, render_template, request, redirect, flash, url_for,jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from components.final_file_generator import combine_files
from flask_mail import Mail, Message
from dotenv import load_dotenv



# get variable from .env
load_dotenv()

# get variable from .env



# Flask Configuration
app = Flask("Easay")
CORS(app)


# Mail Configuration
app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_STARTTLS'] = True
mail = Mail(app)


# File Upload Configuration
UPLOAD_FOLDER = './static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# .txt,.doc,.docx,.odt,.rtf
ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'odt', 'rtf'}
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
FINAL_FILE_PATH = './static/final_file/FINAL.doc'




"""
error handling for non existing pages
"""

# Error handler for 404 - page not found
@app.errorhandler(404)
def page_not_found(e):
    # Redirect to the root URL
    return redirect(url_for('index'))



# get all the files
@app.route("/files")
def get_files():
    """
    Getting all the files in the uploads folder.
    and displaying them on the index.html page
    """
    files = os.listdir('./static/files')
    return jsonify(files)





# get the uploaded files
# save them to the uploads folder
# send them back to the browser as a download


"""
    Check if the given filename is allowed based on the allowed extensions.

    Parameters:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the filename has an extension and the extension is in the allowed extensions list, False otherwise.
"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in request.files:
            print('file non existent')
            return redirect(request.url)
        files = request.files.getlist('files')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        for file in files:
            if file.filename == '':
                print('file name empty')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect('/')
            
    return render_template('index.html')

"""
Convert uploaded files to .doc format
"""
@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        files = request.json.get('files', [])
        upload_folder = './static/final_file'
        os.makedirs(upload_folder, exist_ok=True)

        # Ensure files exist and get their full paths
        file_paths = []
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.exists(file_path):
                file_paths.append(file_path)

        if not file_paths:
            return "No valid files to combine", 400
        
        # Combine files
        combined_file_path = combine_files(file_paths)
        
        # Render the template with combined_file_path
        return render_template('index.html', file_path=combined_file_path)
    
    return redirect(url_for('index'))


"""
Download the final .doc file
"""
@app.route('/download_final_file')
def serve_file():
    if not os.path.exists(FINAL_FILE_PATH):
        return 'File not found', 404
    
    return send_file(FINAL_FILE_PATH, as_attachment=True)

@app.route('/')
def index():
    file_exists = os.path.exists(FINAL_FILE_PATH)
    return render_template('index.html', file_exists=file_exists)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Check if the file exists before attempting to delete
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            # flash(f'Successfully deleted {filename}', 'success')
        except Exception as e:
            flash(f'Error deleting file {filename}: {str(e)}', 'error')
    else:
        flash(f'File {filename} not found', 'error')
    
    return redirect(url_for('index'))


@app.route('/about')
def about():
    """
    About page
    """
    return render_template('about.html')


"""
Email function
"""
# def send_email(name, email, problem, text):
#     msg = Message(
#         subject='Report Submission: ',
#         sender=app.config.get('MAIL_USERNAME'),
#         recipients=[app.config.get('MAIL_USERNAME')],
#         body=f"Name: {name}\nEmail: {email}\nProblem: {problem}\nText: {text}"
#     )
#     mail.send(msg)


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        problem = request.form.get('problem')
        text = request.form.get('text')

        if name and email and problem and text:
            # Send email
            # send_email(name, email, problem, text)
            msg = Message(
                subject=f'Report:{problem} - Reported by {name} - {email} ',
                sender=app.config.get('MAIL_USERNAME'),
                recipients=[app.config.get('MAIL_USERNAME')],
                body= f"{text}"
                
            )
            mail.send(msg)
            flash('Thank you for your report. We will get back to you soon', 'success')
            return render_template('reports.html', name=name, email=email, problem=problem, text=text)
        else:
            flash('Please fill all the fields', 'error')

    return render_template('reports.html')



if __name__ == "__main__":
    app.run(port=5000,debug=True)
