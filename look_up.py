"""
This is the module for the LookUp class.

Kelsey Jones

----
TO DO:
--- Make testingsoup a daum file and class
we want to separate the dictionaries to make it easier to use with other programs

---Add this API http://mymemory.translated.net/doc/spec.php

--- Make all Null values None

- Add support for if url blocks urlopen, like if daum locks you out
go to mymem or if mymem blocks your call

!Work on adding new cards with defintions on Anki
-This is my next step
Being able to import cards directly
----

"""
import sys
import sqlite3
from online_dics import DaumDict, MyMem

class LookUp:
    """
    LookUp Class.
    This will read from a text file with words separated by newline characters.
    ex text file:
    ㅇㅓ
    ㅇㅗ
    ㅇㅓ
    """
    
    def __init__(self, filename='file.txt'):
        """
        ?
        """
        self.filename = filename
        self.db_name = 'dictionary.db'
        output_file_name = 'definitions.txt'
        self.define_methods = [self._lookup_dic, self._lookup_daum,
                               self._lookup_mymem]

        #open output file
        self.out_file = open(output_file_name, 'w')
        
        #delete contents if already exists
        self.out_file.truncate()

        #urls to visit
        self.urls = {}
        self.urls['daum'] = 'http://dic.daum.net/search.do?q=[word]&dic=eng'
        self.daum_dict = DaumDict()
        self.mymem = MyMem()
        
        self._start_lookup()

        
    def _lookup_kengdic(self, word):
        """
        Uses the postgres kengdic to look up the korean word
        returns false if word not found
        """
        pass
    def _lookup_mymem(self, word):
        """
        Lookup the word using the mymemmory api

        returns True or False if added english def to output file
        """
        results = self.mymem.get_def(word)

        if results is not None:
            self._add_def_to_file(results, word)
            return True
        else:
            return False
        
    def _lookup_daum(self, word):
        """
        Lookup the word using the daum dictionary class

        returns True or False if added english def to output file
        """
        results = self.daum_dict.get_def(word)

        if results is not None:
            self._add_def_to_file(results, word)
            return True
        else:
            return False

    def _lookup_dic(self, word):
        """
        Use the sqllite db called dictinoary.db to look up the korean word

        returns True for successful or False for unable to get any results from
        the dictionary
        """
        #connect to db
        try:
            self.db = sqlite3.connect(self.db_name)
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM Terms WHERE Expression = ?',(word,))
            results = cursor.fetchall()
        except Exception as e:
            print("Not found in sqlite dictionary..")
            return False

        #add results to output_file
        if len(results) > 0:
            self._add_def_to_file(results, word)
            return True
        else:
            return False
        
    def _add_def_to_file(self, def_list, org_word):
        """
        Adds the orginal word, all definitions and dicitonary forms and hanja
        written on to the file.
        output file orginal_word;dictionary_form; eng_def; hanja

        def_list - is a list of tuples of definitions
        ex. [('말', 'man', 'NULL'),
        ('말', '4.765 US gallons', 'NULL'),
        ('말', 'Horse', 'NULL'), ('말', 'End', 'NULL'),
        ('말', 'words,speaking', 'NULL')]
        """
        #write to file
        #orginal word; dict form; eng definition; hanja; \n
        #combine eng_definitions and hanja if there are more than one tuple

        if(len(def_list) < 1):#if empty list dont add
            return 0
        
        eng_def = ''
        hanja = ''
        dict_form = def_list[0][0]
        
        for tup in def_list:
            if(len(eng_def) > 1):
                    eng_def += ', '
                    
            eng_def += ('%s'%tup[1])
            temp_hanja = tup[2]
            
            if temp_hanja != 'NULL' and temp_hanja is not None:
                if(len(hanja) > 1):
                    hanja += ', '
                hanja += ('%s'%temp_hanja)
                
        results = [org_word,dict_form,eng_def,hanja]
            
                
        for value in results:
            self.out_file.write('%s;'%value)
            
        self.out_file.write('\n')

    def _start_lookup(self):
        """
        Start looking up the files in the various korean resources
        """
        #open file and start reading line by line/word by word
        try:
            file = open(self.filename, 'r')
        except IOError:
            print("Sorry. file was not found and could not open. Please "
                  "Try again with a valid filename")
            return -1
        except Exception as e:
            print("Sorry something went wrong: %s"%e)
            return -1

        for line in file:
            word = line[:-1]#cut off newline or empty character at end of word

            if(len(word) > 0):
                #try to look up words
                for define_method in self.define_methods:
                    if define_method(word):
                        break

        #close output_file
        self.out_file.close()
        
if len(sys.argv) > 1:
    file = sys.argv[1] #get filename
    look_up = LookUp(file)
else:
    look_up = LookUp()
