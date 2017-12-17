import os
mydir = "/var/www/html/crisper/bacteria-complete-filter"
os.chdir(mydir)
for root, dirs, files in os.walk(mydir):
    for d in dirs:
        os.chdir(d)
        for root1, dirs1, files1 in os.walk(mydir + '/' + d):
            for file1 in files1:
                os.system('gzip -d' + file1)
