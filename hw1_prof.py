import os, re, sys

class Professor:
    def __init__(self, surname = '', name = '', middlename = '', phone = '', email = ''):
        self.surname = surname
        self.name = name 
        self.middlename = middlename
        self.phone = phone
        self.email = email
        self.position = {}
    def get_surname(self, post):
        r = re.search('</div>\n\t+([\w\-]+)(?: [\w\(\)]+)? [\w]+', post)
        if r:
            self.surname = r.group(1)
    def get_name(self, post):
        r = re.search('</div>\n\t+[\w\-]+(?: [\w\(\)]+)? ([\w]+)', post)
        if r:        
            self.name = r.group(1)
    def get_middlename(self, post):
        r = re.search('</div>\n\t+[\w\-]+(?: [\w\(\)]+)? [\w]+ ([\w]+)', post)
        if r:
            self.middlename = r.group(1)
    def get_phone(self, post):
        r = re.search('<span>([\+\d\(\)\-\s\.\*добext]+)</span>', post)
        if r:
            self.phone = r.group(1)
    def get_email(self, post):
        r = re.search('\"mailto:(.+?)\">', post)
        if r:
            self.email = r.group(1)
    def get_position(self, post):
        r = re.findall('<span>\n\t{8}([\w\s\-,]+?):.+?>([\w\s\-,\.\"\(\)]+?)</a>[\t\n]+?\/[\t\n]+?<.+?>([\w\s\-,\.\"\(\)]+?)</a>[\t\n]+?\/[\t\n]+?<.+?>([\w\s\-,\.\"\(\)]+?)</a>', post, flags=re.DOTALL)        
        if not r:
            r = re.findall('<span>\n\t{8}([\w\s\-,]+?):.+?>([\w\s\-,\.\"\(\)]+?)</a>[\t\n]+?\/[\t\n]+?<.+?>([\w\s\-,\.\"\(\)]+?)</a>', post, flags=re.DOTALL)
            if not r:
                r = re.findall('<span>\n\t{8}([\w\s\-,]+?):.+?>([\w\s\-,\.\"\(\)]+?)</a>', post, flags=re.DOTALL)        
        if r:
            for pos in r:
                for i in range(1,len(pos)):
                    self.position[pos[i]] = pos[0] 
                    

fr = open('persons_s.html', encoding = 'utf-8')
text = fr.read().encode('cp866', errors='replace').decode('cp866')
fr.close()

professors = []

r = re.findall('<div class="post__content post__content_person">(.+?)\t</div>\n</div>', text, flags=re.DOTALL)
if r:
    for post in r:
        p = Professor()
        p.get_surname(post)
        p.get_name(post)
        p.get_middlename(post)
        p.get_phone(post)
        p.get_email(post)
        p.get_position(post)
        professors.append(p)

for p in professors:
    print(p.surname+ ' ' + p.name + ' ' + p.middlename  + ' ' + str(p.position)  + ' ' + p.email  + ' ' + p.phone)    
