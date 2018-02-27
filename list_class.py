import os
import glob
from os import chdir
import filecmp

def listClass():
    if not os.path.exists("../listsOfClasses"):
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
            # os.system("rm " + filename)
            chdir("../")
    fp_w=open("duplicated_classes"+""+".txt", 'w')
    chdir("temp")
    for key,value in classDict.items():
        if len(value)>1:
            print(key,file=fp_w)
            print(value,file=fp_w)
            for i in range(len(value)-1):
                for j in range(i+1,len(value)):
                    if filecmp.cmp(value[i],value[j]):
                        print(value[i]+" and "+value[j]+" is exactly same.",file=fp_w)
            print(file=fp_w)
    chdir("../")
    os.system("rm -rf temp")


def inJarListClass(jarname, fp_w):
    os.system("unzip -o -d " + jarname.split('.aar')[0].split('.jar')[0] + " " + jarname + ">>" +
              os.path.dirname(os.path.abspath(__file__))+ "/unzipLog.txt");
    if fp_w == None:
        fp_w = open('../listsOfClasses/' + jarname.split('.aar')[0].split('.jar')[0] + '.txt', 'w')

    for path, directory, inFolderFiles in os.walk('' + jarname.split('.aar')[0].split('.jar')[0]):
        for inFolderFileName in inFolderFiles:
            ext = inFolderFileName.split('.')[-1]
            if ext == 'class' or ext== 'so' or ext== 'a':
                # fp_w.write(inFolderFileName.split('$')[-1]+'\n')

                fp_w.write(inFolderFileName + '\n')
            elif ext == 'jar' or ext == 'aar':

                inJarListClass(jarname.split('.aar')[0].split('.jar')[0] + "/" + inFolderFileName, fp_w)
    os.system("rm -rf " + jarname.split('.aar')[0].split('.jar')[0])


def inJarFindDuplicatedClass(jarname, classDict):
    os.system("unzip -o -d " + jarname.split('.aar')[0].split('.jar')[0] + " " + jarname + ">>" +
              os.path.dirname(os.path.abspath(__file__)) + "/unzipLog.txt")

    for path, directory, inFolderFiles in os.walk('' + jarname.split('.aar')[0].split('.jar')[0]):
        for inFolderFileName in inFolderFiles:
            ext = inFolderFileName.split('.')[-1]
            if ext == 'class':

                packagePath= (path+'/'+inFolderFileName).replace(jarname.split('.aar')[0].split('.jar')[0]+'/', '')
                # 여기서 infoldername은 클래스파일명이 된다.
                if classDict.get(packagePath , 0) == 0 :
                    classDict[packagePath]=[path+'/'+inFolderFileName]
                else:
                    if path+'/'+inFolderFileName not in classDict[packagePath]:
                        classDict[packagePath]+=[path+'/'+inFolderFileName]
            elif ext == 'jar' or ext == 'aar':
                inJarFindDuplicatedClass(jarname.split('.aar')[0].split('.jar')[0] + "/" + inFolderFileName, classDict)
    #os.system("rm -rf " + filename.split('.aar')[0].split('.jar')[0])

def main():
    libraryName = input("Enter library name in this folder : ")
    try:
        chdir(libraryName)
    except:
        print('Wrong folder name')
        return
    if os.path.exists("unzipLog.txt"):
        os.system("rm unzipLog.txt")
    switch = input("1. Find out duplicated classes\n2. create list files of each Aar,Jar files\nEnter the menu num : ");
    if switch == '1':
        findDuplicatedClass()
    elif switch == '2':
        listClass()
    else:
        print('wrong menu num\n')


if __name__ == "__main__":
    main()

