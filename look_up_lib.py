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

--
TO DO
rewrite code and methods so get word
and return list of
----


Notes:
Remember you can't run the program on Python's shell because the utf8 char
acters won't show. You should run the program on the commmand line if you
are testing things out :) .
"""
import sys
import sqlite3
from dics.online_dics import MyMem
from dics.daum import DaumDict

class LookUp:
    """
    LookUp Class.
    This will read from a text file with words separated by newline characters.
    ex text file:
    ㅇㅓ
    ㅇㅗ
    ㅇㅓ
    """


    def __init__(self):
        """
        ?
        """
        self.db_name = 'dictionary.db'
        self.define_methods = [self._lookup_dic, self._lookup_daum,
                               self._lookup_mymem]

        self.UNSUCCESS = []

        #urls to visit
        self.urls = {}
        self.urls['daum'] = 'http://dic.daum.net/search.do?q=[word]&dic=eng'
        self.daum_dict = DaumDict()
        self.mymem = MyMem()

    def _lookup_kengdic(self, word):
        """
        Uses the postgres kengdic to look up the korean word
        returns false if word not found
        """
        pass
    def _lookup_mymem(self, word):
        """
        Lookup the word using the mymemmory api

        returns UNSUCCESS or the results
        """
        print("inside lookup mymem")
        results = self.mymem.get_def(word)

        if results is not None:
            return results
        else:
            return self.UNSUCCESS

    def _lookup_daum(self, word):
        """
        Lookup the word using the daum dictionary class

        returns True or False if added english def to output file
        """
        print("inside lookup daum")
        results = self.daum_dict.get_def(word)

        if results is not None:
            return results
        else:
            return self.UNSUCCESS

    def _lookup_dic(self, word):
        """
        Use the sqllite db called dictinoary.db to look up the korean word

        returns True for successful or False for unable to get any results from
        the dictionary
        """
        print("inside lookup sqllite dic")
        #connect to db
        try:
            self.db = sqlite3.connect(self.db_name)
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM Terms WHERE Expression = ?',(word,))
            results = cursor.fetchall()
        except Exception as e:
            #print("Not found in sqlite dictionary..")
            return self.UNSUCCESS

        #add results to output_file
        if len(results) > 0:
            return results
        else:
            return self.UNSUCCESS

    def _return_formatted_results(self, def_list, org_word):
        """
        Adds the orginal word, all definitions and dicitonary forms and hanja
        and returns as a list
        orginal_word;dictionary_form; eng_def; hanja

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

        return results

    def get_def(self, word):
        """
        Looks up the word and return a list
        orginal_word;dictionary_form; eng_def; hanja;
        """
        if(len(word) > 0):
            #try to look up word
            for define_method in self.define_methods:
                retn_list = define_method(word)
                if len(retn_list) > 0:
                    """def method and it is empty means it wasn't suc
                    essful. If it has values in the list means lookup
                    was successful and you can break and move on to next word
                    if get the return list from the
                    add results to file
                    """
                    results = self._return_formatted_results(retn_list, word)

                    return results




    def write_def_to_file(self, filename="file.txt",
                          output_filename="definitions.txt"):
        """
        This method will read in a text file with words separated by
        newline characters and create/overwrite a new file passed
        in with the filename given.

        ex.input filename
        한국\n
        엄마\n
        절\n

        result/output file:
        orginal_word;dictionary_form; eng_def; hanja;

        총;총;all,entire,whole, A gun;;
        누적시청자수;누적시청자수;The cumulative number of viewers;;
        구독;구독;Subscribe;;
        수현;수혈; ① give a blood transfusion ② blood transfusion ③ transfuse blood ;;
        간지;간지;interleaf, craft, guile;奸智,干支, 奸智,干支;
        펼침;arpeggio; ① develop ② unfold ③ revolve ④ launch ⑤ deploy ;;
        교양;교양;Culture or education;敎養;

        """
        #TODO do error checking for filename and output filename




        #open file and start reading line by line/word by word
        try:
            file = open(filename, 'r')
        except IOError:
            print("Sorry. file was not found and could not open. Please "
                  "Try again with a valid filename")
            return -1
        except Exception as e:
            print("Sorry something went wrong: %s"%e)
            return -1

        #open output file
        out_file = open(output_filename, 'w')

        #delete contents if already exists
        out_file.truncate()

        retn_list = []

        for line in file:
            word = line[:-1]#cut off newline or empty character at end of word

            if(len(word) > 0):
                #try to look up words
                for define_method in self.define_methods:
                    retn_list = define_method(word)
                    if len(retn_list) > 0:
                        """def method and it is empty means it wasn't suc
                        essful. If it has values in the list means lookup
                        was successful and you can break and move on to next word
                        if get the return list from the
                        add results to file
                        """
                        results = self._return_formatted_results(retn_list, word)

                        for value in results:
                            out_file.write('%s;'%value)

                        out_file.write('\n')
                        break

        #close output_file
        out_file.close()

look_up = LookUp()
#look_up.write_def_to_file("test_daum.txt", "out.txt")
cont = True
while cont:
    print("Main menu. type 'd' to look up words one by one.\n Type 'f' to "
          "look up words in a file and form an outfile of the definitions. 'q' is quit")

    key = input(": ")

    if(key == 'q'):
        cont = False
    elif key == 'f':
        look_up.write_def_to_file()
        print("wrote defitions to file")
    elif key == 'd':
        kor_word = input("Enter Korean word to search: ")
        print(str(look_up.get_def(kor_word)))
