import os
import glob
from os import chdir
import filecmp

def listClass():
    os.system("mkdir ../listsOfClasses")
    fp_w = None
    files = glob.glob('*');
    for filename in files:
        if filename.endswith('.aar') or filename.endswith('.jar'):
            inJarListClass(filename, fp_w)


def findDuplicatedClass():
    classDict = dict()
    os.system("mkdir temp")
    files = glob.glob('*');
    for filename in files:
        if filename.endswith('.aar') or filename.endswith('.jar'):
            os.system("cp "+filename+" temp/"+filename)
            chdir("temp")
            inJarFindDuplicatedClass(filename, classDict)
            chdir("../")
    os.system("rm -rf temp")


def inJarListClass(jarname, fp_w, depth=1):
    os.system("unzip -o -d " + jarname.split('.aar')[0].split('.jar')[0] + " " + jarname + ">>" + "../" * depth + "unzipLog.txt");
    if fp_w == None:
        fp_w = open('../listsOfClasses/' + jarname.split('.aar')[0].split('.jar')[0] + '.txt', 'w')

    for path, directory, inFolderFiles in os.walk('' + jarname.split('.aar')[0].split('.jar')[0]):
        for inFolderFileName in inFolderFiles:
            ext = inFolderFileName.split('.')[-1]
            if ext == 'class' or ext== 'so' or ext== 'a':
                # fp_w.write(inFolderFileName.split('$')[-1]+'\n')

                fp_w.write(inFolderFileName + '\n')
            elif ext == 'jar' or ext == 'aar':
                depth += 1
                inJarListClass(jarname.split('.aar')[0].split('.jar')[0] + "/" + inFolderFileName, fp_w, depth)
    os.system("rm -rf " + jarname.split('.aar')[0].split('.jar')[0])


def inJarFindDuplicatedClass(jarname, classDict, depth=1):
    os.system("unzip -o -d " + jarname.split('.aar')[0].split('.jar')[0] + " " + jarname + ">>" + "../" * depth + "unzipLog.txt");

    for path, directory, inFolderFiles in os.walk('' + jarname.split('.aar')[0].split('.jar')[0]):
        for inFolderFileName in inFolderFiles:
            ext = inFolderFileName.split('.')[-1]
            if ext == 'class':
                if classDict.get(inFolderFileName , 0) == 0 :
                    classDict[inFolderFileName]=[path+'/'+inFolderFileName]
                else:
                    if path+'/'+inFolderFileName not in classDict[inFolderFileName]:
                        classDict[inFolderFileName]+=[path+'/'+inFolderFileName]
            elif ext == 'jar' or ext == 'aar':
                depth += 1
                inJarFindDuplicatedClass(jarname.split('.aar')[0].split('.jar')[0] + "/" + inFolderFileName, classDict, depth)
    #os.system("rm -rf " + filename.split('.aar')[0].split('.jar')[0])

def main():
    libraryName = input("Enter library name in this folder : ")
    try:
        chdir(libraryName)
    except:
        print('Wrong folder name')
        return

    os.system("rm unzipLog.txt")
    switch = input("1. class list of each jar,aar\n2. find duplicated class\nEnter the menu num : ");
    if switch == '1':
        listClass()
    elif switch == '2':
        findDuplicatedClass()
    else:
        print('wrong menu num\n')


if __name__ == "__main__":
    main()

