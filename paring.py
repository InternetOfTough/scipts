import regex
import time
from parse import compile

f=open('/home/pi/log.txt', 'r')
gpx=open('/home/pi/gpslog.gpx','r')

list_g = []
list_t = []

p_g = compile("      <trkpt lat=\"{}\" lon=\"{}\">\n")
p_t = compile("        <time>{}</time>\n")
while 1:
    line=str(gpx.readline())

    result_g = p_g.parse(line)
    result_t = p_t.parse(line)

    if result_g!=None:
        print(result_g[0], result_g[1])
        list_g.append((result_g[0], result_g[1]))
    if result_t!=None :
        print(result_t[0])
        list_t.append(result_t[0])

        
    time.sleep(0.1)

