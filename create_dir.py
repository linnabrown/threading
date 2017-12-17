import os
import pprint
import threading
def chunks(l,n):
    """Yield successive n-sized chunks from l.
    """
    for i in range(0,len(l), n):
        yield l[i:i+n]

def myfunc(number):
    """ anti-crisper data preparing

    mv gff, faa and fna into a new dir,
    then user gzip -d to unpress .gz file,
    And then download the phaster.ca/submissions/refseq_id.zip into the new dir.
    """

    mydir = "/var/www/html/crisper/bacteria-complete"
    nwdir = "/var/www/html/crisper/bacteria-complete-filter2"
    nwdir_1 = "/var/www/html/crisper/bacteria-complete-filter1"
    oldDirs = os.listdir(mydir)
    nwdir_1s = os.listdir(nwdir_1)
    aDirs = list(set(oldDirs)^set(nwdir_1s))
    Dir_arr = list(chunks(aDirs,300))
    Dirs = Dir_arr[number]
    fw = open("/var/www/html/crisper_script/log3.txt","w")
    for onedir in Dirs:
        fullDir = mydir + '/' + onedir
        nmydir1 = nwdir + '/' + onedir
        if not os.path.exists(nmydir1):
            os.makedirs(nmydir1,0777)
        for root, dirs, files in os.walk(fullDir):
            for myfile in files:
                if (".gff.gz" in myfile) or \
                   (".faa.gz" in myfile) or \
                   (("_genomic.fna.gz" in myfile) and ("from" not in myfile)):
                    filename = fullDir + "/" + myfile
                    os.system('cp ' + filename + " " + nmydir1)
                    os.chdir(nmydir1)
                    os.system('gzip -d ' + nmydir1 + '/' + myfile)
                    if "fna" in myfile:
                        myfile_unpress = myfile[:-3]
                        f = open(nmydir1 + '/' + myfile_unpress)
                        h = f.readlines()
                        f.close()
                        for line in h:
                            if line[0]==">":
                                refseq = line[1:].split(" ")[0]
                                src = "phaster.ca/submissions/"+refseq+".zip"
                                os.system("wget "+src)
                                if not os.path.exists(nmydir1+'/'+ refseq+".zip"):
                                    fw.write(nmydir1+'/'+ refseq+".zip")
mydir = "/var/www/html/crisper/bacteria-complete"

nwdir_1 = "/var/www/html/crisper/bacteria-complete-filter1"
nwdir = "/var/www/html/crisper/bacteria-complete-filter2"

i = 0
oldDirs = os.listdir(mydir)
nwdir_1s = os.listdir(nwdir_1)
Dirs = list(set(oldDirs)^set(nwdir_1s))
Dir_arr = list(chunks(Dirs,300))
Dir_len = len(Dir_arr)
''' Create the threads

use threading function to run the chunks
'''
threads = []
for i in range(Dir_len):
    threads.append(threading.Thread(target=myfunc,args=(i,)))
# print threads

if __name__ == '__main__':
    for t in threads:
        #t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

# myfunc(Dirs, mydir, nwdir)
