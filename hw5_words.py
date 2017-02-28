import os, json, re

class Word:
    pass

def add_lexems(d1, d2, word, analysis):
    for an in analysis:
        if word not in d2:
            d2[word] = {}
        if an['lex'] not in d2[word]:
            d2[word][an['lex']] = 1
        else:
            d2[word][an['lex']] += 1    
    

fr = open('python_mystem.json', encoding = 'utf-8')
text = fr.read().encode('cp866', errors='replace').decode('cp866')
fr.close()

d1 = {}
d2 = {}
for line in text.split('\n'):
    if 'analysis' in line:
        data = json.loads(line)
        if data['text'].lower() not in d1:
            l = len(data['analysis'])
            d1[data['text'].lower()] = l
            add_lexems(d1, d2, data['text'].lower(), data['analysis'])
        else:
            l = len(data['analysis'])
            d1[data['text'].lower()] += l
            add_lexems(d1, d2, data['text'].lower(), data['analysis'])
                    
print(d1)
print(d2)
