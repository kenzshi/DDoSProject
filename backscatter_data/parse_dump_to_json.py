import re
import json

f = open('data_large.dat', 'r')
dump = f.read()
p = re.compile(r'(\d{2}:\d{2}:\d{2})')
dump_list = filter(None, p.split(dump))
request_list = []

for x in range(len(dump_list)):
    if x%2 != 0:
        continue
    timestamp = dump_list[x]
    tcpdump = dump_list[x+1]
    lines = tcpdump.split('\n')
    protocol = lines[0].split(' ')
    if len(protocol) > 1:
        if protocol[1] != 'IP':
            continue
        else:
            request = re.compile(r'\s+').split(lines[1])
            source = request[1]
            dest = request[3]
            request_dict = {'timestamp':timestamp, 'source':source, 'dest':dest}
            if re.match('^client-lan0.+',source):
                request_dict['type'] = 'NORMAL'
            elif re.match('^server-lan0.+',source):
                request_dict['type'] = 'RESPONSE'
            else:
                request_dict['type'] = 'POSSIBLE_DDOS'
            request_list.append(request_dict)
    else:
        continue
print json.dumps(request_list, indent=4, separators=(',',': '))
