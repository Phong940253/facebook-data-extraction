import json
import os
import pandas as pd

# Lấy các file json từ folder rawData


def getFile():
    listFile = []
    for root, directories, files in os.walk('rawData', topdown=False):
        for name in files:
            listFile.append(os.path.join(root, name))
    return listFile

# Dán nhãn


def assignLabel(Content, Pre_Cmt, Cmt):
    print("=" * 10 + "POSTER" + "=" * 10 + "\n")
    print(Content)
    print("\n")
    if Pre_Cmt is not None:
        for i, cmt in enumerate(Pre_Cmt):
            print("=" * 5 + f"Pre-Comment #{i}" + "=" * 5 + "\n")
            print(cmt)
    print("=" * 10 + "Comment" + "=" * 10 + "\n")
    print(Cmt)
    print("=" * 10 + "\n")
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
                print("Xong")
    return Result


# filePath = 'rawData/groups/364997627165697/1786546065010839.json'
# print(cleanData(filePath))
listFile = getFile()
for filePath in listFile:
    df = pd.DataFrame(
        cleanData(filePath),
        columns=[
            'Poster',
            'Pre-Comment',
            'Comment',
            'Label'])
    print(df)
    fileName = filePath.split("/")[-1].split(".")[0]
    # Lưu trong folder data
    df.to_csv(f"./data/{fileName}.csv", encoding='utf-8', index=False)
