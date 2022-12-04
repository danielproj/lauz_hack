import re

class Textified():
    def __init__(self, title, timestamp, url, course_title):
        self.full_text = ''
        self.timestamped_text = []
        self.title = title
        self.timestamp = timestamp
        self.url = url
        self.course_title = course_title
    # def __init__(self):
    #     self.full_text = ''
    def from_whisper_result(self, result):
        self.full_text = result['text']
        for segment in result['segments']:
            tt = [segment['start'], segment['end'], segment['text']]
            self.timestamped_text.append(tt)
    def toFile(self, title):
        with open(title, "w") as f:
            f.write("~" + self.title + "\n")
            f.write("~" + self.timestamp + "\n")
            f.write("~" + self.url + "\n")
            f.write("~" + self.course_title + "\n")
            for line in self.timestamped_text:
                f.write('[' + str(line[0]) + ':' + str(line[1]) + ']' + line[2] + "\n")
    def fromFile(self, title):
        with open(title, "r") as f:
            line = f.readline()
            self.title = line.split('~')[1]

            line = f.readline()
            self.timestamp = line.split('~')[1]

            line = f.readline()
            self.url = line.split('~')[1]

            line = f.readline()
            self.course_title = line.split('~')[1]

            self.timestamped_text=[]
            for line in f:
                res = re.match("^\[([0-9]*\.[0-9]*)\:([0-9]*\.[0-9]*)\](.*)", line)
                tStart = res.group(1)
                tEnd = res.group(2)
                text = res.group(3)
                tt = [tStart, tEnd, text]
                self.timestamped_text.append(tt)
                self.full_text= self.full_text + text