import os
import filecmp
import re

def FindDuplicatedClass(foldername):
    if os.path.isdir(TEMP_DIRECTORY):
        os.system('rm -rf ' + TEMP_DIRECTORY)
    os.system('mkdir ' + TEMP_DIRECTORY)
    classdict = dict()
    jarLocateDict = dict()

    CollectJar(foldername, jarLocateDict)
    UnzipJarAndFindClasses(classdict)
    FindOutDuplicatedClasses(classdict, jarLocateDict)


def FindOutDuplicatedClasses(classdict, jarLocateDict):
    fp_w=open(DUPLE_LIST_OUTPUT_FILENAME, 'w',encoding="utf-8")
    # 클래스들의 이름, 해당 클래스가 존재하는 위치의 리스트
    for className,classPathList in classdict.items():
        if len(classPathList) > 1 :# 중복이 존재할 경우 : 한 클래스가 여러곳에 존재할 경우
            #형식출력
            PrintLongLine(fp_w)
            #중복된 클래스
            print(className.replace(TEMP_DIRECTORY + '/', ''), file = fp_w)
            PrintLongLine(fp_w)
            print("duplicated at", file = fp_w)
            PrintLongLine(fp_w)
            #중복 위치 출력
            for i in range(len(classPathList)):
                print(str(i) + '. ' + classPathList[i].replace(TEMP_DIRECTORY + '/', '').split('THJAR_')[1], file = fp_w)
                originPath = jarLocateDict.get(classPathList[i].split('/')[1].split('THJAR_')[1] + '.aar', '') + jarLocateDict.get(classPathList[i].split('/')[1].split('THJAR_')[1] + '.jar', '')
                print( (' this class is in ' + originPath), file = fp_w)
            PrintLongLine(fp_w)
            #완전히 똑같은 클래스 출력
            for i in range(len(classPathList)-1):
                for j in range(i + 1, len(classPathList)):
                    if filecmp.cmp( classPathList[i], classPathList[j]) :
                        print(str(i) + " and " + str(j) + ' are exactly same', file = fp_w)
                        PrintLongLine(fp_w)
            print("\n", file = fp_w)
    fp_w.close()


def PrintLongLine(fp_w):
    print("-"*60, file = fp_w)


def FindClasses(jardir, classdict):
    for path, directory, inFolderFiles in os.walk(jardir):
        for inFolderFilename in inFolderFiles:
            if inFolderFilename.endswith('.class') :
                classFilePath = path + '/' + inFolderFilename
                #packagePath는 jar 파일 안에 압축된 경로명이다.
                packagePath = classFilePath.replace(jardir+'/', '')

                # 여기서 infoldername은 클래스파일명이 된다.
                if classdict.get(packagePath , 0) == 0 :
                    classdict[packagePath] = [classFilePath]
                else:
                    if classFilePath not in classdict[packagePath]:
                        classdict[packagePath] += [classFilePath]


def UnzipJarAndFindClasses(classdict):
    unziplist = list()
    remainJar = True

    while remainJar :
        remainJar = False
        for path, directory, inFolderFiles in os.walk(TEMP_DIRECTORY):
            for inFolderFilename in inFolderFiles:
                if inFolderFilename.endswith('.aar') or inFolderFilename.endswith('.jar'):
                    jarFilepath = path + '/' + inFolderFilename
                    if re.sub('....THJAR_','',jarFilepath) not in unziplist:
                        unziplist.append(re.sub('....THJAR_','',jarFilepath))
                        os.system("unzip -o -d " + jarFilepath.split('.aar')[0].split('.jar')[0]
                                  + ' ' + jarFilepath + '>>unziplog.txt')
                        #unzip 후 각 jar,aar의 압축해제 결과물이 저장된 디렉토리에서 Class들을 기록
                        FindClasses(jarFilepath.split('.aar')[0].split('.jar')[0] , classdict)
                        remainJar = True


def CollectJar(foldername, jarLocateDict):
    abspath = os.getcwd()
    index = 0
    for path, directory, inFolderFiles in os.walk(foldername):
        for inFolderFilename in inFolderFiles:
            if inFolderFilename.endswith('aar') or inFolderFilename.endswith('jar'):
                jarLocateDict[inFolderFilename] = path + '/' + inFolderFilename
                # 임시 폴더로 jar,aar파일 이동
                os.system("cp " + path + "/" + inFolderFilename + " " + abspath
                          + '/'+TEMP_DIRECTORY+'/' + "%04dTHJAR_"%index+inFolderFilename )
                index = index +1
def main():
    if os.path.exists("unziplog.txt"):
        os.system("rm unziplog.txt")


    global TEMP_DIRECTORY
    TEMP_DIRECTORY='temp_duplicated'
    global DUPLE_LIST_OUTPUT_FILENAME
    DUPLE_LIST_OUTPUT_FILENAME='duplicated_classes.txt'
    global CONFLICT_MODULE_LIST_FILENAME
    CONFLICT_MODULE_LIST_FILENAME='conflict_modules.txt'
    if os.path.isdir(TEMP_DIRECTORY):
        os.system("rm -rf " + TEMP_DIRECTORY)

    foldername = input("Enter project folder name: ")
    FindDuplicatedClass(foldername)

    os.system('rm -rf ' + TEMP_DIRECTORY)


if __name__ == "__main__":
    main()
