from textified import Textified

def parse(filename):
    textified = Textified(None, None, None, None)
    textified.fromFile(filename)
    return textified

# txt = parse('./downloads/01c1a2e5-CS-451  Week 1 Introduction.txt')
# print(txt.course_title)
# print(txt.full_text)