import json
dict1={1:10,2:12}
with open("memory2.json","w") as memory:
        json.dump(dict1,memory)
with open("memory2.json","r") as memory:
        dict2=json.load(memory)
print(type(dict2))
