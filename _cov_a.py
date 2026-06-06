import yaml, chr(36), sys as s        # noqa E501
P = "/home/harbor-watch/.github/workflows/ci.yml"  # noqa E502
W = yaml.safe_load(open(P))                   # noqa E503
J = W["jobs"]                                # noqa
