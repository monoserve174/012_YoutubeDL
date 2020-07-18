from flask import Flask, render_template, request, url_for
import pafy
from datetime import datetime
import os
import re
app = Flask(__name__)
app.config['SECRET_KEY'] = 'KevinSecretKey'


@app.route('/', methods=['POST', 'GET'])
def index():
    filepath = os.path.abspath(os.path.dirname(__file__))
    if request.method == 'POST':
        yt_url = request.form.get('yt_url')
        if yt_url != '':
            yt = pafy.new(yt_url)
            dataname = f'{yt.category}-{datetime.now().strftime("%Y%m%d%H%M%S")}.webm'
            filepath = filepath + '/static/ytdl_temp/' + dataname
            yt.getbestaudio().download(filepath=filepath)
            with open(file=filepath) as f:
                contents = f.read()
            focus = re.findall('(?<=\<BaseURL>).*?(?=\</BaseURL>)', contents)[0]
            os.remove(filepath)
            return render_template('index.html', data_title=yt.title, filepath=focus)
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()