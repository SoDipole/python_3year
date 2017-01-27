import requests

class Professor:
    def __init__(self, surname = '', name = '', middlename = '', phone = [], email = [], position = {}):
        self.surname = surname
        self.name = name 
        self.middlename = middlename
        self.phone = phone
        self.email = email
        self.position = position

def teachers_with_etree(page):
    from lxml import etree
    root = etree.HTML(page.content)
    posts = root[1][1][3][2][1][0][2][1]    
    professors = []
    for post in posts:
        for part in post[0]:
            if 'l-extra small' in part.attrib['class']:
                phone = []
                email = []
                for element in part:
                    if element.tag == "span":
                        phone.append(element.text.encode('cp866', errors='replace').decode('cp866'))
                    elif element.tag == "a":
                        email.append(get_email(element.attrib['data-at']))
            elif 'main content small' in part.attrib['class']:
                fio = part[0][0][0].attrib['title']
                surname, name, middlename = split_names(fio)
                position = {}
                for pos in part[0][1]:
                    if pos.tag == "span":
                        for place in pos:
                            position[place.text.strip().encode('cp866', errors='replace').decode('cp866')] = pos.text.strip().strip(':').lower()
        professors.append(Professor(surname, name, middlename, phone, email, position))
    return professors

def get_email(string):
    email = ''
    for l in string.split(','):
        l = l.strip('\"\[\]')
        if l == '-at-':
            email += '@'
        else:
            email += l
    return email

def split_names(fio):
    fio = fio.split()
    surname = fio[0]
    name = fio[1]
    if len(fio) == 3:
        middlename = fio[2]
    else:
        middlename = ''    
    return surname, name, middlename
    
def teachers_with_xpath(page):
    from lxml import html
    tree = html.fromstring(page.content)
    professors = []
    posts = len(tree.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div'))
    for i in range(posts):
        fio = tree.xpath('string(/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div[' + str(i+1) + ']/div//div[@title]/@title)')        
        surname, name, middlename = split_names(fio)        
        phone1 = tree.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div[' + str(i+1) + ']/div/div[1]/span/text()')
        phone = []
        for p in phone1:
            phone.append(p.encode('cp866', errors='replace').decode('cp866'))
        pos = tree.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div[' + str(i+1) + ']//p//span/text()[1]')
        position = {}
        for j in range(len(pos)):
            place = tree.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div[' + str(i+1) + ']//p//span[' + str(j+1) + ']/a/text()')
            for pl in place:
                position[pl.encode('cp866', errors='replace').decode('cp866')] = pos[j].strip().encode('cp866', errors='replace').decode('cp866').strip(':')
        email = tree.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div[' + str(i+1) + ']//a[@data-at]/@data-at')
        for k in range(len(email)):
            email[k] = get_email(email[k])       
        professors.append(Professor(surname, name, middlename, phone, email, position))
    return professors               
        

page = requests.get('https://www.hse.ru/org/persons/?ltr=%D0%A1;udept=22726')

professors = teachers_with_etree(page)

#professors = teachers_with_xpath(page)

for p in professors:
    print(p.surname + ' ' + p.name + ' ' + p.middlename  + '\t' + str(p.position)  + '\t' + str(p.email)  + ' ' + str(p.phone))


