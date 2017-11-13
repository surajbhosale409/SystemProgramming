i=0
c=0
fl=0
d=0

datatypes={"int":i ,"char":c,"float":fl,"double":d}


def countVars():
    try:

        f=open("sample.c","r")
        for line in f:
            line=line.rstrip("\n")
            chunks=line.split()
            if len(chunks)>1:
                if chunks[0] in datatypes:
                    varss=chunks[1].split(",")
                    datatypes[chunks[0]]+=len(varss)
        print "No of integer variables: ",datatypes["int"],"\nNo of char variables: ",datatypes["char"],"\nNo of float variables: ",datatypes["float"],"\nNo of  double variables: ",datatypes["double"]
    except FileNotFoundError:
        print "FILE NOT FOUND"

countVars()
