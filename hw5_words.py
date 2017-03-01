import os, json, re

class Word:
    def __init__(self, **values):
        vars(self).update(values)

def count_lexems(d, word, analysis):
    for an in analysis:
        part = re.search('([A-Z]+)', an['gr']).group(1)
        if an['lex'] not in d[word][1]:
            d[word][1][an['lex']] = 1
        else:
            d[word][1][an['lex']] += 1    
        if part not in d[word][2]:
            d[word][2][part] = 1
        else:
            d[word][2][part] += 1 
            
def keywithmaxval(d): 
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]
    
fr = open('python_mystem.json', encoding = 'utf-8')
text = fr.read().encode('cp866', errors='replace').decode('cp866')
fr.close()

d = {}
for line in text.split('\n'):
    if 'analysis' in line:
        data = json.loads(line)
        word = data['text'].lower()
        if word not in d:
            l = len(data['analysis'])
            d[word] = [l,{},{}]
            if l > 0:
                count_lexems(d, word, data['analysis'])
        else:
            l = len(data['analysis'])
            d[word][0] += l
            if l > 0:
                count_lexems(d, word, data['analysis'])
words = []
for lemm in d:
    if d[lemm][0] == 0:
        words.append(Word(form = lemm, numAnalysis = 0))
    else:
        maxLex = keywithmaxval(d[lemm][1])  
        maxPart = keywithmaxval(d[lemm][2])
        words.append(Word(form = lemm, numAnalysis = d[lemm][0], maxLex = maxLex, maxPart = maxPart))
        
for word in words:
    if word.numAnalysis != 0:
        print(word.form, word.numAnalysis, word.maxLex, word.maxPart)
    else:
        print(word.form, word.numAnalysis)
