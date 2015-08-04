# Anki-Korean-Lookup-Addon
This is an add on that will let you define Korean words using online Korean dictionaries and translation resources and add the cards to anki.

Work in Progress
The functionality right now works only on the commandline adnd creates a resulting textfile separated by semicolons with the
orginal Korean word, korean dictionary form, english definition, and hanja is there is any

TODO: 
1.Add support for adding words directly into Anki.
  User will select from GUI which deck and fields to add definitions to
  
  
2.Paste Korean words directly into GUI and start lookup of words

1. Pass txt filename as argument when running the program
  if don't specifiy argument it will try to open file.txt by default
  ex. $python3 look_up.py filename.txt


2. The text file should be korean words sperated by new lines.
ex. 


한국\n


엄마\n


절\n


3. write definitions to file
ex. 


총;총;all,entire,whole, A gun;;


누적시청자수;누적시청자수;The cumulative number of viewers;;


구독;구독;Subscribe;;


수현;수혈; ①  give a blood transfusion ②  blood transfusion ③  transfuse   blood  ;;


간지;간지;interleaf, craft, guile;奸智,干支, 奸智,干支;


펼침;arpeggio; ①  develop ②  unfold ③  revolve ④  launch ⑤  deploy  ;;


교양;교양;Culture or  education;敎養;

REFERENCE/Credit:
I used the sqllite dictionary from 	dayjaby's Yomichan Korean support pull request. Thank you!
