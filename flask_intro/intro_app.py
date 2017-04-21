from flask import Flask
from flask import url_for, render_template, request
import os

app = Flask(__name__)

def add_vote(pet):
    votes_file = open('votes.txt', 'r', encoding = 'utf-8')
    cats, dogs = votes_file.read().strip().split('\n')
    cats, dogs = int(cats), int(dogs)
    votes_file.close()
    if pet == 'cat':
        cats += 1
    elif pet == 'dog':
        dogs += 1
    cats, dogs = str(cats), str(dogs)
    votes_file = open('votes.txt', 'w', encoding = 'utf-8')
    votes_file.write(cats + '\n' + dogs)
    votes_file.close()
    return cats, dogs

def add_name(name):
    names_file = open('names.txt', 'r', encoding = 'utf-8')
    names = names_file.read().strip().split('\n')
    names_file.close()
    names_dict = {}
    if len(names[0]) > 0:
        names_dict = { name.split('\t')[0]:int(name.split('\t')[1])  for name in names }
    if name not in names_dict:
        names_dict[name] = 1
    else:
        names_dict[name] += 1
    names_file = open('names.txt', 'w', encoding = 'utf-8')
    names = []
    for n in sorted(names_dict):
        names.append(n + '\t' + str(names_dict[n]))
    names_file.write('\n'.join(names))
    names_file.close()
    return sorted(names)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods = ['POST', 'GET'])
def results():
    if request.method == 'POST':
        result = request.form
        name = result['name']
        pet = result['pet']
        cats, dogs = add_vote(pet)
        names = add_name(name)
        return render_template('results.html', names = names, cats = cats, dogs = dogs)

if __name__ == '__main__':
    app.run()