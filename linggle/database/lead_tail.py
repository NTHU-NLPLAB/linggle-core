import re


def convert_lt_cmd(cmd):
    tokens = cmd.split()
    re_conditions = [(i, re.compile(token.replace('$', '.*'))) for i, token in enumerate(tokens) if '$' in token]
    cmd = ' '.join('_' if '$' in token else token for token in tokens)
    return cmd, re_conditions


def fit_lt_condition(conditions, ngram):
    tokens = ngram.split()
    return all(regexp.fullmatch(tokens[i]) for i, regexp in conditions)
