from PIL import Image
import base64
import gzip
import json
import zlib
import pprint

nbt_string = b'H4sIAAAAAAAA/42QwQrCMAyG3yXnHfS6q+LJNxCRdk266dwkiSIde3dbu4GiiJemf/r' \
             b'/X2gGsG1fnQTK3QCNgzJrKKZaAl27KkrDPpqiR/Gc3PuxAGfUJEfTIozF8OHJt2cnkW' \
             b'+GYQ4N0JkzzuECpOovScahpoUxwqXtFcpF4r5R9K6flM2akINjvFnP6h2xOCZvfX1FErb18RTEIcWDbD1J+lXnQsFNMrw' \
             b'+J1LW5P7BBcFsfPnbckxL/Lp0QT3kdZlKm76LrRWjUdw2ohBzD7R+boq4AQAA'

# Decode the code string
contents = base64.b64decode(nbt_string)
contents = gzip.decompress(contents)
contents = json.loads(contents)
contents = json.dumps(contents, indent=4)
contents = json.loads(contents)

# print(contents)
# print(contents['blocks'][1]['args']['items'][1]['item']['data']['name'])

# Write the heightmap to a string
im = Image.open('input\\height.png')
height_data = im.load()

height_string = ''
for x in range(301):
    for y in range(301):
        height_string += str(height_data[x, y][0]) + '/'


# Insert the height string into a codeblock
class TextValue:
    def __init__(self, value, slot):
        self.entry = {'item': {'id': 'txt', 'data': {'name': value}}, 'slot': slot}

prev_value = 0
true_index = 0
for i in range(0, len(height_string), 10000):
    true_index += 1
    contents['blocks'][1]['args']['items'].append(TextValue(height_string[i:i+10000], true_index).entry)
    print('wtf')
    print(f'Content: {contents} \n')

# Re encode the code string
contents_string = json.dumps(contents)
contents_bytes = contents_string.encode('utf-8')

output = gzip.compress(contents_bytes)
output = base64.b64encode(output)

with open('output\\heightmap.txt', 'w') as f:
    f.write(output.decode('utf-8'))


