alphabets=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def getDecodedChar(ch):
    try:
        i=alphabets.index(ch)
    except ValueError:
        i=-1

    if i!=-1:
        return alphabets[i-2]
    else:
        return ch


def decode(data):
    decodedData=[]
    for l in data:
        str=""
        for ch in l:
            str+=getDecodedChar(ch)
        decodedData.append(str)
    return decodedData

def getData(fname):
    f=open(fname,"r")
    return f.read()

def writeDecodedData(fname,data):
    f=open(fname,"w")
    for l in data:
        f.write(l)
    f.close()


data=getData("encodeddata.txt")
decodedData=decode(data)
writeDecodedData("decodeddata.txt",decodedData)


