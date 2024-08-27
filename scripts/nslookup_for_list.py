from nslookup import Nslookup
from tabulate import tabulate

dns_list = open('scripts/data/nslookup_for_list.txt', 'r')
dns_query = Nslookup()

data = []

for line in dns_list.readlines():
    domain = line.split('/')[0]
    ips_record = dns_query.dns_lookup(domain)

    if ips_record.response_full:
        data.append([
            ips_record.response_full[0].split(' ')[0],
            ' '.join(ips_record.answer)
        ])

print(tabulate(data, headers=['Domain', 'IP']))
