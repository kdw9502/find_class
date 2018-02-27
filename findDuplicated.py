import os
from os import chdir
import filecmp



def findDuplicatedClass(foldername):
    if os.path.isdir(TEMP_DIRECTORY):
        os.system('rm -rf '+TEMP_DIRECTORY)
    os.system('mkdir '+TEMP_DIRECTORY)
    classdict = dict()
    jarLocateDict = dict()

    collectJar(foldername, jarLocateDict)
    unzipJarAndFindClasses(classdict)
    findOutDuplicatedClasses(classdict)

def findOutDuplicatedClasses(classdict):
    fp_w=open(DUPLE_LIST_OUTPUT_FILENAME,'w')
    for className,classPathList in classdict.items():
        if len(classPathList)>1 :
            print(className,file=fp_w)
            print(classPathList,file=fp_w)
            for i in range(len(classPathList)-1):
                for j in range(i+1,len(classPathList)):
                    if filecmp.cmp( classPathList[i], classPathList[j]) :
                        print(classPathList[i]+" and "+classPathList[j]+' are exactly same',file=fp_w)
            print(file=fp_w)
    fp_w.close()

def findClasses(jardir,classdict):
    for path, directory, inFolderFiles in os.walk(jardir):
        for inFolderFilename in inFolderFiles:
            if inFolderFilename.endswith('.class') :
                classFilePath = path + '/' + inFolderFilename
                #packagePath는 jar 파일 안에 압축된 경로명이다.
                packagePath= classFilePath.replace(jardir+'/', '')

                # 여기서 infoldername은 클래스파일명이 된다.
                if classdict.get(packagePath , 0) == 0 :
                    classdict[packagePath]=[classFilePath]
                else:
                    if classFilePath not in classdict[packagePath]:
                        classdict[packagePath]+=[classFilePath]
                        
def unzipJarAndFindClasses(classdict):
    unziplist = list()
    remainJar = 1
    while remainJar > 0:
        remainJar = 0
        for path, directory, inFolderFiles in os.walk(TEMP_DIRECTORY):
            for inFolderFilename in inFolderFiles:
                if inFolderFilename.endswith('.aar') or inFolderFilename.endswith('.jar'):
                    jarFilepath=path + '/' + inFolderFilename
                    if jarFilepath not in unziplist:
                        unziplist.append(jarFilepath)
                        os.system("unzip -o -d " + jarFilepath.split('.aar')[0].split('.jar')[0]
                                  + ' ' + jarFilepath + '>>unziplog.txt')
                        findClasses(jarFilepath.split('.aar')[0].split('.jar')[0],classdict)
                        remainJar += 1


def collectJar(foldername, jarLocateDict):
    abspath = os.getcwd()
    for path, directory, inFolderFiles in os.walk(foldername):
        for inFolderFilename in inFolderFiles:
            if inFolderFilename.endswith('aar') or inFolderFilename.endswith('jar'):
                jarLocateDict[inFolderFilename] = path + '/' + inFolderFilename
                os.system("cp " + path + "/" + inFolderFilename + " " + abspath + '/'+TEMP_DIRECTORY+'/'+inFolderFilename)


def main():
    global TEMP_DIRECTORY
    TEMP_DIRECTORY='temp_duplicated'
    global DUPLE_LIST_OUTPUT_FILENAME
    DUPLE_LIST_OUTPUT_FILENAME='duplicated_classes.txt'
    foldername = input("Enter project folder name: ")
    findDuplicatedClass(foldername)


# os.system('rm -rf '+TEMP_DIRECTORY)

if __name__ == "__main__":
    main()
