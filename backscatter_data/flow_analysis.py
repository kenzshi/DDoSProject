import re, json, csv

TIMEOUT_PERIOD = 5 

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

flows = []
cur_flow = []
for request in request_list:
    if request['type'] != 'POSSIBLE_DDOS':
        continue
    if len(cur_flow) == 0:
        cur_flow.append(request)
        continue
    cur_req_ts = request['timestamp'].split(':')
    cur_req_ts = int(cur_req_ts[0])*3600 + int(cur_req_ts[1])*60 + int(cur_req_ts[2])
    prev_req_ts = cur_flow[-1]['timestamp'].split(':')
    prev_req_ts = int(prev_req_ts[0])*3600 + int(prev_req_ts[1])*60 + int(prev_req_ts[2])
    if cur_req_ts - prev_req_ts < TIMEOUT_PERIOD:
        cur_flow.append(request)
    else:
        flows.append(cur_flow)
        cur_flow = []

csv_file = open('data_flow_'+str(TIMEOUT_PERIOD)+'.csv', 'wb+')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['start','end','num_packets'])
for flow in flows:
    print '{0}; {1}; {2}'.format(flow[0]['timestamp'],flow[-1]['timestamp'],len(flow))
    csv_writer.writerow([flow[0]['timestamp'],flow[-1]['timestamp'],len(flow)])
csv_file.close()
