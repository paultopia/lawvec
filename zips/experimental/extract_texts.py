# not currently working, see https://stackoverflow.com/questions/49074623/saving-string-to-tarfile-in-python-3-throws-unexpected-end-of-data-error
from get_clean_text import get_cleaned_text
import tarfile
import json
from io import BytesIO
from pathlib import Path

max_length = 0

def make_clean_gzip(inzip):
    global max_length
    outzip = "extracted/clean-" + inzip
    with tarfile.open(inzip, 'r:gz') as infile, tarfile.open(outzip, 'w:gz') as outfile:
        jfiles = infile.getnames()
        for j in jfiles:
            dirtycase = json.loads(infile.extractfile(j).read().decode("utf-8"))
            cleaned = get_cleaned_text(dirtycase)
            caselength = len(cleaned)
            if caselength > max_length:
                max_length = caselength
            newtarfile = tarfile.TarInfo(Path(j).stem + ".txt")
            fobj = BytesIO()
            fobj.write(cleaned.encode('utf-8'))
            newtarfile.size = fobj.tell()
            outfile.addfile(newtarfile, fobj)


make_clean_gzip("usjc.tar.gz")
#make_clean_gzip("nyfamct.tar.gz")
#print(max_length)
