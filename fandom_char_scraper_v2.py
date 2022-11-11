#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 21:10:06 2022

@author: embeaman
"""

import requests 
import time
import re
import py7zr
import io
from collections import Counter
from bs4 import BeautifulSoup
import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')


def parse(page):
    character_match = re.search(r'<title>(.+)</title>', page)
    character = character_match.group(1)
    pattern = r'=Appearance=+([^=]+wear[^=]+)(?:=|\[\[Category)'
    appearance_match = re.search(pattern, page, flags=re.DOTALL)
    appearance_text = appearance_match.group(1)
    return character, appearance_text

with open('../Downloads/fandom_links.txt') as f:
    fandom_links = f.read().splitlines()
    
with open('../Downloads/clothing_wordbank.txt') as f:
    clothing_wordbank = set(f.read().splitlines())

data = []
for f in fandom_links:
    _urlbase = f.rsplit('.com', 1)[0]
    urlbase = f"{_urlbase}.com/wiki"
    furl = f"{urlbase}/Special:Statistics"
    print(furl)
    try:
        r = requests.get(furl)
        if r.status_code != 200:
            print('bad status')
            continue
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
    wikisoup = BeautifulSoup(r.text)
    dump_label = wikisoup.find('label', attrs={'id': 'ooui-php-8'})
    if not dump_label:
        continue
    dump_link = dump_label.find('a')
    if not dump_link:
        continue
    dump_url = dump_link['href']
    if 'wikia_pages_current' in dump_url:
        continue
    rd = requests.get(dump_url)
    if rd.status_code != 200:
        continue
    print('downloading dump...')
    dump_content = rd.content
    print('decompressing dump...')
    dump_io = io.BytesIO(dump_content)
    dump_io.seek(0)
    dump_7z = py7zr.SevenZipFile(dump_io, 'r')
    dump_items = dump_7z.read()
    dump_text = io.TextIOWrapper(dump_items['contents']).read()
    
    print('parsing dump...')
    addlines = False
    for line in dump_text.splitlines():
        if line.strip() == '<page>':
            pagelines = []
            pagelines.append(line)
            addlines = True
        elif addlines:
            pagelines.append(line)
            if line.strip() == '</page>':
                addlines = False
                page = '\n'.join(pagelines)
                if '=appearance=' in page.lower():
                    data.append((urlbase, page))
        
pattern = r'=Appearance=+[^=]+wear[^=]+(=|\[\[Category)'
char_data = [d for d in data if re.search(pattern, d[1], flags=re.DOTALL)]  
_char_data_parsed = [(d[0],) + parse(d[1]) for d in char_data]  
char_data_parsed = [d for d in _char_data_parsed if d[1] is not None]

clothing_descriptions = []
for doc in nlp.pipe((d[-1] for d in char_data_parsed), batch_size=32):
    phrases = []
    for d in doc:
        if d.text.strip() in clothing_wordbank:
            phrase = doc[d.left_edge.i: d.right_edge.i + 1]
            phrases.append(phrase)
    
    if not phrases:
        clothing_descriptions.append(None)
        continue
            
    unique_maximal_phrases = []
    phrases.sort(key=lambda x: (x[0].i, x[-1].i))
    cur_phrase = phrases[0]
    for i in range(1, len(phrases)):
        next_phrase = phrases[i]
        if next_phrase[0].i > cur_phrase[-1].i:
            unique_maximal_phrases.append(cur_phrase)
            cur_phrase = next_phrase
        elif next_phrase[-1].i > cur_phrase[-1].i:
            cur_phrase = next_phrase
    if not unique_maximal_phrases or unique_maximal_phrases[-1] != cur_phrase:
        unique_maximal_phrases.append(cur_phrase)
        
    clothing_description = ' '.join([p.text for p in unique_maximal_phrases])
    clothing_descriptions.append(clothing_description)

    
final_descriptions = []
for cdp, cd in zip(char_data_parsed, clothing_descriptions):
    final_descriptions.append(cdp + (cd,))
    
df = pd.DataFrame(
    final_descriptions,
    columns=['url', 'character', 'full_description', 'clothing_description'],
    )
df.to_csv('repos/personal/halloween-costume-generator/fandom_scrape.csv', index=False)
    