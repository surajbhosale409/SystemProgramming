import op

f=open("opcodeTab","w")
for inst in op.opcodes:
    f.write(inst+"\t"+op.opcodes[inst]+"\n")
f.close()
