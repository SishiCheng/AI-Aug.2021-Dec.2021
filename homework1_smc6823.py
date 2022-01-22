############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Sishi Cheng"


############################################################
# Section 1: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]


def concatenate(seqs):
    return [y for x in seqs for y in x]


def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


############################################################
# Section 2: Sequence Slicing
############################################################

def copy(seq):
    new = seq[:]
    return new


def all_but_last(seq):
    new = seq[:len(seq) - 1]
    return new


def every_other(seq):
    new = seq[:len(seq):2]
    return new


############################################################
# Section 3: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq) + 1):
        yield seq[:i]


def suffixes(seq):
    for i in range(len(seq) + 1):
        yield seq[i:len(seq)]


def slices(seq):
    j = 1
    for i in range(len(seq)):
        while j <= len(seq):
            yield seq[i:j]
            j += 1
        j = i + 2


############################################################
# Section 4: Text Processing
############################################################

def normalize(text):
    return (text.lower()).strip()


def no_vowels(text):
    result = [x for x in text if x.lower() not in ['a', 'e', 'i', 'o', 'u']]
    return ''.join(result)


def digits_to_words(text):
    digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    result = [x for x in text if x.isdigit()]
    string = ""
    for x in range(len(result)):
        string += digits[int(result[x])]
        string += " "
    return string


def to_mixed_case(name):
    words = list(filter(None, name.split("_")))
    result = words[0].lower() + "".join(x.title() for x in words[1:])
    return result


############################################################
# Section 5: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        new = []
        for x in self.polynomial:
            new.append((-x[0], x[1]))
        return Polynomial(new)

    def __add__(self, other):
        new = list(self.polynomial[:])
        for x in other.polynomial:
            new.append(x)
        return Polynomial(new)

    def __sub__(self, other):
        new = list(self.polynomial[:])
        for x in other.polynomial:
            new.append((-x[0], x[1]))
        return Polynomial(new)

    def __mul__(self, other):
        new = []
        for x in self.polynomial:
            for y in other.polynomial:
                new.append((x[0] * y[0], x[1] + y[1]))
        return Polynomial(new)

    def __call__(self, x):
        result = 0
        for y in self.polynomial:
            result += y[0] * x ** y[1]
        return result

    def simplify(self):
        poly_dict = {}
        i = 0
        for x in self.polynomial:
            if x[1] in poly_dict.keys():
                poly_dict[x[1]] += x[0]
                if poly_dict[x[1]] == 0:
                    del poly_dict[x[1]]
                    self.polynomial = self.polynomial[:i] + self.polynomial[i + 1:]
            else:
                poly_dict[x[1]] = x[0]
        i += 1
        self.polynomial = []
        if len(poly_dict) == 0:
            self.polynomial = self.polynomial + list((0, 0))
        else:
            for y in poly_dict:
                self.polynomial.append((poly_dict[y], y))
            self.polynomial.sort(key=lambda z: z[1], reverse=True)
        self.polynomial = tuple(self.polynomial)

    def __str__(self):
        result = ""
        flag = 0
        for x in self.polynomial:
            sign = "-" if x[0] < 0 else "+"
            coefficient = x[0] if x[0] != 1 and x[0] != -1 else ""
            if x[1] == 0:
                if flag == 0 and sign == "+":
                    result += f'{x[0]}'
                else:
                    if x[0] < 0:
                        result += f'{sign}{-x[0]}'
                    else:
                        result += f'{sign}{x[0]}'
            elif x[1] == 1:
                if flag == 0 and x[0] < 0 and x[0] != -1:
                    result += f'{sign}{-x[0]}x'
                elif flag == 0 and x[0] == -1:
                    result += f'{sign}x'
                elif flag == 0 and x[0] == 1:
                    result += f'x'
                elif flag == 0 and x[0] > 1:
                    result += f'{coefficient}x'
                elif flag == 0 and x[0] == 0:
                    result += f'{coefficient}x'
                elif x[0] < 0:
                    result += f'{coefficient}x'
                else:
                    result += f'{sign}{coefficient}x'
            else:
                if flag == 0 and x[0] >= 0:
                    result += f'{coefficient}x^{x[1]}'
                elif flag == 0 and x[0] < 0 and x[0] != -1:
                    result += f'{sign}{-x[0]}x^{x[1]}'
                elif flag == 0 and x[0] == -1:
                    result += f'{sign}x^{x[1]}'
                elif flag == 0 and x[0] == 1:
                    result += f'x^{x[1]}'
                elif flag == 0 and x[0] > 1:
                    result += f'{coefficient}x^{x[1]}'
                elif flag == 0 and x[0] == 0:
                    result += f'{coefficient}x^{x[1]}'
                else:
                    if x[0] < 0:
                        result += f'{coefficient}x^{x[1]}'
                    else:
                        result += f'{sign}{coefficient}x^{x[1]}'
            flag += 1
        return result


############################################################
# Section 6: Feedback
############################################################

feedback_question_1 = """
I spent approximately 18 hours on this assignment .
"""

feedback_question_2 = """
I found out that last question is the most challenging. 
Because I need to consider many conditions.
"""

feedback_question_3 = """
To be honest, I like the whole assignment.
It's good exercise for me. In my opinion, nothing need to be changed.
"""
