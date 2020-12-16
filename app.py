from emoji.unicode_codes import UNICODE_EMOJI
from flask import Flask, render_template, request
import MeCab
from MeCab import error_info
from werkzeug.exceptions import abort
import markovify
import emoji
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index(title="your bot"):
    try:
        if request.method == 'GET':
            return render_template('index.html',title=title, error='', sentense='')
        elif request.method == 'POST':
            if 'file' not in request.files:
                print('file')
                file = request.files['file']
                fileobj = open(file,'r')
            elif request.form['text'] is not None:
                print('text')
                fileobj = request.form['text']
            else:
                return render_template('index.html',title=title, error='ファイルかテキストデータを送信してください。', sentense='')

#           raw_text = fileobj.split('\r\n')
 #          print(raw_text)
  #          talkobj = ''
   ##            line_split = line.split('\t')
     #           print(line_split)
      #          if line_split[0][2]==':' :
       #             if line_split[1] == request.form['name_to_make']:
        #                if line_split[2][-1]!='。':
         #                   line_split[2] += '。'
          #              talkobj += line_split[2]
           # print(talkobj)

#            talkobj_removed_emoji = ''.join(i for i in talkobj if i not in emoji.UNICODE_EMOJI)
 #           talkobj_removed_emoji = ''.join(i for i in talkobj if (i != '[写真]' and i != '[動画]' and i != '[スタンプ]'))
  #          print(talkobj_removed_emoji)

            raw_text = fileobj.split('\r\n')
            raw_text = [i for i in raw_text if i != '']
            talkobj = []
            for line in raw_text:
                line_split = line.split('\t')
                if str(line_split[0])[2]==':' :
                    if line_split[1] == request.form['name_to_make']:
                        if (line_split[2] != '[写真]') and (line_split[2] != '[動画]') and (line_split[2] != '[スタンプ]'):
                            talkobj.append(line_split[2])

            talkobj_removed_emoji = []
            for i in talkobj:
                if i not in emoji.UNICODE_EMOJI:
                    talkobj_removed_emoji.append(i)
            for i in range(len(talkobj_removed_emoji)):
                if str(talkobj_removed_emoji[i])[-1] != '。':
                    talkobj_removed_emoji[i] += '。'
            print(talkobj_removed_emoji)
            text_to_parse = ''.join(talkobj_removed_emoji)
#            text_to_parse = ''
 #           text_to_parse += (i for i in talkobj_removed_emoji)
            print(text_to_parse)

            parsed_text = MeCab.Tagger('-Owakati').parse(text_to_parse)

            text_model = markovify.Text(parsed_text, state_size=1)

            sentense = []
            for i in range(10):
                sentense.append(text_model.make_short_sentence(140).replace(' ',''))
            return render_template('index.html',title=title, error='', sentense=sentense)

        else:
            return abort(400)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)