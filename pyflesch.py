#!/usr/bin/python

import re
import sys
import worddb

document = """Hello.  From Jamkit.

This is a short example document on which we can run this program.

""" # 25 words

def guess_syllables(word):
    "Guess the number of syllables in a word"
    # Out basic way of guessing is to count the number of vowels
    # in a word.  We then subtract 1 for each dipthong we find,
    # and add 1 for anti-dipthongs (OK, that's probably not the
    # technical term).
    
    syl = 0
    subtract_syl = ['cial',
                    'tia',
                    'cius',
                    'cious',
                    'giu',              # belgium!
                    'ion',
                    'iou',
                    'sia$',
                    '.ely$',             # absolutely! (but not ely!)
                    'ea.',
                    'oa.',
                    'enced$',
                    
                    ]
    add_syl = [
        'ia',
        'riet',
        'dien',
        'iu',
        'io',
        'ii',
        '[aeiouym]bl$',     # -Vble, plus -mble
        '[aeiou]{3}',       # agreeable
        '^mc',
        'ism$',             # -isms
        '([^aeiouy])\1l$',  # middle twiddle battle bottle, etc.
        '[^l]lien',         # alien, salient [1]
        '^coa[dglx].',      # [2]
        '[^gq]ua[^auieo]',  # i think this fixes more than it breaks
        'dnt$',           # couldn't
        ]
    word = word.lower()
    word = word.replace("'", "") # fold contractions
    word = word.replace('"', "") # remove quotes from around word
    word = re.sub("e$", "", word)
    spl = re.split("[^aeiouy]+", word)
    try:
        spl.remove("")
        spl.remove('') # why do this twice?  
    except ValueError:
        pass
    for rx in subtract_syl:
        if re.match(rx, word):
            syl -= 1
    for rx in add_syl:
        if re.match(rx, word):
            syl += 1
    if len(word) == 1: # 'x'
        syl += 1
    syl += len(spl)
    if syl == 0: syl = 1
    #print "# guessing syllable count: *%s*, %s" % (word, syl)
    return syl
    
    

def getFlesch(document):
    "Calculate the flesch reading ease score for the string 'document'"
    # We will count a bulleted line as a sentence
    BULLETS = ["* ", "- ", "o ", "*", "-"]
    
    syllables = 0.0
    words = 0
    sentences = 0.0
    
    word_re = re.compile(r"[a-zA-Z0-9'-]+")
    for word in document.split():
        word = word.upper()
        if word[-1] == "." or word[-1] == "?":
            sentences += 1
            word = word.replace(".", "")
	    word = word.replace("?", "")
        for b in BULLETS:
            bullet = 0
            if word.startswith(b):
                sentences += 1
                bullet = 1
                break
        if bullet:
            continue
        word = word.replace(",", "")
        try:
            s = int(worddb.worddb[word])
        except KeyError:
            s = guess_syllables(word)
        syllables += s
        words += 1
    print "words:", words
    print "sentences:", sentences
    print "syllables:", syllables
    if sentences==0: sentences = 1
    if words==0: words = 1
    ASL = (words/sentences)
    ASW = (syllables/words)
    return (206.835 - (1.015 * ASW) - (84.6 * ASW), (.39 * ASL) + (11.8 * ASW) - 15.59)



if __name__ == "__main__":
    document = sys.stdin.read()
    (flesch, gradelevel) = getFlesch(document)
    print "Flesch score", flesch
    print "Grade level", gradelevel
