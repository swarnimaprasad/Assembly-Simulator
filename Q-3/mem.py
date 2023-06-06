import json
with open("bin.txt","r") as file:
    input_start=file.readlines()
if "\n" not in input_start[-1]:
    input_start[-1]=input_start[-1]+"\n"
if len(input_start)<128:
    while(len(input_start)!=127):
        input_start.append("0"*16+"\n")
    input_start.append("0"*16)
with open("memory.json","w") as memory:
    json_dict={"binary":input_start}
    json.dump(json_dict,memory)
with open("memory.json","r") as memory:
    json_dump=json.load(memory)
    binary=json_dump["binary"]
error=[]
def check():
    if(len(error)==0):
        return False
    else:
        return True
def fetchData(PC): 
    return binary[PC]

def memorydump():
    with open("memory.json","r") as memory:
        json_dump=json.load(memory)
        binary=json_dump["binary"]
    return binary