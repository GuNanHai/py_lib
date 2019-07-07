import os
import sys

# 依照系统判断文件路径分离符号
osPlatform = sys.platform
if osPlatform == 'win32':
    FPSLASH = '\\'
if osPlatform == 'linux1' or osPlatform == 'linux2':
    FPSLASH = '/'
    
cwd = os.getcwd()



# 获取当前路径下的所有文件夹的路径，按照数字小到大排列
def getDirList(path=cwd):
    dirList = []
    allDir = os.listdir(path)
    def getNum(val):
        baseName = os.path.basename(val)
        baseName = baseName.split('.')[0]
        result = ''
        for each in baseName:
            if each.isdigit():
                result = result + each
        if result=='':
            result=9999999
        return result
    allDir.sort(key=lambda f: int(getNum(f)))
    for each in allDir:
        each = path + FPSLASH + each
        if os.path.isdir(each):
            dirList.append(each)
    return dirList

# 获取当前路径下的所有文件的路径，按照数字小到大排列
def getFileList(path=cwd):
    fileList = []
    allDir = os.listdir(path)
    def getNum(val):
        baseName = os.path.basename(val)
        baseName = baseName.split('.')[0]
        result = ''
        for each in baseName:
            if each.isdigit():
                result = result + each
        if result=='':
            result=9999999
        return result
    allDir.sort(key=lambda f: int(getNum(f)))
    for each in allDir:
        each = path + FPSLASH + each
        if os.path.isfile(each):
            fileList.append(each)
    return fileList


cwd = os.getcwd()
dirList = getDirList(cwd)
count = 0
for each in dirList:
    fileList = getFileList(each)
    for f in fileList:
        if f.find('.mp4') != -1:
            count += 1
            # 此处依据实际文件名的命名规则进行相应修改！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！1
            basename = os.path.basename(f).split(' ')[1:]
            basename = '_'.join(basename)
            newfilename = each+FPSLASH+str(count)+'-'+basename

            print(newfilename)
            os.rename(f,newfilename)

