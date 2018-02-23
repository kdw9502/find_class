import os
import glob


    
os.system("rm log.txt")
files=glob.glob('*');
for filename in files:
    if filename.find('.aar')!=-1 or filename.find('.jar')!=-1:
        os.system("unzip -d "+filename.split('.')[0]+" "+filename+">>log.txt");
        fp_w=open('class_List_'+filename.split('.')[0]+'.txt','w')
        for path,directory,inFolderFiles in os.walk(''+filename.split('.')[0]):
            for inFolderFileName in inFolderFiles:
                ext= inFolderFileName.split('.')[-1]
                if ext == 'class':
                    fp_w.write(inFolderFileName+'\n')
        fp_w.close()
        os.system("rm -rf "+filename.split('.')[0])


