def connect(ssid, password):
    import network
    import time
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    
    for i in range (20):
        if station.isconnected():
            break
        time.sleep(0.1)
    return station