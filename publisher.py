import paho.mqtt.client as mqtt
import json
import os
loadavg_fs = open("/proc/loadavg",'r')
meminfo_fs = open("/proc/meminfo",'r')

#print fs.read()
alloc_mem = 0
free_mem = 0;
host = "127.0.0.1"
topic = "PyPaho/temperature"
port = 1883
keepalive = 30
bind_addr = ""
mqtt_client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311)
mqtt_client.connect_async(host, port, keepalive, bind_addr)
mqtt_client.loop_start()

def calc_meminfo():
    meminfo_fs.seek(0)
    lines = meminfo_fs.readlines()
    for line in lines:
        if (line.split(": ")[0] == "MemTotal"):
            alloc_mem = line.split(": ")[1]
        if (line.split(": ")[0] == "MemFree"):
            free_mem = line.split(": ")[1]
    memdata = {
        "Allocated memory" : alloc_mem,
        "Free memory": free_mem,
    }
    return memdata

def calc_cpuload():
    loadavg_fs.seek(0)
    cpuload = loadavg_fs.read()
    cpuloadAvg = {
    '1 min avg': cpuload.split(" ")[0],
    '5 min avg': cpuload.split(" ")[1],
    '15 min abg': cpuload.split(" ")[2],
    }

    return cpuloadAvg

while True:
    cpuloadAvg = calc_cpuload()
    memdata = calc_meminfo()
    data = {
        'cpuload_average':cpuloadAvg,
        'memory_data':memdata
    }

    json_str = json.dumps(data)
    mqtt_client.publish(topic,json_str)
mqtt_client.disconnect