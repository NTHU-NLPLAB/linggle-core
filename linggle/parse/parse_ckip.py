
def parse_ckip_abbr(line):
    un, abbr, simpleTag, ckipTags = line.strip().split('\t')
    # ckipTags = ckipTags.split(', ')
    return abbr, simpleTag
