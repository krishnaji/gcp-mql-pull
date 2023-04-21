
import requests

# Config
MQL_QUERYS = {
"instance/cpu/utilization":
"""
fetch gce_instance::compute.googleapis.com/instance/cpu/utilization
| bottom 3, max(val()) | within 10m
""",
"https/request_count":
"""
fetch https_lb_rule
| metric 'loadbalancing.googleapis.com/https/request_count'
| align rate(1m)
| every 1m
| group_by [], [value_request_count_mean: max(value.request_count)]
| within 10m
"""
}

QUERY_URL = "https://monitoring.googleapis.com/v3/projects/gke-projects-372400/timeSeries:query"

def mql_result(token,query):
    q = f'{{"query": "{query}"}}'
    print(q)
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {token}"}
    return requests.post(QUERY_URL, data=q, headers=headers).json()

token = input("Paste you Auth token here:")
result = mql_result(token, MQL_QUERYS['instance/cpu/utilization'])
print(result)
result = mql_result(token, MQL_QUERYS['https/request_count'])
print(result)
