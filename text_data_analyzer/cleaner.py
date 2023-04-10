import re
from persiantools import digits

def cleaning(text):
    
    numbers = digits.en_to_fa('0123456789')
    
    text = str(text)
    text = re.sub(r'[كﮑﮐﮏﮎﻜﻛﻚﻙ]', r'ک', text)
    text = re.sub(r'[ىىىﻴﻢﻳﻲﻱﻰىىﻯي]', r'ی', text)
    text = digits.ar_to_fa(text)
    text = digits.en_to_fa(text)
    text = re.sub(r'-', ' ', text)
    text = text.replace('\u200c', ' ')
    text = re.sub(r'([ا-ی])\1{2,}', r'\1', text)
    text = re.sub(r'[^\w\s]',' ',text)
    text=re.sub(r'[\–\—…°≈≠±≤≥\−×÷√٪→←↔↑↓\#()_\٫]',u' ',text) 
    temp = ''
    for i in range(len(text)-1):
        if text[i] in numbers and text[i+1] not in numbers+' ':
            temp = temp + text[i] + ' '
        elif text[i] not in numbers+' ' and text[i+1] in numbers:
            temp = temp + text[i] + ' '
        else:
            temp = temp + text[i]
    temp = temp + text[-1]
    text = ' '.join(temp.split())
    return text.strip()