"""
import argparse
from fontTools.ttLib import TTFont, TTCollection
def parse_args():
    parser = argparse.ArgumentParser(description='font redirectorv1')
    parser.add_argument('--content',required=True,help='target text content')
    parser.add_argument('--font',required=True,help='source font file')
    parser.add_argument('--output',required=True,help='dest font output')
    return parser.parse_args()

def read_font(font_path):
    # support more types other than ttf later
    font = TTFont(font_path)
    aa = TTCollection(font_path)
    aa.fonts
    return font

"""
from fontTools.ttLib import TTFont
import random
import json

def generate_ref(cmap, source):
    hits = {}
    refs = {}
    for char in source:
        hits[char] = True
        new_ord = random.choice(cmap)
        while hits.get(new_ord):
            new_ord = random.choice(cmap)
        hits[new_ord] = True
        refs[char] = new_ord
    return refs


def generate_single_ttfont(ttfont, source):
    srcs = [ord(char) for char in source]
    cmap = ttfont.getBestCmap()
    cmapkeys = list(cmap.keys())
    refs = generate_ref(cmapkeys, srcs)
    for k, v in refs.items():
        cmap[v] = cmap[k]
    return source, "".join([chr(refs[char]) for char in srcs])


def generate(content, font_path, dest_path):
    enc_res_list = []
    if font_path.endswith(".ttf") or font_path.endswith(".otf"):
        font = TTFont(font_path)
        origin, encrypted = generate_single_ttfont(font, content)
        enc_res_list.append({
            'origin' : origin,
            'encrypted' : encrypted
        })
        font.save(dest_path)
        
    else:
        raise NotImplementedError("还没做")
    with open(f'{font_path}_ref.json','w', encoding='utf-8') as f:
        f.write(json.dumps(enc_res_list, ensure_ascii=False, indent=4))


generate('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.:,;\'\"(!?)+-*/=中国智造，慧及全球','simhei.ttf','encrypted.ttf')
