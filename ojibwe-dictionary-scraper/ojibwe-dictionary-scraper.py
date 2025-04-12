from browsers import secret_agent
from bs4 import BeautifulSoup as bs
import csv
import datetime
import numpy as np
import pandas as pd
import random
from random import randint
import re
import requests

def timestamp():
    now = datetime.datetime.now()
    return(now)
   
def ojibwe_word_grammar():
    for entry in range(0,25):
        headers = {"user-agent": secret_agent[random.randint(0, len(secret_agent)-1)]}
        # print("header: ", headers)
        new_response = requests.get(new_url, headers=headers)
        new_html_soup = bs(new_response.text, "html.parser")
        new_page_html = new_html_soup.find_all("div", class_="english-search-main-entry")
        sample_entry = new_page_html[entry]
        word = sample_entry.find("a").text
        word_list.append(word)
        grammar = sample_entry.find_all("span")[2].text
        grammar = grammar.strip()
        if " " in grammar:
            # print("grammar: ", grammar)
            # print("contains \s")
            if "+" in grammar:
                updated_grammar = re.sub("\s\S\s", "-", grammar)
                # print("updated: ", updated_grammar)
                grammar_pos.append(updated_grammar)
            else:
                updated_grammar_2 = re.sub("\s", "-", grammar)
                # print("updated: ", updated_grammar_2)
                grammar_pos.append(updated_grammar_2)
        else:
            # print("grammar: ", grammar)
            # print("does not contain \s")
            grammar_pos.append(grammar)
        # print("entry count: ", entry)

print("begin time: ", timestamp(), "\n")
print("collect words and grammar parts...\n")
grammar_pos = []
word_list = []

alphabet = ["a", "aa", "b", "ch", "d", "e", "g", "h", "'", "i", "ii", "j", "k", "m", "n", "o", "oo", "p", "s", "sh", "t", "w", "y", "z", "zh"]
root_url = "https://ojibwe.lib.umn.edu/browse/ojibwe/"
headers = {"user-agent": secret_agent[random.randint(0, len(secret_agent)-1)]}
# print("header: ", headers)
response = requests.get(root_url, headers=headers)
html_soup = bs(response.text, "html.parser")
page_html = html_soup.find_all("div", class_="english-search-main-entry")

alphabet_count = 0
pages = 0
page_range = 5

for letter in alphabet:
    try:
        alphabet_count += 1
        print("alphabet count: ", alphabet_count)
        new_url = root_url+str(letter)
        print("letter: ", letter)
        while pages < page_range:
            try:
                if pages < 1:
                    # print("pages: ", pages)
                    pages += 1
                    print("url: ", new_url)
                    ojibwe_word_grammar()
                elif pages < 175:
                    # print("pages: ", pages)
                    pages += 1
                    page_range = 175
                    new_url = "https://ojibwe.lib.umn.edu/browse/ojibwe/"+str(letter)+"?page="+str(pages)
                    print("url: ", new_url)
                    ojibwe_word_grammar()
            except:
                print("almost there: ", timestamp(), "\n")
                pages = 0
                break
    except:
        continue
           
print(len(word_list), "words and", len(grammar_pos), "grammar parts collected!\n")

data_frame = pd.DataFrame(list(zip(word_list, grammar_pos)), columns = ["ojibwe word", "part of speech"])
data_frame.to_csv("ojibwe-dict.csv", sep=",", encoding="utf-8", index=None, header=True)

print("create urls...\n")
definition_url = []

