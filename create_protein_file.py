import os
mydir = "/var/www/html/crisper/bacteria-complete"
for roots, dirs, files in os.walk(mydir):
    print os.path.basename(roots)
