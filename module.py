from wifi_lib import connect

import dht
import machine
import urequests
import time

ssid = input("Digite o nome da rede que deseja se conectar: ")
password = input("Digite a senha da respectiva rede: ")

print("Aguardando conexão...")

station = connect(ssid, password)

if not station.isconnected():
    print("Não foi possível se conectar. Valide os dados inseridos e tente novamente.")
else:
    print("Conexão realizada com sucesso!")
    
    api_key = input("Digite a sua chave API Key do Thingspeak: ")

    d = dht.DHT11(machine.Pin(4))
    r = machine.Pin(2, machine.Pin.OUT)

    r.value(0)

    quantity = int(input("Digite a quantidade de leituras que deseja fazer(10s-10s / 3840: 1 dia): "))
    
    print("Iniciando a extração de dados...")
    
    print("Extração de dados em andamento...")
    
    for i in range(quantity):
        print("Iteração/index:", i)
        d.measure()
        
        if (d.temperature() > 31 or d.humidity() > 70) and r.value() == 0:
            r.value(1)

        if (d.temperature() <= 31 and d.humidity() <= 70) and r.value() == 1:
            r.value(0)

        print("{}.".format(i + 1), (" " * (len(str(quantity)) - len(str(i + 1)))), "Temperatura = {}°C    Umidade = {}%".format(d.temperature(), d.humidity()))

        response = urequests.get("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}".format(api_key, d.temperature(), d.humidity(), r.value()))

        response.close()

        if (i < quantity - 1):
            time.sleep(10)

    station.disconnect()