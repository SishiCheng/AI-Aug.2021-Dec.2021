############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Sishi Cheng"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import os


############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    fd = os.open(path, os.O_RDONLY)
    obj = os.fdopen(fd)
    data = []
    for x in obj:
        sentence = []
        for y in x.split():
            sentence.append(tuple(y.split("=")))
        data.append(sentence)
    return data


class Node:
    def __init__(self, tag, prob, pre):
        self.tag = tag
        self.prob = prob
        self.pre = pre


class Tagger(object):

    def __init__(self, sentences):
        self.tags = ["NOUN", "VERB", "ADJ", "ADV", "PRON", "DET", "ADP", "NUM", "CONJ", "PRT", ".", "X"]
        tags_index = {"NOUN": 0, "VERB": 1, "ADJ": 2, "ADV": 3, "PRON": 4, "DET": 5, "ADP": 6, "NUM": 7, "CONJ": 8,
                      "PRT": 9, ".": 10, "X": 11}
        d = len(tags_index)
        initial_prob = {"NOUN": 0, "VERB": 0, "ADJ": 0, "ADV": 0, "PRON": 0, "DET": 0, "ADP": 0, "NUM": 0, "CONJ": 0,
                        "PRT": 0, ".": 0, "X": 0}
        transition_prob = [[0 for i in range(d)] for j in range(d)]
        total = {"NOUN": 0, "VERB": 0, "ADJ": 0, "ADV": 0, "PRON": 0, "DET": 0, "ADP": 0, "NUM": 0, "CONJ": 0,
                 "PRT": 0, ".": 0, "X": 0}
        emission_prob = {}

        # num_sentences = len(sentences)

        for sentence in sentences:
            for i in range(len(sentence)):
                if i == 0:
                    initial_prob[sentence[0][1]] += 1

                if i < len(sentence) - 1:
                    transition_prob[tags_index[sentence[i][1]]][tags_index[sentence[i + 1][1]]] += 1

                total[sentence[i][1]] += 1

                if sentence[i][0] in emission_prob:
                    emission_prob[sentence[i][0]][tags_index[sentence[i][1]]] += 1
                else:
                    tag_list = [0 for i in range(d)]
                    emission_prob[sentence[i][0]] = tag_list
                    emission_prob[sentence[i][0]][tags_index[sentence[i][1]]] = 1

        for tag in self.tags:
            if initial_prob[tag] == 0:
                initial_prob[tag] = 1 / (len(sentences) + d)
            else:
                initial_prob[tag] = (initial_prob[tag] + 1) / (len(sentences) + d)

        self.initial_prob = initial_prob

        for i in range(d):
            for j in range(d):
                transition_prob[i][j] = (transition_prob[i][j] + 1) / (total[self.tags[i]] + d)

        self.transition_prob = transition_prob

        emission_prob["<UNK>"] = [0 for i in range(d)]
        for word in emission_prob:
            # temp = 0
            # for i in range(d):
            #    temp += emission_prob[word][i]
            for i in range(d):
                emission_prob[word][i] = (emission_prob[word][i] + 1) / (total[self.tags[i]] + len(emission_prob))

        self.emission_prob = emission_prob

    def most_probable_tags(self, tokens):
        result = []
        for token in tokens:
            most_probable = 0
            index = 0
            for i in range(len(self.tags)):
                if self.emission_prob[token][i] > most_probable:
                    most_probable = self.emission_prob[token][i]
                    index = i
            result.append(self.tags[index])
        return result

    def viterbi_tags(self, tokens):
        N_len = len(tokens)
        viterbi = [[Node("", 0, None) for j in range(len(self.tags))] for i in range(N_len)]
        for state in range(len(self.tags)):
            viterbi[0][state].tag = self.tags[state]
            if tokens[0] in self.emission_prob:
                viterbi[0][state].prob = self.initial_prob[self.tags[state]] * self.emission_prob[tokens[0]][state]
            else:
                viterbi[0][state].prob = self.initial_prob[self.tags[state]] * self.emission_prob["<UNK>"][state]

        for step in range(1, N_len):
            for state in range(len(self.tags)):
                max = 0
                node = None
                for i in range(len(self.tags)):
                    temp = viterbi[step - 1][i].prob * self.transition_prob[i][state]
                    if temp >= max:
                        node = viterbi[step - 1][i]
                        max = temp
                if tokens[step] in self.emission_prob:
                    viterbi[step][state].prob = max * self.emission_prob[tokens[step]][state]
                else:
                    viterbi[step][state].prob = max * self.emission_prob["<UNK>"][state]
                viterbi[step][state].tag = self.tags[state]
                viterbi[step][state].pre = node

        max = 0
        temp_node = None
        path = []
        for state in viterbi[N_len - 1]:
            if state.prob >= max:
                max = state.prob
                temp_node = state
        while temp_node is not None:
            path.append(temp_node.tag)
            temp_node = temp_node.pre
        path.reverse()
        return path


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """

I spent approximately 7 hours on this assignment .
"""

feedback_question_2 = """

I found out that second question is the most challenging. 
Because I spent most of the time to think about how to implement
"""

feedback_question_3 = """

To be honest, I like the whole assignment.
It's good exercise for me. In my opinion, nothing need to be changed.
"""
