"""
Name: Korean / German Anki Sentence look up editor tool
Author: Kelsey Jones
This add on adds a lookup  button to the anki editor to allow
the user to look up highlighted words from xx dictionaries for Korean
and xx website for German. If the word is not found in the dictionary it
uses xx to translate the selected word and place the word in the field xx.
Date: 9/30/15

references:
http://ankisrs.net/docs/addons.html
https://github.com/z1lc/AutoDefine/blob/master/AutoDefineAddon/core.py
basic_CLOZE addon

Got button working on anki

Note: to check editor._html from within anki debug window -->
from aqt import editor
print editor._html

---
#use web.eval to execute the javascript
#do re stuff here to add to edit._html

#editor.web.eval("setFields(%s, %d);" % (allFields, 0))
#then do focus

editor.loadNote()
editor.web.eval("focusField(0);")
editor.web.eval("focusField(1);")
editor.web.eval("focusField(0);")

"""
from anki.hooks import wrap, addHook
from aqt import editor as aqt_editor
from aqt.editor import Editor
from aqt.utils import showInfo
import re

"""
Set Sentence field you want to highlight and look up words
Set Destination field to place Word - Def
"""
org_fld = 'Expression'
des_fld = 'Meaning'

#javascript methods will use
#to get highlighted/selected text
#
js = """
function getSelection()
{
    return (window.getSelection().getRangeAt(0).cloneContents())

};


"""

_anchor = '</script></head><body>'
_rex = re.compile( '(' + _anchor + ')')


def _add_def_to_field(field):

"""
This is where the real work will go.
the fields of the cards are the items()[field1][field2] etc

if the LK button is pressed it calls look_up editor
"""
def look_up(editor):
    valid_org_fld = False
    valid_des_fld = False

    #list of values like [u'value', ...]
    note = editor.note.items()
    showInfo(_(str(editor.note.items())))

    for field, val in note:
        if field == org_fld:
            valid_org_fld = True

        if field == des_fld:
            valid_des_fld = True

    if not valid_org_fld:
        showInfo(_("Sorry the name you entered for the word field is incorrect"))
        return

    if not valid_des_fld:
        showInfo(_("Sorry the name you entered for the destination field is incorrect"))
        return

    #set up javascript to get highlighted word
    #showInfo(_("returned selected text " + str(editor.web.page().mainFrame().evaluateJavaScript("getSelection()"))))
    sel = editor.web.selectedText()
    showInfo(_(sel))

    note = editor.note

    #add definition to second field value
    sec_field_name = note.items()[1][0]
    showInfo(_(sec_field_name))
    note[sec_field_name] = "hehehe"

    #need to loadNote to make sure new field value appears
    editor.loadNote()

    return



def setupButtons(editor):
    #add javascript to editor._html
    aqt_editor._html = _rex.sub(js + _anchor, aqt_editor._html)
    editor._addButton("LookUp", lambda ed=editor: look_up(ed),
                      text="LK", tip="Look up word.", key="Ctrl+d")

Editor.look_up = look_up
addHook("setupEditorButtons", setupButtons)
