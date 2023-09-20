import json 

f = open('dict_data_hm.json', 'r')
data = json.loads(f.read())
f.close()
new_data = { }
current_key = None
ids = []
for key in data.keys():
    new_key = key[:10]
    if new_key != current_key:
        if current_key != None:
            new_data[current_key] = {
                "min": min(ids),
                "max": max(ids)
            }
        current_key = new_key
        ids = []
    ids.append(data[key]["max"])
    ids.append(data[key]["min"])

f = open('new_data.json', 'w', encoding='utf-8')
f.write(json.dumps(new_data))
f.close()