from parse import compile
import csv

gpslogfile = './gpslog.gpx'
netlogfile = './log.txt'
net_gps_file = "log_parsed.csv"

gps_expression = compile("      <trkpt lat=\"{}\" lon=\"{}\">\n")
gps_time_expression = compile("        <time>{}T{}Z</time>\n")

net_time_expression = compile("{} +{}\n")
net_stat_expression = compile("          Link Quality={}/70  Signal level={} dBm  \n")
essid_expression = compile("wlan0     IEEE 802.11  ESSID:{}  \n")

lat_lons = []
gps_times = []
net_times = []
net_stats = []

with open(net_gps_file, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Time(d)','Time(t)', 'Link Quality(/70)','Signal Level(-100)', 'lat', 'lon'])

    gpx=open(gpslogfile,'r')
    lines=gpx.readlines()

    for i in range(len(lines)):

        result_g = gps_expression.parse(lines[i])
        result_t = gps_time_expression.parse(lines[i])

        if result_g != None:
            # print(result_g[0], result_g[1])
            lat_lons.append((result_g[0], result_g[1]))
        if result_t != None :
            juno = result_t[1].split(':')
            tmp = str((int(juno[0])+9)%24) + ':'+str(juno[1])+':'+str(juno[2])
            gps_times.append((result_t[0], tmp))

    f=open(netlogfile, 'r')
    lines = f.readlines()

    idx=0
    flag = 0
    for i in range(len(lines)):
        if idx>=len(gps_times):
            break
        result_t2 = net_time_expression.parse(lines[i])
        result_essid = essid_expression.parse(lines[i])

        if result_t2 != None:
            # print(result_t2[0], result_t2[1])
            if gps_times[idx][1] == result_t2[1]:
                net_times.append((result_t2[0], result_t2[1])) # time
                idx += 1
                flag=1

        if result_essid == "\"halow_demo\"" and flag == 1:
            flag=2
            
        if flag==2:
            net_stats.append((result_essid[0], result_essid[1]))
            flag = 0
            
            

    for i in range(len(gps_times)):
        writer.writerow([gps_times[i][0], gps_times[i][1],net_stats[i][0],net_stats[i][1], lat_lons[i][0], lat_lons[i][1]])

gpx.close()
f.close()