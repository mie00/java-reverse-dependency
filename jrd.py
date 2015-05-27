import os, sys
from functional import seq
import re

def extract_imports(f,files,package_name):
    for line in f:
        if line.startswith("import"):
            yield line.strip()[7:-1]
        else:
            for class_name in re.findall("[A-Z][a-zA-Z0-9_]*",line):
                if class_name in files:
                    yield package_name+"."+class_name

if __name__ == "__main__":
    rootdir = sys.argv[1]
    imports = []
    class_names = []
    for root, subdirs, files in os.walk(rootdir):
        classes = map(lambda x:x[:-5],filter(lambda y:y.endswith(".java"),files))
        if classes:
            relative_root = root[len(rootdir):]
            package_name = relative_root.replace("/",".")
            for class_name in classes:
                full_class_name = package_name+"."+class_name
                class_names.append(full_class_name)
                with open(os.path.join(root,class_name+".java")) as f:
                    imports.append((full_class_name,list(extract_imports(f,filter(lambda x:x != class_name,classes),package_name))))
    sol = seq(imports).map(lambda (x,y):(seq(y).map(lambda z:(z,x)))).flatten().distinct().filter(lambda (x,y):x in class_names).group_by_key().map(lambda (x,y):(x,sorted(y))).to_list()
    print "\n".join(map(lambda (x,y):"%s\n%s\n%s\n\t%s"%("="*100,x,"-"*100,"\n\t".join(y)),sol))
