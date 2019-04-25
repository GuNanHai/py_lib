import os
cwd = os.getcwd()



# 获取当前路径下的所有文件夹的路径，按照数字小到大排列
def getDirList(path=cwd):
    dirList = []
    allDir = os.listdir(path)
    #-------------剔除非数字名称的文件夹
    temp = []
    for each in allDir:
        if os.path.basename(each).isdigit():
            temp.append(each)
    allDir = temp
    #-------------------------------
    allDir.sort(key=lambda f: int(os.path.basename(f)))
    for each in allDir:
        if each == '__pycache__':
            continue
        each = path + '/' + each
        if os.path.isdir(each):
            dirList.append(each)
    return dirList


def getFileList(path=cwd):
    fileList = []
    allDir = os.listdir(path)
    def getNum(val):
        baseName = os.path.basename(val)
        result = ''
        for each in baseName:
            if each.isdigit():
                result = result + each
        return result
    allDir.sort(key=lambda f: int(getNum(f)))
    for each in allDir:
        each = path + '/' + each
        if os.path.isfile(each):
            fileList.append(each)
    return fileList
