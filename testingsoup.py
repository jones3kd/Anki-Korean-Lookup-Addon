"""
Holds the Daum Dictionary class
Uses Beautiful soup to extract english definitions

Todo:
1.)add support to retrieve multiple definitions
from the http://dic.daum.net/word/view.do?wordid page.
2.)Add Hanja
"""

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import time
import re
import random

defin = []
base_url = 'http://dic.daum.net'

class DaumDict:
    """
    This class looks up korean vocabulary words using the
    Daum korean-english dictionary.
    """

    def __init__(self):
        #will replace [word] with the actual korean
        #word we want to query
        self.url = 'http://dic.daum.net/search.do?q=[word]&dic=eng'

    def get_def(self, word):
        """
        Looks up the word givein the params and returns a
        list of tuples of definitons because
        there may be more than one definition for words.

        If the definition was not found returns None
        """
        kor_word = None
        eng_def = ""
        hanja = None

        #convert word from hangul into the percent characters
        #example converts korean word to %ED%95%9C%EB%B2%88
        word = urllib.parse.quote(word)

        #put word in url
        url = self.url.replace('[word]', word)
        
        time.sleep(random.randrange(4,10))
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        

        #returns a list of tag objects
        kor_word = soup.find(True, {'class':['inner_tit']})

        #if http://dic.daum.net/word/view.do?wordid
        if kor_word is not None:#specific daum definition page
            eng_def = soup.find(True, {'class':['wrap_meaning']})
            eng_def = eng_def.string
            hanja = soup.find(True, {'class':['phonetic font_ng']})
        else:#still daum search page
            #get korean defintion by taking first search result
            kor_word = soup.find(True, {'class':['link_txt']})
            
            #get eng definition
            eng_def_children = soup.find(True, {'class':['txt_means_KUKE']}).children
            if eng_def_children is not None or len(eng_def_children) > 0:
                for child in eng_def_children:
                    eng_def += child.string + ' '

                eng_def = eng_def.replace('\n','')
            

        #don't show hanja on search page so hanja stays as None
        if len(eng_def) > 0:
            kor_word = kor_word.string
            return [(kor_word, eng_def, hanja)]
        else:
            return None


"""
#open file and start reading line by line/word by word
try:
    file = open('test_daum.txt', 'r')
except IOError:
    print("Sorry. file was not found and could not open. Please "
          "Try again with a valid filename")
except Exception as e:
    print("Sorry something went wrong: %s"%e)

for line in file:
    kor_word = None
    eng_def = ""
    hanja = None
    #reset variable
    #url = 'http://dic.daum.net/search.do?q=[word]&dic=eng'
    
    word = line[:-1]#cut off newline or empty character at end of word
    print("original word: %s"%word)

    #word = urllib.urlencode(word)

    #convert word from hangul into the percent characters
    #example converts korean word to %ED%95%9C%EB%B2%88
    word = urllib.parse.quote(word)

    print("url before: %s"%url)
    #put word in url
    url = url.replace('[word]', word)
    print("url after: %s"%url)
    
    #specific look up dictionary
    time.sleep(random.randrange(4,10))
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    #print(soup.prettify())
    

    #returns a list of tag objects
    #get korean words
    #kor_words = soup.find_all(True, {'class':['inner_tit']})
    #if(kor_word)
    kor_word = soup.find(True, {'class':['inner_tit']})
    if kor_word is not None:#specific daum definition page
        eng_def = soup.find(True, {'class':['wrap_meaning']})
        eng_def = eng_def.string
        hanja = soup.find(True, {'class':['phonetic font_ng']})
    else:#still daum search page
        
        #get korean defintion by taking first sserach result
        kor_word = soup.find(True, {'class':['link_txt']})
        
        #get eng definition
        eng_def_children = soup.find(True, {'class':['txt_means_KUKE']}).children
        print(eng_def_children)
        for child in eng_def_children:
            eng_def += child.string + ' '

        #take out newline characters
        eng_def = eng_def.replace('\n','')
        

        #don't show hanja on search page so hanja stays as None
  
        


    #tags storing
    #[<span class="inner_tit">필요</span>, <span class="inner_tit">필요하다</span>]


    #print(soup.find(string))
    #print(kor_word)
    print("korean word: %s"%kor_word.string)
    print("Eng def: %s"%eng_def)

    if hanja is not None:
        print(hanja)



for tag in kor_words:

    #2 ways of getting string from tag elements
    print(tag.contents[0])
    print(tag.string)

for tag in kor_defs:

    #2 ways of getting string from tag elements
    print(tag.contents[0])
    print(tag.string)
"""


    
