import os
mydir = "/var/www/html/crisper/gff1"
os.chdir(mydir)
for root, dirs, files in os.walk(mydir):
    for myfile in files:
        # print(myfile)
        os.system('gzip -d '+ myfile)
