from pytube import YouTube
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "flaTuber"

class urlForm(FlaskForm):
	url = StringField(validators = [DataRequired()])
	video_submit = SubmitField('Video')
	audio_submit = SubmitField('Audio')

@app.route('/', methods=['GET', 'POST'])
def index():
	form = urlForm()
	if form.validate_on_submit():
		press_video = form.video_submit.data
		press_audio = form.audio_submit.data	
		url = form.url.data
		yt = YouTube(url)
		if press_video:
			video = yt.streams.filter(subtype='mp4', progressive=True).order_by('resolution').desc().first()
			video.download()
		elif press_audio:
			audio = yt.streams.filter(subtype='mp4', only_audio=True).order_by('abr').desc().first()
			audio.download()
			
		flash('Done!')
		return redirect(url_for('index'))
	return render_template("index.html", form=form)