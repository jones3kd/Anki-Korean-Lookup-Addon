"""
To do
get hanja
get multiple definitions on page
example sentences
"""

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import time
import re
import random

defin = []

class NaverDict:
    """
    This class looks up korean vocabulary words using the
    Naver korean-english dictionary.
    """

    def __init__(self):
        #will replace [word] with the actual korean
        #word we want to query
        self.url = 'http://endic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=[word]'

    def get_def(self, org_word):
        """
        Looks up the word givein the params and returns a
        list of tuples of definitons because
        there may be more than one definition for words.

        If the definition was not found returns None
        """

        kor_word = None
        eng_defs = ""
        eng_def = ""
        hanja = None

        #convert word from hangul into the percent characters
        #example converts korean word to %ED%95%9C%EB%B2%88
        word = urllib.parse.quote(org_word)

        #put word in url
        url = self.url.replace('[word]', word)

        #time.sleep(random.randrange(4,10))
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')


        #returns a list of tag objects
        kor_word = soup.find(True, {'class':['first']})
        try:
            kor_word = kor_word.span.a.string
            eng_defs = soup.find(True, {'class':['list_e2']}).dd.div.p.span
            #print(eng_def.children)
            for string in eng_defs.stripped_strings:
                eng_def += str(string) + " "
            #eng_def = eng_def.dd.div.p.string
        except Exception as e:
            #could not find word in naver dic
            return None

        #dont forget to get the hanja

        if kor_word is None:
            kor_word = org_word

        return [(org_word, kor_word, eng_def)]

naver_dic = NaverDict()
word = input("enter word: ")
print(naver_dic.get_def(word))
