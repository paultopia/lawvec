## this code isn't usable.  See comment inside clean_text.  Need a more sophisticated strategy to distinguish citations with lots of periods from sentences in order for a sentence parser to do any work at all.

import re, string
from bs4 import BeautifulSoup
from nltk import sent_tokenize

# note: need to download punkt first on new machine
#   >>> import nltk
#  >>> nltk.download('punkt')


def extract_text(html):
    soup = BeautifulSoup(html, "lxml")
    for crap in soup(["script", "style", "meta"]):
        crap.extract()
    return soup.get_text()

my_punctuation = ''.join([x for x in string.punctuation if x is not '.']) + string.digits

transdict = {ord(x): " " for x in my_punctuation}

def clean_text(dirty_case):
    sentence_lines = "\n".join(sent_tokenize(dirty_case))
    # sentence parsers are a problem in cases.  It turns out that this doesn't work well because it treats bits of citations as sentences.
    # the citations do have important semantic meaning however, so I don't want to just chop out short lines.
    # I think a better strategy would just be to tell the gensim streaming corpus constructor to accept really really long sentences (like 500000 character sentence max for eg)
    # and this code should be considered not working.
    depunctuated = dirty_case.translate(transdict)
    desentenced = re.sub('\.\s+', "\n", depunctuated) # idea is to try to keep most abbreviation periods (often not followed by spaces, esp. in legal text) and ditch sentence periods
    # I'm also assuming there's no unicode punctuation other than section symbols, paragraph symbols, etc.
    return re.sub('\s\s+', " ", desentenced).lower()

def get_cleaned_text(opinion_from_courtlistener):
    if opinion_from_courtlistener["plain_text"]:
        text = opinion_from_courtlistener["plain_text"]
    elif opinion_from_courtlistener["html"]:
        text = extract_text(opinion_from_courtlistener["html"])
    elif opinion_from_courtlistener['html_lawbox']:
        text = extract_text(opinion_from_courtlistener["html_lawbox"])
    elif opinion_from_courtlistener['html_columbia']:
        text = extract_text(opinion_from_courtlistener["html_columbia"])
    elif opinion_from_courtlistener['html_with_citations']:
        text = extract_text(opinion_from_courtlistener["html_with_citations"])
    elif opinion_from_courtlistener['extracted_by_ocr']:
        text = opinion_from_courtlistener['extracted_by_ocr']
    else:
        text = ""
    return clean_text(text)

# test code

import json
with open("supcourt/99999.json") as j:
    case = json.load(j)
    print(get_cleaned_text(case))
