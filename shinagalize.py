from janome.tokenizer import Tokenizer
import re

def shinagalize(text):
    lines = Tokenizer().tokenize(text)

    last = len(lines)
    target = lines[last - 1]
    # print(target.surface, target.part_of_speech)
    if re.search("名詞,サ変接続", target.part_of_speech):
        return ''.join([x.surface for x in lines[0:last]]) + "しながら"
    target = lines[last - 2]
    prefix = ''.join([x.surface for x in lines[0:last - 2]])
    # print(target.surface, target.part_of_speech, target.infl_type)
    if re.search("動詞", target.part_of_speech):
        if target.infl_type == "一段" or re.search("カ変", target.infl_type):
            return prefix + re.sub("る$", "", target.base_form) + "ながら"
        if re.search("サ変.+スル", target.infl_type) :
            return prefix + re.sub("する$", "し", target.base_form) + "ながら"
        if re.search("サ変.+ズル", target.infl_type) :
            return prefix + re.sub("ずる$", "じ", target.base_form) + "ながら"
        m = re.search("五段・(.)行", target.infl_type)
        if m:
            mappings = [
                "アいう", "カきく", "ガぎぐ", "サしす", "タちつ",
                "ナにぬ", "バびぶ", "マみむ", "ラりる", "ワいう"
            ]
            m =  m.group(1)
            for mapping in mappings:
                if mapping[0] == m:
                    return prefix + re.sub(mapping[2] + "$", mapping[1], target.base_form) + "ながら"

    if re.search("特殊・タ", target.infl_type):
        return prefix + ("ても" if target.base_form == "た" else "でも")
    if re.search("特殊・ダ", target.infl_type):
        return prefix + "でも"
    if re.search("特殊・ナイ", target.infl_type):
        return prefix + "ずに"
    return text + "しながら"
