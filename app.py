from flask import Flask, render_template, request
from mecab import error_info
from werkzeug.exceptions import abort
import markovify
import MeCab
import emoji
app = Flask(__name__)

@app.route('/',['GET','POST'])
def index(title="your bot"):
    try:
        if request.method == 'GET':
            return render_template('index.html',title=title, error='')
        elif request.method == 'POST':
            if request.files is not None:
                file = request.files['file']
                fileobj = open(file,'r')
            elif request.form['text'] is not None:
                fileobj = request.form['text']
            else:
                return render_template('index.html',title=title, error='ファイルかテキストデータを送信してください。')
        else:
            return abort(400)
    except Exception as e:
        return str(e)

    raw_text = []
    while True:
        line = fileobj.readline()
        if line:
            raw_text.append(line)
        else:
            break
    
    talkobj = ''
    for line in raw_text:
        line_split = line.split()
        if line_split[1] == request.form.name_to_make:
            if line_split[2][-1]!='。':
                line_split[2] += '。'
            talkobj += line_split[2]

    talkobj_removed_emoji = ''.join(i for i in talkobj if i not in emoji.UNICODE_EMOJI)

    parsed_text = MeCab.Tagger('-Owakati').parse(talkobj_removed_emoji)

    text_model = markovify.Text(parsed_text, state_size=2)

    sentense = []
    for i in range(10):
        sentense.append(text_model.make_short_sentense(100,20,tries=100).replace(' ',''))
    return sentense

if __name__ == "__main__":
    app.run(debug=True)