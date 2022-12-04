import os 
# os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.24/tika-server-1.24.jar'
import sys
import tika
from tika import parser 
# tika.TikaJarPath = os.path.join("/", "tika-server.jar")
# tika.TikaPath = os.path.join("/", "tika-server.jar")
# os.environ['TIKA_SERVER_JAR'] = "/tika-server.jar"
# os.environ['TIKA_PATH'] = "/tika-server.jar"
import json

# files = os.listdir("../data/sample_papers/")
# DIR = "../data/sample_papers/"
# SAVE_DIR = "../data/proccesed_json/"

class StructurePDF:
    def __init__(self,json_file_name):
        json_file = parser.from_file(json_file_name)

        self.created_data = json_file["metadata"]["created"]
        
        self.created_by = json_file["metadata"]["creator"]
        self.title = json_file["metadata"]["dc:title"]
        self.content = json_file["content"]

        # self.content = json_file.get("content", "")
        # self.created_data = json_file["metadata"].get("created", "")
        
        # self.created_by = json_file["metadata"].get("creator", "")
        # self.title = json_file["metadata"].get("dc:title", "")
        
def save_json(struct, save_location):
    """
    Save the PDF in the target directory
    """
    dict_pdf = struct.__dict__
    with open(save_location+".json", 'w', encoding='utf-8') as f:
        json.dump(dict_pdf, f, ensure_ascii=False, indent=4)


# if __name__=="__main__":
#     for file in files:
#         temp = parser.from_file(DIR+file)
#         pdf = StructurePDF(temp)
#         save_json(pdf, SAVE_DIR+file.split(".")[0])