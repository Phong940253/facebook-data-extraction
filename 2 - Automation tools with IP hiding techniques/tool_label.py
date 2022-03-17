import glob
import json
import os
import pandas as pd

# Lấy các file json từ folder rawData

folderPattern = "nhatky"
fileNamePattern = "*"


def getFile():
    groupPost = glob.glob(
        f"rawData/groups/{folderPattern}/{fileNamePattern}.json")
    pagePost = glob.glob(f"rawData/{folderPattern}/{fileNamePattern}.json")
    return groupPost + pagePost

# Dán nhãn


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BGGREEN = '\x1b[6;30;42m'


def assignLabel(Content, Pre_Cmt, Cmt):
    print(WARNING + "=" * 10 + "POSTER" + "=" * 10 + ENDC + "\n")
    print(Content)
    print("\n")
    if Pre_Cmt is not None:
        for i, cmt in enumerate(Pre_Cmt):
            print(
                WARNING +
                "=" *
                5 +
                f"Pre-Comment #{i}" +
                "=" *
                5 +
                ENDC +
                "\n")
            print(cmt)
    print(WARNING + "=" * 10 + "Comment" + "=" * 10 + ENDC + "\n")
    print(Cmt)
    print(WARNING + "=" * 10 + ENDC + "\n")
    print("Comment này phù hợp hay không phù hợp ?")
    cmtLabel = input("1 = Phù hợp, 0 = Không phù hợp: ")
    os.system('cls')
    return [Content, Pre_Cmt, Cmt, cmtLabel]

# cleanData


def cleanData(filePath):
    Result = []
    with open(filePath, encoding="utf8") as f:
        data = json.loads(f.read())
        for cmt in data['Comment']:
            if cmt is not None:
                os.system('cls')
                Result.append(assignLabel(data['Content'], None, cmt['Cmt']))
                if cmt['Number reply'] != 0:
                    pre = [cmt['Cmt']]
                    for i, rep in enumerate(cmt['Reply cmt']):
                        pre += [parent["Cmt"]
                                for parent in cmt['Reply cmt'][:i]]
                        Result.append(
                            assignLabel(
                                data['Content'],
                                pre,
                                rep["Cmt"]))
                print(BGGREEN + "Xong" + ENDC)
    return Result


# filePath = 'rawData/groups/364997627165697/1786546065010839.json'
# print(cleanData(filePath))

labeledFiles = glob.glob("data/*.csv")
labeledFileNames = []
for labeledFile in labeledFiles:
    labeledFileNames.append(labeledFile.split("\\")[-1].split(".")[0])


listFile = getFile()

for filePath in listFile:
    fileName = filePath.split("\\")[-1].split(".")[0]
    print(fileName)
    print(labeledFileNames)
    if fileName in labeledFileNames:
        continue

    df = pd.DataFrame(
        cleanData(filePath),
        columns=[
            'Poster',
            'Pre-Comment',
            'Comment',
            'Label'])
    print(df)
    fileName = filePath.split("\\")[-1].split(".")[0]
    # print(fileName)
    # Lưu trong folder data
    # if not os.path.exists(f'data/{page}'):
    #     os.makedirs(f'data/{page}')
    if not os.path.exists(f'data'):
        os.makedirs(f'data')
    df.to_csv(f"./data/{fileName}.csv", encoding='utf-8', index=False)
