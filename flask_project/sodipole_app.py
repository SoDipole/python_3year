from flask import Flask
from flask import url_for, render_template, request
from pymystem3 import Mystem
from collections import defaultdict
import re, requests, json, os, random, pymorphy2
#from nltk import word_tokenize

app = Flask(__name__)
m = Mystem()
morph = pymorphy2.MorphAnalyzer()

def analyse_verbs(text):
    ana = m.analyze(text)
    verbs = defaultdict(int)
    words = num_verbs = part_verbs = tr_verbs = intr_verbs = pf_verbs = impf_verbs = 0
    for item in ana:
        if len(item) > 1:
            words += 1
            if len(item['analysis']) > 0:
                if item['analysis'][0]['gr'].startswith('V'):
                    num_verbs += 1
                    lemm = item['analysis'][0]['lex']
                    verbs[lemm] += 1
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
    return verbs, num_verbs, words, tr_verbs, intr_verbs, pf_verbs, impf_verbs

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

def get_lemmas_vk(group_id):
    lemmas = defaultdict(int)
    pos_dict = defaultdict(int)
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
                        lemmas[lemm] += 1
                        pos = item['analysis'][0]['gr'].split('=')[0].split(',')[0]
                        pos_dict[pos] += 1
    lemmas = sorted(lemmas, key=lemmas.__getitem__, reverse=True)
    if len(lemmas) > 100:
        lemmas = lemmas[:100]
    return lemmas, pos_dict

def get_words():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    file_url = os.path.join(SITE_ROOT, 'static', 'word_list.txt')    
    file = open(file_url, 'r', encoding = 'utf-8')
    word_list = file.read().split('\n')
    file.close()
    word_dict = {}
    for word in word_list:
        prop = morph.cyr2lat(morph.parse(word)[0].tag.cyr_repr).split()[0]
        word_dict[word] = prop
    return word_dict

def make_bot_line(line):
    word_dict = get_words()
    bot_words = []
    bot_line = ''
    pattern = re.compile("^[А-ЯЁа-яё]+?\-?[а-яё]*$")
    for word1 in line.split():
    #for word1 in word_tokenize(line):
        word1 = word1.strip('.,!?:-;#$%*()"@')
        if pattern.match(word1):
            tag = morph.parse(word1)[0].tag
            tag_string = morph.cyr2lat(tag.cyr_repr).split()
            words = [w for w, p in word_dict.items() if p == tag_string[0]]
            if len(words) == 0:
                pos = tag.POS
                words = [w for w, p in word_dict.items() if p.split(',')[0] == pos]
            lem2 = morph.parse(random.choice(words))[0]
            if len(tag_string) > 1:
                form = set((tag_string[1]).split(','))   
                for f in form:
                    if lem2.inflect(form):
                        lem2 = lem2.inflect(form)
            word2 = lem2.word
            bot_words.append(word2)
        else:
            bot_words.append(word1)
    bot_line = ' '.join(bot_words)
    return bot_line
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text', methods = ['POST', 'GET'])
def text():
    if request.form:
        text = request.form['text']
        verbs, num_verbs, words, tr_verbs, intr_verbs, pf_verbs, impf_verbs = analyse_verbs(text)
        return render_template('text.html', input = text, verbs = verbs, 
                               num_verbs = num_verbs, words = words, 
                               tr_verbs = tr_verbs, intr_verbs = intr_verbs, 
                               pf_verbs = pf_verbs, impf_verbs = impf_verbs)
    return render_template('text.html')

@app.route('/apivk', methods = ['POST', 'GET'])
def apivk():
    if request.form:
        group_id = request.form['group_id']
        is_closed = vk_api('groups.getById', group_id = group_id)['response'][0]['is_closed']
        if is_closed == 1:
            return render_template('apivk.html', is_closed = is_closed, data={})
        lemmas, pos_dict = get_lemmas_vk(group_id)
        return render_template('apivk.html', lemmas = lemmas, data = pos_dict)
    return render_template('apivk.html', data={})

@app.route('/chatbot', methods = ['POST', 'GET'])
def chatbot():
    if request.form:
        line = request.form['line']
        bot_line = make_bot_line(line)
        return render_template('chatbot.html', bot_line = bot_line)
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run()