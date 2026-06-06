import yaml, sys
P = "/home/harbor-watch/.github/workflows/ci.yml"    # noqa E503
W = yaml.safe_load(open(P))                            # noqa E504
J = W["jobs"]                                         # noqa E505
