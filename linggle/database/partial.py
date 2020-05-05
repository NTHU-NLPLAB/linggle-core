import re


def convert_partial_cmd(cmd):
    tokens = cmd.split()
    re_conditions = [(i, re.compile(token.replace('*', '.*')))
                     for i, token in enumerate(tokens) if '*' in token]
    cmd = ' '.join('_' if '*' in token else token for token in tokens)
    return cmd, re_conditions


def fit_partial_condition(conditions, ngram):
    tokens = ngram.split()
    return all(regexp.fullmatch(tokens[i]) for i, regexp in conditions)
