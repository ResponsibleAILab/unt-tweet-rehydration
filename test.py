import json 

f = open('dict_data_hm.json', 'r')
data = json.loads(f.read())
f.close()

num_wrong = 0
for key in data.keys():
    item = data[key]
    if item["min"] > item["max"]:
        num_wrong += 1
    
print(num_wrong)