import os
import glob


depth=0    
os.system("rm log.txt")
fp_w = None
def inJarFindClass(filename,fp_w,depth):
        depth+=1
        os.system("unzip -d "+filename.split('.')[0]+" "+filename+">>"+"../"*depth+"log.txt");
        if fp_w==None:
            fp_w=open('class_List_'+filename.split('.')[0]+'.txt','w')
        
        for path,directory,inFolderFiles in os.walk(''+filename.split('.')[0]):
            for inFolderFileName in inFolderFiles:
                ext= inFolderFileName.split('.')[-1]
                if ext == 'class':
                    fp_w.write(inFolderFileName+'\n')
                elif ext == 'jar' or ext=='aar':
                    inJarFindClass(filename.split('.')[0]+"/"+inFolderFileName,fp_w,depth)
        os.system("rm -rf "+filename.split('.')[0])



files=glob.glob('*');
for filename in files:
    if filename.find('.aar')!=-1 or filename.find('.jar')!=-1:
        inJarFindClass(filename,fp_w,depth)

