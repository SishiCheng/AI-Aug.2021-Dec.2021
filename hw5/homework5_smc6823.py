############################################################
# CMPSC442: Homework 5
############################################################


student_name = "Sishi Cheng"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import os
from email import iterators
from math import log, exp


############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    fd = os.open(email_path, os.O_RDONLY)
    obj = os.fdopen(fd, encoding="UTF8")
    msg = email.message_from_file(obj)
    it = email.iterators.body_line_iterator(msg)
    tokens = []
    for l in it:
        tokens += l.split()
    return tokens


def log_probs(email_paths, smoothing):
    dic = {}
    for p in email_paths:
        tokens = load_tokens(p)
        for token in tokens:
            if token in dic:
                dic[token] += 1
            else:
                dic[token] = 1
    total = sum(dic.values())
    for token in dic:
        dic[token] = log((dic[token] + smoothing) / (total + smoothing * (len(dic) + 1)))

    dic["<UNK>"] = log(smoothing / (total + smoothing * (len(dic) + 1)))
    return dic


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam = os.listdir(spam_dir)
        for i in range(len(spam)):
            spam[i] = os.path.join(spam_dir, spam[i])
        ham = os.listdir(ham_dir)
        for i in range(len(ham)):
            ham[i] = os.path.join(ham_dir, ham[i])
        self.log_prob_spam = log_probs(spam, smoothing)
        self.log_prob_ham = log_probs(ham, smoothing)
        self.prob_spam = log(len(spam) / (len(spam) + len(ham)))
        self.prob_not_spam = log(len(ham) / (len(ham) + len(spam)))

    def is_spam(self, email_path):
        ham = self.prob_not_spam
        spam = self.prob_spam
        tokens = load_tokens(email_path)  # return a list of tokens in the file
        for i in tokens:
            if i in self.log_prob_spam:
                spam += self.log_prob_spam[i]
            else:
                spam += self.log_prob_spam["<UNK>"]
            if i in self.log_prob_ham:
                ham += self.log_prob_ham[i]
            else:
                ham += self.log_prob_ham["<UNK>"]

        return spam > ham

    def most_indicative_spam(self, n):
        indicative_spam = []
        for i in self.log_prob_spam:
            if i in self.log_prob_ham:
                value = self.log_prob_spam[i] - log((exp(1) ** (self.log_prob_spam[i] + self.prob_spam)) +
                                                    (exp(1) ** (self.log_prob_ham[i] + self.prob_not_spam)))
                indicative_spam.append((i, value))
        indicative_spam.sort(key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], indicative_spam))[:n]

    def most_indicative_ham(self, n):
        indicative_ham = []
        for i in self.log_prob_spam:
            if i in self.log_prob_ham:
                value = self.log_prob_ham[i] - log((exp(1) ** (self.log_prob_spam[i] + self.prob_spam)) +
                                                   (exp(1) ** (self.log_prob_ham[i] + self.prob_not_spam)))
                indicative_ham.append((i, value))
        indicative_ham.sort(key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], indicative_ham))[:n]


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent approximately 5 hours on this assignment .
"""

feedback_question_2 = """
I found out that first question is the most challenging. 
Because I am not families with the os and email module.
"""

feedback_question_3 = """

To be honest, I like the whole assignment.
It's good exercise for me. In my opinion, nothing need to be changed.
"""
