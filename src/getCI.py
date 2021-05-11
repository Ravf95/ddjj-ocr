from json import load
from re import findall
from re import search
from re import compile

def is_cedula(str):
    return search('[0-9\.\,]{5,}', str)

def extract(str):
    m = findall('[0-9\.\,]{5,}', str)
    if len(m) >  0:
        ci = m[0].strip().replace('.', '').replace(',', '')
        if ci.isnumeric():
            print(ci)

def getData(data):
    blocks = data['Blocks']
    line = []

    for block in blocks:
        type = block['BlockType']
        if type == 'LINE':
            text = block['Text']
            if is_cedula(text):
                extract(text)

def main():
    blockfile = './block.json'
    with open(blockfile, 'r') as f:
        data = load(f)
    getData(data)
    
if __name__ == "__main__":
    main()
