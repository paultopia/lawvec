import tarfile
import glob
import os

tars = [x for x in glob.glob("extracted/*") if os.path.isfile(x)]

def count_file_length(zippedfile, textfile):
    return len(zippedfile.extractfile(textfile).read().decode("utf-8"))

def get_max_length(tar):
    with tarfile.open(tar, "r:gz") as zippedfile:
        textfiles = zippedfile.getnames()
        return max(count_file_length(zippedfile, x) for x in textfiles)

max_length = max(get_max_length(x) for x in tars)

with open("maxlength.txt", "w") as ml:
    ml.write(str(max_length))

print("max length is: ", max_length)