for word, grammar in zip(word_list, grammar_pos):
    if "'" in word:
        if re.search(".*'$", word):
            # print("end apostrophy:", word)
            new_word = word.replace("'", "-")
            # print("replaced apostrophy start of word:", new_word)
            url_1 = "https://ojibwe.lib.umn.edu/main-entry/"+str(new_word)+str(grammar)
            # print("url:", url_1)
            definition_url.append(url_1)
        elif re.search("^'[aio]", word):
            # print("start apostrophy:", word)
            new_word = word.replace("'", "")
            # print("replaced apostrophy end of word:", new_word)
            url_2 = "https://ojibwe.lib.umn.edu/main-entry/"+str(new_word)+'-'+str(grammar)
            # print("url:", url_2)
            definition_url.append(url_2)
        else:
            # print("both:", word)
            new_word = word.replace("'", "-")
            # print("replaced apostrophy in word:", new_word)
            url_3 = "https://ojibwe.lib.umn.edu/main-entry/"+str(new_word)+'-'+str(grammar)
            # print("url:", url_3)
            definition_url.append(url_3)
    elif '-' in word:
        if re.search(".*\-$", word):
            # print("end hyphen:", word)
            url_4 = "https://ojibwe.lib.umn.edu/main-entry/"+str(word)+str(grammar)
            # print("url:", url_4)
            definition_url.append(url_4)
        elif re.search(".*\-.*", word):
            # print("middle hyphen:", word)
            url_5 = "https://ojibwe.lib.umn.edu/main-entry/"+str(word)+'-'+str(grammar)
            # print("url:", url_5)
            definition_url.append(url_5)
        else:
            # print("middle hyphen:", word)
            new_word = word.replace("'", "-")
            # print("replaced apostrophy:", new_word)
            url_6 = "https://ojibwe.lib.umn.edu/main-entry/"+str(new_word)+'-'+str(grammar)
            # print("url:", url_6)
            definition_url.append(url_6)
    elif "=" in word:
            # print("equal sign:", word)
            new_word = word.replace("=", "-")
            # print("replaced equal sign:", new_word)
            url_7 = "https://ojibwe.lib.umn.edu/main-entry/"+str(new_word)+str(grammar)
            # print("url:", url_7)
            definition_url.append(url_7)
    else:
        # print("neither")
        url_8 = "https://ojibwe.lib.umn.edu/main-entry/"+str(word)+"-"+str(grammar)
        # print("url:", url_8)
        definition_url.append(url_8)
    
print(len(definition_url), "urls created!\n")
data_frame["url"] = pd.Series(definition_url)
data_frame.to_csv('ojibwe-dict.csv', index=None, header=True)

print("collect definitions...\n")
definition_list = []
index = 1

for i in definition_url:
    try:
        if index % 1000 == 0:
            print(index, "of", len(definition_url), "definitions collected: ", timestamp())
        index = index + 1
        url = i
        headers = {"user-agent": secret_agent[random.randint(0, len(secret_agent)-1)]}
        response = requests.get(url, headers=headers)
        html_soup = bs(response.text, "html.parser")
        entry_containers = html_soup.find_all("div", class_="col-md-9 col-sm-9 content")
        sample_entry = entry_containers[0]
        target_definition = sample_entry.find("p", class_="glosses").text
        definition = target_definition.strip()
        definition_list.append(definition)
    except:
        definition_list.append("skip")
        continue

print("\n", len(definition_list), "definitions collected!\n")
data_frame["definition"] = pd.Series(definition_list)
data_frame.to_csv('ojibwe-dict.csv', index=None, header=True)

# uncomment this code block to define grammar types, clean nulls and skipped entries from final dataset

print("define grammar types...\n")
grammar_list = data_frame["part of speech"]
grammar_cat = []

for type in grammar_list:
    if re.search("^a", type):
        type_def = "adverb"
        grammar_cat.append(type_def)
    elif re.search("^n", type):
        if re.search("^n.*[se]$", type):
            type_def = "personal, place name"
            grammar_cat.append(type_def)
        elif re.search("^n.*r$", type):
            type_def = "noun phrase"
            grammar_cat.append(type_def)
        elif re.search("^n[ai].?v$", type):
            type_def = "(in)animate participle"
            grammar_cat.append(type_def)
        else:
            grammar_cat.append("noun")
    elif re.search("^p", type):
        if re.search("^pc.*", type):
            type_def = "particle"
            grammar_cat.append(type_def)
        elif re.search("^pf$", type):
            type_def = "prefix"
            grammar_cat.append(type_def)
        elif re.search(".*ep$", type):
            type_def = "preposition"
            grammar_cat.append(type_def)
        elif re.search("^pr.*", type):
            type_def = "pronoun"
            grammar_cat.append(type_def)
        elif re.search("^pv.*", type):
            type_def = "preverb"
            grammar_cat.append(type_def)
    elif re.search("^q", type):
        if re.search("^qn.*", type):
            type_def = "quantifier"
            grammar_cat.append(type_def)
        else:
            type_def = "unknown"
            grammar_cat.append(type_def)
    elif re.search("^v", type):
        if re.search("v.*r$", type):
            type_def = "verb phrase"
            grammar_cat.append(type_def)
        else:
            type_def = "verb"
            grammar_cat.append(type_def)
    else:
        grammar_cat.append("skip")

data_frame["category"] = pd.Series(grammar_cat)
data_frame.to_csv("ojibwe-dict.csv", index=None, header=True)

print("cleaning data...\n")
data_frame = data_frame.mask(data_frame == '')
data_frame = data_frame.dropna()
data_frame = data_frame[data_frame["definition"].str.contains("skip")==False]
data_frame = data_frame[["category", "part of speech", "ojibwe word", "definition", "url"]]
data_frame.to_csv('ojibwe-dict.csv', index=None, header=True)

print(".csv created!\n")
print("end time: ", timestamp())