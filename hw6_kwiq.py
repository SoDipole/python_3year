import re, unittest

def kwiq(word, text, num = 3):
    """Find all occurrences of the WORD in the TEXT surrunded by maximum of NUM words of context."""
    text2 = re.sub('- ', '— ', text)
    snippets = re.findall('(' + '(?:[а-яёА-ЯЁ\-\d]+?[\s\.,\(\)\[\]\"!\?—:;«»]+?){1,'+str(num)+'}' + word + '(?:[\s\.,\(\)\[\]\"!\?—:;«»]+?[а-яёА-ЯЁ\-\d]+?){1,'+str(num)+'}' + '[\s\.,\(\)\[\]\"!\?—:;«»]+?)', text2, flags=re.DOTALL)
    if snippets:
        for i in range(len(snippets)):
            snippet = re.sub('\n', ' ', snippets[i])     
            snippet = re.sub('\s{2,}', ' ', snippet)
            snippet = re.sub('([\s\.,\(\)\[\]\"!\?—:;«»])(' + word + ')([\s\.,\(\)\[\]\"!\?—:;«»])', '\\1###\\2###\\3', snippet)
            snippets[i] = snippet.split('###')  
    else:
        snippets = ''
    return snippets
    
def to_table(snippets, word):
    """Print all occurrences of the WORD in 'keyword in context' format."""
    widths = [max(map(len, col)) for col in zip(*snippets)]
    for snippet in snippets:
        print ('   '.join(val.ljust(width) for val, width in zip(snippet, widths)))
        
class kwiqTestCase(unittest.TestCase):
    #def test_one_word(self):
        #self.assertEqual(([['(', 'слово', '.']]), kwiq('слово', ' (слово. '))
    #def test_two_words(self):
        #self.assertEqual(('', 'слово', 'контекст'), kwiq('слово', 'слово контекст'))    
    def test_more_words(self):
        self.assertEqual(([['контекст контекст ', 'слово', ' контекст контекст.']]), kwiq('слово', 'контекст контекст слово контекст контекст.', 2))    
    def test_no_words(self):
        self.assertEqual((''), kwiq('слово', '')) 

#if __name__ == "__main__":
    #unittest.main()    
    
fr = open('text.txt', encoding = 'utf-8')
text = fr.read()
fr.close

word = 'в'
snippets = kwiq(word, text)
to_table(snippets, word)