import re
import csv
from datetime import datetime, timedelta

gpslogfile = './log/gpslog.gpx'
netlogfile = './log/temp-log.txt'
net_gps_file = "log_parsed.csv"

# GPS 좌표 표현식
gps_expression = re.compile(r"<trkpt lat=\"(.*?)\" lon=\"(.*?)\">")
# GPS 시간 표현식
gps_time_expression = re.compile(r"<time>(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z</time>")
# 네트워크 시간 표현식
net_time_expression = re.compile(r"(\d{2}/\d{2}/\d{2}) \+(\d{2}:\d{2}:\d{2})")
# 네트워크 상황 표현식
net_stat_expression = re.compile(r"Link Quality=(\d+)/70  Signal level=(-\d+) dBm")

lat_lons = []
gps_times = []
net_times = []
net_stats = []


gpx = open(gpslogfile, 'r', encoding='utf-8')
lines = gpx.readlines()
is_before_trkseg = True  # <trkseg> 이전 상태를 나타내는 플래그
for line in lines:
    if is_before_trkseg:
        # <trkseg> 태그인지 확인
        if '<trkseg>' in line:
            is_before_trkseg = False
        continue
    result_g = gps_expression.search(line)
    if result_g:
        lat_lons.append((result_g.group(1), result_g.group(2)))
        continue
    result_t = gps_time_expression.search(line)
    if result_t:
        # 시간을 파싱하여 datetime 객체로 변환
        time_str = result_t.group(1)
        gps_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        # 9시간 추가
        gps_time += timedelta(hours=9)
        # 변환된 시간을 다시 문자열로 변환하여 리스트에 추가
        gps_times.append(gps_time.strftime('%Y-%m-%d %H:%M:%S'))        
gpx.close()
# print(lat_lons, len(lat_lons))
# print(gps_times, len(gps_times))
gps_lat_lon_pairs = []
for i in range(len(gps_times)):
    if i < len(lat_lons):
        gps_lat_lon_pairs.append((gps_times[i], lat_lons[i][0], lat_lons[i][1]))
# print(gps_lat_lon_pairs, len(gps_lat_lon_pairs))

f = open(netlogfile, 'r')
lines = f.readlines()
is_net_stat_turn = False
for i in range(len(lines)):
    result_t2 = net_time_expression.search(lines[i])
    result_stat2 = net_stat_expression.search(lines[i])
    # 시간 읽을 차례에 시간이 오면
    if is_net_stat_turn is False and result_t2:
        time_str = result_t2.group(1) + ' ' + result_t2.group(2)
        net_time = datetime.strptime(time_str, '%m/%d/%y %H:%M:%S')
        net_time_str = net_time.strftime('%Y-%m-%d %H:%M:%S')
        net_times.append(net_time_str)
        is_net_stat_turn = True
        continue
    # net_stat읽을 차례에 시간이 오면
    elif is_net_stat_turn is True and result_t2:
        net_stats.append(('',''))
        time_str = result_t2.group(1) + ' ' + result_t2.group(2)
        net_time = datetime.strptime(time_str, '%m/%d/%y %H:%M:%S')
        net_time_str = net_time.strftime('%Y-%m-%d %H:%M:%S')
        net_times.append(net_time_str)
        is_net_stat_turn = True
    # net_stat 읽을 차례에 net_stat이 오면
    if result_stat2:
        # Signal level과 Link quality를 추출하여 리스트에 추가
        signal_level = result_stat2.group(2)
        link_quality = result_stat2.group(1)
        net_stats.append((link_quality, signal_level))
        is_net_stat_turn = False
f.close()
# print(net_times, len(net_times))
# print(net_stats, len(net_stats))
net_stat_pairs = []
for i in range(len(net_times)):
    if i < len(net_stats):
        if net_times[i]:
            net_stat_pairs.append((net_times[i], net_stats[i][0], net_stats[i][1]))
# print(net_stat_pairs, len(net_stat_pairs))

combined_pairs = []
# gps_lat_lon_pairs를 기준으로 동일한 시간대의 net_stat_pairs를 찾아서 결합
for gps_time, lat, lon in gps_lat_lon_pairs:
    for net_time, quality, level in net_stat_pairs:
        if gps_time == net_time:
            combined_pairs.append((gps_time, lat, lon, quality, level))
            break  # 동일한 시간대를 찾았으면 중단하고 다음 gps 시간으로 넘어감
# print(combined_pairs, len(combined_pairs))

with open(net_gps_file, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'lat', 'lon', 'Link_Quality(/70)', 'Signal_Level(-100)'])

    for pairs in combined_pairs:
        writer.writerow(pairs)