alphabets=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def getEncodedChar(ch):
    try:
        i=alphabets.index(ch)
    except ValueError:
        i=-1

    if i!=-1:
        return alphabets[i+2]
    else:
        return ch


def encode(data):
    encodedData=[]
    for l in data:
        str=""
        for ch in l:
            str+=getEncodedChar(ch)
        encodedData.append(str)
    return encodedData

def getData(fname):
    f=open(fname,"r")
    return f.read()

def writeEncodedData(fname,data):
    f=open(fname,"w")
    for l in data:
        f.write(l)
    f.close()


data=getData("data.txt")
encodedData=encode(data)
writeEncodedData("encodeddata.txt",encodedData)


