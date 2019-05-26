import Adafruit_DHT
 
#configuracao do sensor de temperatura utilizado (DHT22)
sensor = Adafruit_DHT.DHT22  
 
#configuracao do pino de leitura do sensor de temperatura
pin = 'P8_11'
 
Leitura = 1
 
while(True):
    try:
        #faz leitura do sensor de temperatura e umidade
        umidade, temperatura = Adafruit_DHT.read_retry(sensor, pin)
 
        #formata string de umidade e temperatura
        UmidadeStr = "{0:0.1f}".format(umidade) 
        TemperaturaStr = "{0:0.1f}*C".format(temperatura) 
        print "Leitura "+str(Leitura)+": "+TemperaturaStr+" - "+UmidadeStr
        Leitura = Leitura + 1
    except KeyboardInterrupt:
        print "Aplicacao encerrada."
exit(1)