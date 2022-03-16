import json
import glob

groupPost = glob.glob("rawData/*/*/*.json")
pagePost = glob.glob("rawData/*/*.json")
groupPagePost = groupPost + pagePost


def is_json(myjson):
    try:
        json.load(myjson)
    except ValueError as e:
        return False
    return True


for postFile in groupPagePost:
    with open(postFile, "r", encoding="utf-8") as f:
        valid = is_json(f)
        if not valid:
            print(postFile)
