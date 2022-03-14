import glob
import json
import numpy as np
import pandas as pd

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


groupPost = glob.glob("data/*/*/*.json")
pagePost = glob.glob("data/*/*.json")
groupPagePost = groupPost + pagePost
listPostFile = []

# for postFile in groupPagePost:
#     listPostFile.append(postFile.split("\\")[-1].split(".")[0])


def getCommentInfo(data, comment):
    pass


for postFile in groupPagePost:
    with open(postFile, "r", encoding="utf-8") as f:
        # json.dump(DS, outfile, ensure_ascii=False)
        # print(postFile)
        data = json.load(f)

        row = {
            "Content": "",
            "PreComment": [],
            "Comment": "",
            "Label": 0,
        }
        if "Content" in data:
            row["Content"] = data["Content"]

            for comment in data["Comment"]:
                # getCommentInfo(data, comment)
                if comment is not None:
                    if "Cmt" in comment:
                        row["PreComment"].append(comment["Cmt"])

                    if "Reply cmt" in comment:
                        for reply in comment["Reply cmt"]:
                            print(
                                WARNING + str(comment["Reply cmt"]) + WARNING)
