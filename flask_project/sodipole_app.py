from flask import Flask
from flask import url_for, render_template, request
from pymystem3 import Mystem
import re, requests, json

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

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

def get_lemmas_vk(group_id):
    lemmas = {}
    posts = vk_api('wall.get', domain = group_id)['response']
    num_posts = posts[0]
    if num_posts >= 1000:
        off = 9
    else:
        off = num_posts // 100
    while off >= 0:
        posts = vk_api('wall.get', domain = group_id, count = 100, offset = off*100)['response']
        off -= 1
        for i in range(1,len(posts)):
            if posts[i]['text']:
                ana = m.analyze(posts[i]['text'])
                for item in ana:
                    if len(item) > 1 and len(item['analysis']) > 0:
                        lemm = item['analysis'][0]['lex']
                        if lemm in lemmas:
                            lemmas[lemm] += 1
                        else:
                            lemmas[lemm] = 1
    lemmas = sorted(lemmas, key=lemmas.__getitem__, reverse=True)
    if len(lemmas) > 100:
        lemmas = lemmas[:100]
    return lemmas

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

@app.route('/apivk', methods = ['POST', 'GET'])
def apivk():
    if request.form:
        group_id = request.form['group_id']
        is_closed = vk_api('groups.getById', group_id = group_id)['response'][0]['is_closed']
        if is_closed == 1:
            return render_template('apivk.html', is_closed = is_closed)
        lemmas = get_lemmas_vk(group_id)
        return render_template('apivk.html', lemmas = lemmas)
    return render_template('apivk.html')

if __name__ == '__main__':
    app.run()