#!/usr/bin/env python

import mailbox
import random
import string
import cPickle
import sys

try:
    with open('markov.pickle', 'rb') as f:
        markov_source = cPickle.load(f)
except IOError:
    mail_path = sys.argv[1].strip()
    footer_boundry = '_______________________(RACKSPACE Mailing List)_____________________________'

    markov_source = {}

    mbox = mailbox.mbox(mail_path)
    for i, msg in enumerate(mbox):
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                raw_body = part.get_payload(decode=True)
                while footer_boundry in raw_body:
                    raw_body = raw_body.split(footer_boundry)[0] # strip mailing list footer
                raw_body = raw_body.rstrip('\n').rsplit('\n\n', 1)[0] # strip off any signature (just a guess)
                body = []
                for line in (x.strip() for x in raw_body.split('\n')):
                    if not line:
                        continue
                    use = True
                    # get rid of signature lines and headers that show up in replies
                    for ignore in 'From: To: Sent: Subject: Office: Fax: [cid: Cc: Direct: Cell: email: phone: E-Mail: Web: Skype: AIM: Twitter: -----Original Mobile: wrote:'.split():
                        if ignore in line:
                            use = False
                            break
                    if use:
                        body.append(line)
                body = '\n'.join(body)
                if body:
                    words = []
                    for w in body.split():
                        cleaned_w = w.strip().strip(string.punctuation)
                        if cleaned_w.startswith('http'):
                            cleaned_w = None
                        if cleaned_w:
                            if w.endswith('.'):
                                cleaned_w += '.'
                            words.append(cleaned_w)
                    if len(words) <= 2:
                        continue
                    w1 = words[0]
                    w2 = words[1]
                    for word in words[2:]:
                        markov_source.setdefault((w1,w2), []).append(word)
                        w1, w2 = w2, word
        if i % 100 == 0:
            print i
    with open('markov.pickle', 'wb') as f:
        cPickle.dump(markov_source, f, protocol=cPickle.HIGHEST_PROTOCOL)

for _ in range(3):
    w1, w2 = random.choice(markov_source.keys())
    max_sentences = 4
    first_word = True
    while True:
        try:
            word = random.choice(markov_source[(w1,w2)])
        except KeyError:
            w1, w2 = random.choice(markov_source.keys())
            word = random.choice(markov_source[(w1,w2)])
        if first_word:
            print word.capitalize(),
            first_word = False
        else:
            print word,
        if word.endswith('.'):
            max_sentences -= 1
            first_word = True
            if max_sentences <= 0:
                break
            w1, w2 = random.choice(markov_source.keys())
        else:
            w1, w2 = w2, word
    print
    print