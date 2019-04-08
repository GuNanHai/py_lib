import os
cwd = os.getcwd()
#获取当前路径下的所有文件夹的路径，按照数字小到大排列
def getDirList(path=cwd):
    dirList = []
    allDir = os.listdir(path)
    allDir.sort()
    for each in allDir:
        each = path + '/' + each
        if os.path.isdir(each):
            dirList.append(each)
    return dirList

def getFileList(path=cwd):
    fileList = []
    allDir = os.listdir(path)
    allDir.sort()
    for each in allDir:
        if each == '__pycache__':
                continue
        each = path + '/' + each
        if os.path.isfile(each):
            fileList.append(each)
    return fileList
