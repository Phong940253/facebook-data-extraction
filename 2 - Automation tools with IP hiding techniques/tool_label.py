import glob
import json
import os
import pandas as pd

# Lấy các file json từ folder rawData

folderPattern = "364997627165697"
fileNamePattern = "*"
check_point = "1778607179138061"


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


def assignLabel(Content, Pre_Cmt, Cmt, Id_Post, number_current_post, number_all_post):
    print(WARNING + "=" * 10 + "POSTER" + "=" * 10 + ENDC + "\n")
    print(str(number_current_post)+"|"+str(number_all_post))
    print("ID:"+Id_Post)
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


def cleanData(filePath, fileName, number_current_post, number_all_post):
    Result = []
    with open(filePath, encoding="utf8") as f:
        data = json.loads(f.read())
        for cmt in data['Comment']:
            try:
                if cmt is not None:
                    os.system('cls')
                    Result.append(assignLabel(
                        data['Content'], None, cmt['Cmt'], fileName, number_current_post, number_all_post))
                    if cmt['Number reply'] != 0:
                        pre = [cmt['Cmt']]
                        for i, rep in enumerate(cmt['Reply cmt']):
                            pre += [parent["Cmt"]
                                    for parent in cmt['Reply cmt'][:i]]
                            if rep is not None and rep['Cmt'] is not None:
                                Result.append(
                                    assignLabel(
                                        data['Content'],
                                        pre,
                                        rep["Cmt"],
                                        fileName,
                                        number_current_post,
                                        number_all_post))
                    print(BGGREEN + "Xong" + ENDC)
            except:
                pass
    return Result


# filePath = 'rawData/groups/364997627165697/1786546065010839.json'
# print(cleanData(filePath))

labeledFiles = glob.glob("data/*.csv")
labeledFileNames = []
for labeledFile in labeledFiles:
    labeledFileNames.append(labeledFile.split("\\")[-1].split(".")[0])


listFile = getFile()
# print(len(listFile))
# for n in listFile:
#     print(n)
check_point_index = listFile.index(
    f"rawData/groups/{folderPattern}\{check_point}.json")
# check_point_index=0
for i in range(check_point_index, len(listFile)):
    fileName = listFile[i].split("\\")[-1].split(".")[0]
    print(fileName)
    print(labeledFileNames)
    if fileName in labeledFileNames:
        continue

    df = pd.DataFrame(
        cleanData(listFile[i], fileName, i, len(listFile)),
        columns=[
            'Poster',
            'Pre-Comment',
            'Comment',
            'Label'])
    print(df)
    if "\\" in listFile[i]:
        fileName = listFile[i].split("\\")[-1].split(".")[0]
    else:
        fileName = listFile[i].split("/")[-1].split(".")[0]
    # print(fileName, filePath)
    # print(fileName)
    # Lưu trong folder data
    # if not os.path.exists(f'data/{page}'):
    #     os.makedirs(f'data/{page}')
    # if not os.path.exists(f'data'):
    #     os.makedirs(f'data')
    # df.to_csv(f"./data/{fileName}.csv", encoding='utf-8', index=False)
