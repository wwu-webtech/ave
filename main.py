import os
from flask import Flask, flash, render_template, request, send_file, send_from_directory
from flask_uploads import UploadSet, configure_uploads
from werkzeug.utils import redirect, secure_filename
from markupsafe import escape


app = Flask(__name__)
extensions = ('mp4')  # restricting to mp4 for now. If updating this, also update HTML
videos = UploadSet("videos", extensions)
app.config["UPLOADED_VIDEOS_DEST"] = "static/uploads"
app.config["SECRET_KEY"] = os.urandom(24)
configure_uploads(app, videos)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'video' in request.files:
        try:
            video = request.files['video']
            videoname = secure_filename(video.filename)
            videos.save(video)
            flash("Video " + videoname + " saved successfully.")
            return render_template('index.html', uploaded_video=escape(videoname))
        except:
            flash("Incorrect file type. Please upload an MP4 file.")
            return render_template('index.html')
    return render_template('index.html')


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["UPLOADED_VIDEOS_DEST"], escape(filename))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/download')
def download(filename=''):
    path = "static/uploads" + filename  # <- security concerns
    return send_file(path, as_attachment=True)
