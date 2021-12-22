from . import trans
import json


def transText(message, base_lang , lang):
    s = str(trans.trans(message,lang))
    x = s.replace('[{"detectedLanguage":{"language":"'+base_lang+'","score":1.0},"translations":[{"text":"','')
    s = str(x.replace('","to":"'+ lang +'"}]}]',''))
    return s
