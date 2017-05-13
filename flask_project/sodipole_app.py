from flask import Flask
from flask import url_for, render_template, request
from pymystem3 import Mystem
import re

app = Flask(__name__)
m = Mystem()

def analyse_verbs(text):
    ana = m.analyze(text)
    verbs = {}
    words = num_verbs = part_verbs = tr_verbs = intr_verbs = pf_verbs = impf_verbs = 0
    for item in ana:
        if len(item) > 1:
            words += 1
            if len(item['analysis']) > 0:
                if item['analysis'][0]['gr'].startswith('V'):
                    num_verbs += 1
                    lemm = item['analysis'][0]['lex']
                    if lemm in verbs:
                        verbs[lemm] += 1
                    else:
                        verbs[lemm] = 1
                    trans = re.search('\,нп', item['analysis'][0]['gr'])
                    if trans:
                        intr_verbs += 1
                    else:
                        tr_verbs += 1
                    perf = re.search('несов', item['analysis'][0]['gr'])
                    if perf:
                        impf_verbs += 1
                    else:
                        pf_verbs += 1
    if words > 0:
        part_verbs = round(num_verbs*100/words, 2)
    verbs = sorted(verbs, key=verbs.__getitem__, reverse=True)
    return verbs, num_verbs, part_verbs, tr_verbs, intr_verbs, pf_verbs, impf_verbs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text', methods = ['POST', 'GET'])
def text():
    if request.form:
        text = request.form['text']
        verbs, num_verbs, part_verbs, tr_verbs, intr_verbs, pf_verbs, impf_verbs = analyse_verbs(text)
        return render_template('text.html', input = text, verbs = verbs, 
                               num_verbs = num_verbs, part_verbs = part_verbs, 
                               tr_verbs = tr_verbs, intr_verbs = intr_verbs, 
                               pf_verbs = pf_verbs, impf_verbs = impf_verbs)
    return render_template('text.html')

if __name__ == '__main__':
    app.run()