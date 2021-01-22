import re


def convert_partial_cmd(cmd):
    tokens = cmd.split()
    conditions = tuple(get_partial_check_func(i, token) for i, token in enumerate(tokens) if '*' in token)
    cmd = ' '.join('_' if '*' in token else token for token in tokens)
    return cmd, conditions


def get_partial_check_func(i, token):
    def check(tokens):
        return regexp.fullmatch(tokens[i])
    regexp = re.compile(token.replace('.', r'\.').replace('*', r'.*'))
    return check
