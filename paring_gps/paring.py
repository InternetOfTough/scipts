from parse import compile
import csv

f=open('./log.txt', 'r')
gpx=open('./gpslog.gpx','r')

p_g = compile("      <trkpt lat=\"{}\" lon=\"{}\">\n")
p_t = compile("        <time>{}T{}Z</time>\n")
p_t2 = compile("{} +{}\n")
p_sig = compile("          Link Quality={}/70  Signal level={} dBm  \n")
p_essid = compile("wlan0     IEEE 802.11  ESSID:{}  \n")

list_g = []
list_t = []
list_t2 = []
list_sig = []

with open("log_parsed.csv", 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Time(d)','Time(t)', 'Link Quality(/70)','Signal Level(-100)', 'lat', 'lon'])

    lines=gpx.readlines()

    for i in range(len(lines)):

        result_g = p_g.parse(lines[i])
        result_t = p_t.parse(lines[i])

        if result_g!=None:
            # print(result_g[0], result_g[1])
            list_g.append((result_g[0], result_g[1]))
        if result_t!=None :
            juno = result_t[1].split(':')
            tmp = str((int(juno[0])+9)%24) + ':'+str(juno[1])+':'+str(juno[2])
            list_t.append((result_t[0], tmp))

    lines = f.readlines()

    idx=0
    flag = 0
    for i in range(len(lines)):
        if idx>=len(list_t):
            break
        result_t2 = p_t2.parse(lines[i])
        result_essid = p_essid.parse(lines[i])

        if result_t2 != None:
            # print(result_t2[0], result_t2[1])
            if list_t[idx][1] == result_t2[1]:
                list_t2.append((result_t2[0], result_t2[1])) # time
                idx += 1
                flag=1

        if result_essid == "\"halow_demo\"" and flag == 1:
            flag=2
            
        if flag==2:
            list_sig.append((result_essid[0], result_essid[1]))
            flag = 0
            
            

    for i in range(len(list_t)):
        writer.writerow([list_t[i][0], list_t[i][1],list_sig[i][0],list_sig[i][1], list_g[i][0], list_g[i][1]])

gpx.close()
f.close()