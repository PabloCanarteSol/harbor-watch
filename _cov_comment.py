import yaml, sys
P = "/home/harbor-watch/.github/workflows/ci.yml"
W = yaml.safe_load(open(P))
J = W["jobs"]
ts = J["test"]["steps"]
cov_post_step = {
  "name": "Post coverage to PR",
  "if": "${{ github.event_name == 'pull_request' && always() }}",
  "uses": "mrgar...[truncated]