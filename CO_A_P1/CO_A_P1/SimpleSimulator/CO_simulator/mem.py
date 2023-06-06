import json,sys
with open("memory.json","r") as memory:
    json_dump=json.load(memory)
    binary=json_dump["binary"]
    error=json_dump["error"]
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
    for i in binary:
        sys.stdout.write(i+"\n")