
def isHTMLDoc(fname):
    f=open(fname,"r")
    for line in f:
        line=line.lower()
        if "<html>" in line:
            return True
    return False



print "File page.html is HTML File: ",isHTMLDoc("page.html")
print "File page1.html is HTML File: ",isHTMLDoc("page1.html")
