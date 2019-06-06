# encoding: utf-8 #Usar caracteres especiais nos comentários
from Tkinter import * #Importar biblioteca grafica TK Inter

import Adafruit_DHT #Importar biblioteca Adafruit_DHT para trabalhar com o sensor DHT22
import Adafruit_BBIO.GPIO as GPIO #Importar biblioteca Adafruit_BBIO para trabalhar com os botões
import requests #Importar requests para obter informação de um site
import json #Importar a biblioteca json própria para trabalhar com dados no formato json
import feedparser #Importar biblioteca para organizar feed de notícias
import googlemaps #Importar biblioteca para obter as rotas
import time #Importar biblioteca do tempo

from datetime import datetime #Importar a classe datetime do módulo datetime para trabalhar com horas

from PIL import Image, ImageTk #PIL eh uma biblioteca de manipulação de imagens para o Python
			       #ImageTk eh um modulo que contem o suporte para criar e modificar objetos TkInter

#Configuração do sensor de temperatura utilizado (DHT22)
sensor = Adafruit_DHT.DHT22
#Configuração do pino de leitura do sensor de temperatura
pin = 'P8_11'

#Configuração dos pinos utilizados pelos botões de mudança de cor e mudança de perfil:
GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_14", GPIO.IN)

#Criação de uma classe auxilar para fazer a troca de perfis e cores do display
class aux():
    pushbutton = 0
    color ="white"
    change_prof = 0

#Caro usuário, nesse momento você deve criar um token para poder captar as informações de previsão do tempo
#Recomendamos o site darksky.net, após acessá-lo basta clicar em Dark Sky API, se registrar e obter seu próprio token 
weather_api_token = '4ecc5df768c626180a20aa8bfdc0db96' #Substitua esse token pelo seu token criado
#O usuário pode definir a latitude e longitude manualmente ou pegá-las pelo IP. Caso for adquirir as informações com base no IP,
#é necessário utilizar uma API, para isso sugerimos o site: ipstack.com, basta se registar, garantir seu token e substituir na
#variável abaixo com nome ip_token. (Obs.: Utilizamos o ip para obter as informações de localização)
ip_token = '33a23fcdf35dc1446075208d4461cfec' #Substitua esse token pelo seu token criado
#Para adquirir as informações de rota, vamos utilizar uma API do google maps, para isso é necessário que o usuário crie sua chave
#de acesso no site https://cloud.google.com/maps-platform/?hl=pt-br, basta clicar em primeiros passos, selecionar a opção Routes
#e seguir os passos sequentes para se cadastrar. Em seguida cole seu código chave na variável googlemaps_key abaixo.
googlemaps_key = 'AIzaSyBiNUWP5FbEKdByztRyhINuDCjfemldWlg' #Substitua esse código de acesso pelo que você criou
latitude = None #Definindo latitude como nula (para usar o IP)	
longitude = None #Definindo longitude como nula (para usar o IP)
#Definindo o tamanho das letras a serem utilizadas:
texto_gg = 94
texto_grande = 48
texto_medio = 28
texto_pequeno = 10
texto_pp = 10

#Atribuindo as imagens às respectivas variáveis:
pic_lookup = {
    'clear-day': "assets/Sun.png",  # Limpo
    'wind': "assets/Wind.png",   # Vento
    'cloudy': "assets/Cloud.png",  # Lublado
    'partly-cloudy-day': "assets/PartlySunny.png",  # Parcialmente nublado
    'rain': "assets/Rain.png",  # Chuvoso
    'snow': "assets/Snow.png",  # Neve
    'snow-thin': "assets/Snow.png",  # Neve fina
    'fog': "assets/Haze.png",  # Neblina
    'clear-night': "assets/Moon.png",  # Noite limpa
    'partly-cloudy-night': "assets/PartlyMoon.png",  # Noite parcialmente nublada
    'thunderstorm': "assets/Storm.png",  # Tempestade de trovões
    'tornado': "assests/Tornado.png",    # Tornado
    'hail': "assests/Hail.png"  # Granizo
}

#Criar a classe abaixo para construir o label das horas
class Clock(Frame): #Frame é a classe pai
    def __init__(self, master = None): # Definir o construtor da classe e inicializar o objeto self e seus atributos
        Frame.__init__(self, master) #Chamar o construtor da classe pai
        self.widget = Frame(self) #Criação de um atributo widget para o objeto self
        self.widget["bg"] = ("black") #Definir a cor do plano de fundo para preto
        self.widget.pack(side=TOP) #Posicionar o widget

	        # Inicializar label de tempo
        self.time1 = ''
        self.timelbl = Label(self.widget, text = self.time1) #Label é uma função do TkInter para exibir um widget, self.widget é o widget pai
        self.timelbl["font"] = ("Helvetica", texto_grande) #Definir fonte e tamanho
        self.timelbl["bg"] = ("black") #Definir cor do plano de fundo
        self.timelbl["fg"] = ("white") #Definir cor da letra
        self.timelbl.pack(side=TOP, anchor=E) #Posicionar o label

            # Inicializar label de dia da semana
		#Mesma lógica do label de tempo
        self.d_of_w1 = ''
        self.d_of_wlbl = Label(self.widget, text = self.d_of_w1) 
        self.d_of_wlbl["font"] = ("Helvetica", texto_pequeno)
        self.d_of_wlbl["bg"] = ("black")
        self.d_of_wlbl["fg"] = ("white")
        self.d_of_wlbl.pack(side=TOP, anchor=E)

            # Inicializar label de data
		#Mesma lógica do label de tempo e de dia da semana
        self.date1 = ''
        self.datelbl = Label(self.widget, text = self.date1)
        self.datelbl["font"] = ("Helvetica", texto_pequeno)
        self.datelbl["bg"] = ("black")
        self.datelbl["fg"] = ("white")
        self.datelbl.pack(side=TOP, anchor=E)
	
        self.att() #Chamar o método att

    def att(self):

	now = datetime.now() #Captar a hora e data atual
	time2 = now.strftime("%H:%M") #Formatar o dado para pegar a hora em string
	d_of_w2 = now.strftime("%A") #Formatar o dado para pegar os dias da semana em string
	#Simples conversão para o pt-br:
	if d_of_w2 == "Sunday":		d_of_w2 = "Domingo"
	if d_of_w2 == "Saturday":	d_of_w2 = "Sabado"
	if d_of_w2 == "Monday":		d_of_w2 = "Segunda-feira"
	if d_of_w2 == "Tuesday":	d_of_w2 = "Terca-feira"
	if d_of_w2 == "Wednesday":	d_of_w2 = "Quarta-feira"
	if d_of_w2 == "Thursday":	d_of_w2 = "Quinta-feira"
	if d_of_w2 == "Friday":		d_of_w2 = "Sexta-feira"
	date2 = now.strftime("%d/%m/%Y") #Formatar o dado para pegar a data em string

        # Verificar para atualizar
	if time2 != self.time1:
        	self.time1 = time2
                self.timelbl.config(text=time2) #Atualizando o label com o valor atual

        if d_of_w2 != self.d_of_w1:
                self.d_of_w1 = d_of_w2
                self.d_of_wlbl.config(text=d_of_w2) #Atualizando o label com o valor atual

        if date2 != self.date1:
                self.date1 = date2
                self.datelbl.config(text=date2) #Atualizando o label com o valor atual
        
        self.timelbl.after(200, self.att) #Define um tempo para atualizar novamente o label de horas


#Criação da classe Weather para captar as informações de previsão do tempo
#Sua declaração e inicialização é similar à explicada para a classe Clock
class Weather(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master, bg='black')
	#definição dos atributos necessários:
        self.temp = ''
        self.local = ''
        self.prev = ''
        self.atual = ''
        self.pic = ''
        self.tempamb = ''
        self.umid = ''


        self.widget_clima = Frame(self) #Obs: Utilizar Frame(master) criaria um widget dominante na região impedindo a divisão de tela com o widget de horas
        self.widget_clima["bg"] = ("black") #Definir cor do plano de fundo
        self.widget_clima.pack(side=TOP, anchor=W) #Definir posionamento e orientação
	
	#Criação do label que contém a temperatura e a figura
        self.widget_plot = Label(self.widget_clima) #Criação de um label filho de self.widget_clima
        self.widget_plot["bg"] = ("black") #Definir cor do plano de fundo
        self.plotClima() #Chamar o método encarregado de plotar a temperatura e sua figura
        self.widget_plot.pack(side=TOP, anchor=N) #Definir posicionamento e orientação
	
	#Criação do label de condição atual do tempo
        self.atuallbl = Label(self.widget_clima)  #Criação de um label filho de self.widget_clima
        self.atuallbl["font"] = ("Helvetica", texto_medio) #Definir características da fonte
        self.atuallbl["bg"] = ("black") #Definir cor do plano de fundo
        self.atuallbl["fg"] = ("white") #Definir cor da letra
        self.atuallbl.pack(side=TOP, anchor=W) #Definir o posicionamento e orientação
	
	#Criação do label de condição futura do tempo (estrutura semelhante a criada acima para a condição atual do tempo)
        self.prevlbl = Label(self.widget_clima)
        self.prevlbl["font"] = ("Helvetica", texto_pequeno)
        self.prevlbl["bg"] = ("black")
        self.prevlbl["fg"] = ("white")
        self.prevlbl.pack(side=TOP, anchor=W)
	
	#Criação do label de localização da previsão (estrutura semelhante a criada acima para a condição atual do tempo)
        self.locallbl = Label(self.widget_clima)
        self.locallbl["font"] = ("Helvetica", texto_pequeno)
        self.locallbl["bg"] = ("black")
        self.locallbl["fg"] = ("white")
        self.locallbl.pack(side=TOP, anchor=W)
        
	#Criação do label de temperatura ambiente (estrutura semelhante a criada acima para a condição atual do tempo)
        self.tempamblbl = Label(self, text=self.tempamb)
        self.tempamblbl["font"] = ("Helvetica", texto_pequeno)
        self.tempamblbl["bg"] = "black"
        self.tempamblbl["fg"] = aux.color #Mudança da cor da letra
        self.tempamblbl.pack(side=TOP, anchor=W)
        
	#Criação do label de umidade ambiente (estrutura semelhante a criada acima para a condição atual do tempo)
        self.umidlbl = Label(self, text=self.umid)
        self.umidlbl["font"] = ("Helvetica", texto_pequeno)
        self.umidlbl["bg"] = "black"
        self.umidlbl["fg"] = aux.color #Mudança da cor da letra
        self.umidlbl.pack(side=TOP, anchor=W)

        try: 
            #faz leitura do sensor de temperatura e umidade
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

            #formata string de umidade e temperatura
            umid2 = "Umidade do ar: {0:0.1f}%".format(humidity)
            grau= u'\N{DEGREE SIGN}'
            tempamb2 = "Temperatura ambiente: {0:0.1f}%sC".format(temperature) % (grau)
		
            if self.tempamb != tempamb2:
		#Atualiza a temperatura ambiente
                self.tempamb = tempamb2
                self.tempamblbl.config(text=tempamb2)

            if self.umid != umid2:
		#Atualiza a umidade ambiente
                self.umid = umid2
                self.umidlbl.config(text=umid2)
            
        except Exception as e: #Exception as e: da para acessar o conteudo do objeto exception = e
            print "Error: %s. Cannot get sensor." % e


        self.get_weather() #Chamar método para fazer aquisição das informações

    def plotClima(self):
        
	#Obs.: Foi necessário criar o método para fazer o posicionamento das informações no display conforme desejado
        self.templbl = Label(self.widget_plot) #Criar um label filho de self.widget_plot
        self.templbl["font"] = ("Helvetica", texto_gg) #Definir características de fonte
        self.templbl["bg"] = ("black") #Definir cor do plano de fundo
        self.templbl["fg"] = ("white") #Definir cor da letra
        self.templbl.pack(side=LEFT, anchor=N) #Definir posicionamento e orientação

        self.piclbl = Label(self.widget_plot) #Criar um label filho de self.widget_plot
        self.piclbl["bg"] = ("black") #Definir cor do plano de fundo
        self.piclbl.pack(side=LEFT, anchor=N, padx=20) #Definir posicionamento e orientação

	
    def get_ip(self): #Método para pegar o ip
        try:
            ip_url = "http://jsonip.com/" #Site usado para pegar o ip
            req = requests.get(ip_url) #requests.get usado para obter as informações do site
            ip_json = json.loads(req.text) # json.loads é uma função própria para carregar arquivos com strings
            return ip_json['ip'] #Com a atribuição feita acima, ip_json virou uma espécie de dicionário e seus campos podem ser acessados como foi feito nesta linha
        except Exception as e:	#Exception as e: da para acessar o conteudo do objeto exception = e
           return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:
            if latitude is None and longitude is None:
                # Localização pelo IP
                location_req_url = "http://api.ipstack.com/%s?access_key=%s" % (self.get_ip(), ip_token)
                r = requests.get(location_req_url) #requests.get usado para obter as informações do site
                location_obj = json.loads(r.text) #json.loads é uma função própria para carregar arquivos com strings

                lat = location_obj['latitude'] # Acessando o campo de latitude
                lon = location_obj['longitude'] # Acessando o campo de longitude

                local2 = "%s, %s" % (location_obj['city'], location_obj['region_code']) #formatando a localização

                # Pegar o clima
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=pt&units=si" % (weather_api_token, lat, lon)
            else:
		#Localização já definida pelo usuário
                local2 = ""
                # Pegar o clima
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=pt&units=si" % (weather_api_token, latitude, longitude)
	
		#Captando informações do URL:
            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)
	
            grau= u'\N{DEGREE SIGN}' #Símbolo de grau
            temp2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), grau) #Formatando a temperatura
            atual2 = weather_obj['currently']['summary'] #Acessando os campos para pegar condição atual do tempo
            prev2 = weather_obj["hourly"]["summary"] #Acessando os campos para pegar a condição futura do tempo

            pic_id = weather_obj['currently']['icon'] #Acessando os campos para pegar a informação da figura
            pic2 = None
		
		#Inserindo figura
            if pic_id in pic_lookup:
                pic2 = pic_lookup[pic_id]

            if pic2 is not None:
                if self.pic != pic2:
			#Atualizar a figura
                    self.pic = pic2
                    image = Image.open(pic2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)
		
			#Atualizar o label
                    self.piclbl.config(image=photo)
                    self.piclbl.image = photo
            else:
                # Remover imagem
                self.piclbl.config(image='')
		
		#Atualizar condição atual do tempo
            if self.atual != atual2:
                self.atual = atual2
                self.atuallbl.config(text=atual2)
		
		#Atualizar condição futura do tempo
            if self.prev != prev2:
                self.prev = prev2
                self.prevlbl.config(text=prev2)
		
		#Atualizar a temperatura
            if self.temp != temp2:
                self.temp = temp2
                self.templbl.config(text=temp2)
		
		#Atualizar a localização
            if self.local != local2:
                if local2 == ", ":
                    self.local = "Cannot Pinpoint Location"
                    self.locallbl.config(text="Cannot Pinpoint Location")
                else:
                    self.local = local2
                    self.locallbl.config(text=local2)
        except Exception as e:
            print "Error: %s. Cannot get weather." % e

        self.after(6000, self.get_weather) #Executa novamente o método self.get_weather após 6000ms


#Criação da classe abaixo para exibir o label de Notícias na interface
#Sua declaração e inicialização é semelhante à explicada para a classe Clock
class Noticias(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master, bg='black')
        
        self.manchetes = Frame(self, bg="black") #Definição do atributo manchetes, e definição de sua cor de fundo
        self.manchetes.pack(side=TOP) #Posicionamento do widget      
	
	self.manchetes_url = "http://rss.uol.com.br/feed/noticias.xml" #Endereço RSS fonte das últimas notícias

        self.get_manchete() #Méotodo para fazer a aquisição das notícias


    def get_manchete(self):
        try:
            # Remover todas as notícias que podem estar na tela
            for widget in self.manchetes.winfo_children():
                widget.destroy()
		
		#Abaixo, há uma sequência de lógica if responsável por alterar as notícias que são exibidas, de acordo com os perfis pré configurados
            if aux.change_prof == 0:
                self.titulo = "Ultimas Noticias"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo) #Criar um label filho de self.manchetes que exibe o conteúdo da variável self.titulo
                self.noticiaslbl["font"] = ("Helvetica", texto_medio) #Definir características da fonte
                self.noticiaslbl["bg"] = "black" #Definir cor do plano de fundo
                self.noticiaslbl["fg"] = aux.color #Definir cor da fonte
                self.noticiaslbl.pack(side=TOP, anchor=W) #Posicionar o label
		
		#Exibição das Principais Notícias (construção semelhante a vista acima para as Últimas Notícias):
            if aux.change_prof == 1:
                self.titulo = "Principais Noticias"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo)
                self.noticiaslbl["font"] = ("Helvetica", texto_medio)
                self.noticiaslbl["bg"] = "black"
                self.noticiaslbl["fg"] = aux.color
                self.noticiaslbl.pack(side=TOP, anchor=W) 
		
		#Exibição das Notícias sobre Tecnologia (construção semelhante a vista acima para as Últimas Notícias):
            if aux.change_prof == 2:
                self.titulo = "Tecnologia"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo)
                self.noticiaslbl["font"] = ("Helvetica", texto_medio)
                self.noticiaslbl["bg"] = "black"
                self.noticiaslbl["fg"] = aux.color
                self.noticiaslbl.pack(side=TOP, anchor=W)
		
		#Exibição das Notícias sobre Econômia (construção semelhante a vista acima para as Últimas Notícias):
            if aux.change_prof == 3:
                self.titulo = "Economia"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo)
                self.noticiaslbl["font"] = ("Helvetica", texto_medio)
                self.noticiaslbl["bg"] = "black"
                self.noticiaslbl["fg"] = aux.color
                self.noticiaslbl.pack(side=TOP, anchor=W)

		#Exibição das Notícias de Esportes (construção semelhante a vista acima para as Últimas Notícias):
            if aux.change_prof == 4:
                self.titulo = "Esportes"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo)
                self.noticiaslbl["font"] = ("Helvetica", texto_medio)
                self.noticiaslbl["bg"] = "black"
                self.noticiaslbl["fg"] = aux.color
                self.noticiaslbl.pack(side=TOP, anchor=W)

		#Exibição das Notícias de Jogos (construção semelhante a vista acima para as Últimas Notícias):
            if aux.change_prof == 5:
                self.titulo = "Jogos"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo)
                self.noticiaslbl["font"] = ("Helvetica", texto_medio)
                self.noticiaslbl["bg"] = "black"
                self.noticiaslbl["fg"] = aux.color
                self.noticiaslbl.pack(side=TOP, anchor=W)

		#Exibição das Notícias de Cinema (construção semelhante a vista acima para as Últimas Notícias):
            if aux.change_prof == 6:
                self.titulo = "Cinema"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo)
                self.noticiaslbl["font"] = ("Helvetica", texto_medio)
                self.noticiaslbl["bg"] = "black"
                self.noticiaslbl["fg"] = aux.color
                self.noticiaslbl.pack(side=TOP, anchor=W)

		#Exibição das Notícias sobre Vestibular (construção semelhante a vista acima para as Últimas Notícias):
            if aux.change_prof == 7:
                self.titulo = "Vestibular"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo)
                self.noticiaslbl["font"] = ("Helvetica", texto_medio)
                self.noticiaslbl["bg"] = "black"
                self.noticiaslbl["fg"] = aux.color
                self.noticiaslbl.pack(side=TOP, anchor=W)

		#Exibição das Notícias sobre Música (construção semelhante a vista acima para as Últimas Notícias):
            if aux.change_prof == 8:
                self.titulo = "Musica"
                self.noticiaslbl = Label(self.manchetes, text=self.titulo)
                self.noticiaslbl["font"] = ("Helvetica", texto_medio)
                self.noticiaslbl["bg"] = "black"
                self.noticiaslbl["fg"] = aux.color
                self.noticiaslbl.pack(side=TOP, anchor=W)
                aux.change_prof = 0    
            feed = feedparser.parse(self.manchetes_url) #Capturando rss pelo pelo feedparser
		
		#Exibição de 5 notícias:
            for post in feed.entries[0:5]:
                headline = Manchetes_foto(self.manchetes, post.title) #Função Manchetes_foto será encarregada de configurar a exibição com as figuras
                headline.pack(side=TOP, anchor=W)

        except Exception as e:
            print "Error: %s. Cannot get news." % e

        self.after(600000, self.get_manchete) #Atualizar notícias após 600000ms

#Criação da classe Manchetes para exibição das Manchetes com título e figura
#Sua declaração e inicialização é semelhante à explicada para a classe Clock
class Manchetes_foto(Frame):
    def __init__(self, master= None, event_name=""):
        Frame.__init__(self, master, bg='black')
	#Abrindo a imagem correta, fazendo o tratatamento e atribuindo a variável encarregada
        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
	
	#Criando o label que exibirá a figura e já atribuindo a imagem a ele:
        self.piclbl = Label(self, bg='black', image=photo) 
        self.piclbl.image = photo
        self.piclbl.pack(side=LEFT, anchor=N)
	
        self.eventName = event_name #Recebendo o título
        self.eventNamelbl = Label(self, text=self.eventName, wraplength = 400) #Criando o label para exibir o título
	 #Configurando o widget: fonte, cor de plano de fundo, cor da letra, e fazendo o posicionamento:
        self.eventNamelbl["font"] = ("Helvetica", texto_pequeno)
        self.eventNamelbl["bg"] = "black"
        self.eventNamelbl["fg"] = aux.color
        self.eventNamelbl.pack(side=LEFT, anchor=N)

#Criação da classe responsável pelas Rotas
#Sua declaração e inicialização é semelhante à explicada para a classe Clock
class Rotas(Frame):
    def __init__(self,master = None):
        Frame.__init__(self,master,bg='black')
	
	#Definição do ponto de origem da rota
        self.origin="Avenida Nove de Julho, 3333, Jundiai"
	#Definição do ponto de destino da rota
        self.destination="Joao Carbonari Junior 64"
                
	#Criação do widget rota:
        self.widgetRota = Frame(self)
        self.widgetRota["bg"] = ("black")
        self.widgetRota.pack(side=TOP, anchor=N)

        self.get_url() #Chamar o método responsável por pegar o URL

    def get_url(self):
    	
	#Destruir alguma rota que esteja sendo exibida na tela:
        for widget in self.widgetRota.winfo_children():
             widget.destroy()

	#Obtenção das rotas através da API do google maps:
        gmaps = googlemaps.Client(key=googlemaps_key)
        map_url = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&language=pt-BR&units=metric&region=br&departure_time=now&key=%s" % (self.origin,self.destination,googlemaps_key)
        map_req = requests.get(map_url)
        self.map_obj = json.loads(map_req.text)

	
        self.titulo = "Destino" #Definir o título do widget
        self.rotaslbl = Label(self.widgetRota, text = self.titulo) #Criar o label para exibir o título
	#Configurar características de fonte, plano de fundo, cor da fonte e posicionamento do widget:
        self.rotaslbl["font"] = ("Helvetica", texto_medio) 
        self.rotaslbl["bg"] = "black" 
        self.rotaslbl["fg"] = aux.color
        self.rotaslbl.pack(side=TOP, anchor=W)
        self.get_rota() #Método para exibir as rotas que estão organizadas no formato json em self.map_obj
        self.after(600000, self.get_url) #Definir tempo para atualizar as rotas

    def get_rota(self):
        try:
            
            self.destino = self.map_obj['routes'][0]['legs'][0]['end_address'] #Acessar o campo desejado de endereço
            self.destline = Label(self.widgetRota) #Criar um label filho de self.widgetRota que representa uma linha de instrução da rota
	    #Obs.: É necessário a criação de um label para cada linha, para fazer o plot do destino final com uma figura e
	    #informações de tempo e distância posicionados lado a lado
            self.destline["bg"] = "black" 
            self.plotdest() #Método para plotar o destino
            self.destline.pack(side=TOP, anchor = W) #Posicionamento da linha de instrução
		
		#Acessar as instruções da rota e configurar para exibi-la no display
            for self.step_ in self.map_obj['routes'][0]['legs'][0]['steps']:
                self.step = self.step_['html_instructions']
                for i in range(0,len(self.step)):
                    self.step = self.step.replace("<b>","")
                    self.step = self.step.replace("</b>","")
                    self.step = self.step.replace('<div style="font-size:0.9em">',". ")
                    self.step = self.step.replace("</div>","")
		
		#Assim como self.destline, esse é o label que representa uma linha de instrução, com figura, informação de tempo e distância
                self.stepline = Label(self.widgetRota)
                self.stepline["bg"] = "black"
                self.plotstep()
                self.stepline.pack(side=TOP, anchor=W)
                
        except Exception as e:
            print "Error: %s. Cannot get routes." % e


    
    def plotdest(self):
	
	#Definir a figura que será exibida e configurá-la para exibição:
        image = Image.open("assets/Arrow2.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
	
	#Criação e posicionamento do label da figura:
        self.main_arrowlbl = Label(self.destline, bg='black', image=photo)
        self.main_arrowlbl.image = photo
        self.main_arrowlbl.pack(side=LEFT, anchor=W)

        #Criação e posicionamento do label de destino final da rota:
        self.destinolbl = Label(self.destline, text = self.destino, wraplength = 400)
        self.destinolbl["font"] = ("Helvetica", 12)
        self.destinolbl["bg"] = "black"
        self.destinolbl["fg"] = aux.color
        self.destinolbl.pack(side=LEFT, anchor=W)
	
	#Acessar a distância do percurso e configurar exibição:
        self.dist = self.map_obj['routes'][0]['legs'][0]['distance']['text'] 
        self.dist_str = "(" + self.dist + "," 
	
	#Criação e posicionamento do label de distância:
        self.distlbl = Label(self.destline, text = self.dist_str)
        self.distlbl["font"] = ("Helvetica", texto_pp)
        self.distlbl["bg"] = "black"
        self.distlbl["fg"] = aux.color
        self.distlbl.pack(side=LEFT, anchor=W)
        
	#Acessar o tempo do percurso e configurar exibição:
        self.tempo_est = self.map_obj['routes'][0]['legs'][0]['duration']['text']
        for i in range(0,len(self.tempo_est)):
            self.tempo_est = self.tempo_est.replace("minutos","min")
        self.tempo_est_str = self.tempo_est + ")"
	
	#Criação e posicionamento do label de tempo:
        self.time_estlbl = Label(self.destline, text = self.tempo_est_str)
        self.time_estlbl["font"] = ("Helvetica", texto_pp)
        self.time_estlbl["bg"] = "black"
        self.time_estlbl["fg"] = aux.color
        self.time_estlbl.pack(side=LEFT, anchor=W)


    def plotstep(self):
        
	#Definir a figura que será exibida e configurá-la para exibição:
        image = Image.open("assets/Arrow1.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
	
	#Criação e posicionamento do label da figura:
        self.arrowlbl = Label(self.stepline, bg='black', image=photo)
        self.arrowlbl.image = photo
        self.arrowlbl.pack(side=LEFT, anchor=W)
	
	#Criação e posicionamento do label de instrução do passo:
        self.steplbl = Label(self.stepline, text = self.step, wraplength = 400)
        self.steplbl["font"] = ("Helvetica", texto_pp)
        self.steplbl["bg"] = "black"
        self.steplbl["fg"] = aux.color
        self.steplbl.pack(side=LEFT, anchor=W)
	
	#Acessar a distância do passo e configurar exibição:
        self.step_dist = self.step_['distance']['text']
        self.step_dist_str = "(" + self.step_dist + ","
	
	#Criação e posicionamento do label de distância do passo:
        self.step_distlbl = Label(self.stepline, text = self.step_dist_str)
        self.step_distlbl["font"] = ("Helvetica", texto_pp)
        self.step_distlbl["bg"] = "black"
        self.step_distlbl["fg"] = aux.color
        self.step_distlbl.pack(side=LEFT, anchor=W)
	
	#Acessar o tempo do passo e configurar exibição:
        self.step_temp = self.step_['duration']['text']
        for i in range(0,len(self.step_temp)):
            self.step_temp = self.step_temp.replace("minutos","min")
        self.step_temp_str = self.step_temp + ")"
	
	#Criação e posicionamento do label de tempo do passo:
        self.step_templbl = Label(self.stepline, text = self.step_temp_str)
        self.step_templbl["font"] = ("Helvetica", texto_pp)
        self.step_templbl["bg"] = "black"
        self.step_templbl["fg"] = aux.color
        self.step_templbl.pack(side=LEFT, anchor=W)
    
# Criação da classe FullscreeWindow, ela reunirá todos os elementos que serão exibidos na tela, e terá as funções para a interrupção com os botões.
class FullscreenWindow:

    def __init__(self):
	#Configuração para que seja exibida uma tela completamente preta
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.centerFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.centerFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
	#Configuração do botão enter para entrar em tela cheia e esc para sair da tela cheia.
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        #criação de uma instância da classe clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=10, pady=10)
        #criação de uma instância da classe weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=10, pady=10)
        #criação de uma instância da classe news
        self.noticias = Noticias(self.bottomFrame)
        self.noticias.pack(side=LEFT, anchor=S, padx=10, pady=60)
        #criação de uma instância da classe rotas
        self.rotas = Rotas(self.bottomFrame)
        self.rotas.pack(side=RIGHT, anchor=S, padx=10, pady=60)
	
        self.gpio() #Chamar o método gpio
    #Esse método é responsável por entrar no modo tela cheia.
    def toggle_fullscreen(self, event=None):
        self.state = True 
        self.tk.attributes("-fullscreen", self.state)
        return "break"
    #Esse método é responsável por sair do modo tela cheia.
    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    #Este método é chamado toda vez que o botão de alterar perfil é pressionado.
    #Abaixo está configurado as rotas e notícias desejadas por cada perfil cadastrado. Aqui o usuário pode personalizar para atender as suas preferências:
    def my_callback_one(self, event=None):
        aux.change_prof = aux.change_prof + 1 #A variável change_prof é incrementada para que o próximo perfil seja selecionado.
        if aux.change_prof == 1:
            self.rotas.destination = "Joao Carbonari Junior 64"
            self.noticias.manchetes_url = "http://rss.home.uol.com.br/index.xml" #principais noticias
		
        if aux.change_prof == 2:
            self.rotas.destination = "Avenida Nove de Julho 500, Jundiai"
            self.noticias.manchetes_url = "http://rss.uol.com.br/feed/tecnologia.xml" #tecnologia
		
        if aux.change_prof == 3:
            self.rotas.destination = "Avenida Francisco Antonio Mafra 210"
            self.noticias.manchetes_url = "http://rss.uol.com.br/feed/economia.xml" #economia
   
        if aux.change_prof == 4:
            self.rotas.destination = "Avenida Trabalhador Sao Carlense 400"
            self.noticias.manchetes_url = "https://esporte.uol.com.br/ultimas/index.xml" #esporte
   
        if aux.change_prof == 5:
            self.rotas.destination = "Jacinto Favoretto 230"
            self.noticias.manchetes_url = "http://rss.uol.com.br/feed/jogos.xml" #jogos
   
        if aux.change_prof == 6:
            self.rotas.destination = "Avenida Sao Carlos 1200"
            self.noticias.manchetes_url = "http://rss.uol.com.br/feed/cinema.xml" #cinema
   
        if aux.change_prof == 7:
            self.rotas.destination = "Doutor Carlos de Camargo Salles 414"
            self.noticias.manchetes_url = "http://rss.uol.com.br/feed/vestibular.xml" #vestibular
  
        if aux.change_prof == 8:
            self.rotas.destination = "Episcopal 640"
            self.noticias.manchetes_url = "https://musica.uol.com.br/ultnot/index.xml" #musica
            aux.change_prof = 0
	#Aqui as rotas e as notícias são atualizadas.
        self.rotas.get_url()
        self.noticias.get_manchete()
        

       
    #Este método é chamado toda vez que o botão de alterar cor é pressionado.
    def my_callback_two(self, event=None):
        aux.pushbutton = aux.pushbutton + 1 #A variável pushbutton é incrementada para que a próxima cor seja selecionada.
        if aux.pushbutton == 0:
            aux.color = "white"
        if aux.pushbutton == 1:
            aux.color = "red"
        if aux.pushbutton == 2:
            aux.color = "green"
        if aux.pushbutton == 3:
            aux.color = "yellow"
            aux.pushbutton = -1
	
	#Neste bloco as cores das labels são alteradas de acordo com a variável color.
        self.clock.timelbl.configure(fg=aux.color)
        self.noticias.noticiaslbl.configure(fg=aux.color)
        self.weather.templbl.configure(fg=aux.color)
        self.weather.atuallbl.configure(fg=aux.color)
        self.weather.prevlbl.configure(fg=aux.color)
        self.weather.locallbl.configure(fg=aux.color)
        self.weather.tempamblbl.configure(fg=aux.color)
        self.weather.umidlbl.configure(fg=aux.color)
        self.clock.d_of_wlbl.configure(fg=aux.color)
        self.clock.datelbl.configure(fg=aux.color)
        self.rotas.rotaslbl.configure(fg=aux.color)
	
	#Aqui as rotas e as notícias são atualizadas.
        self.rotas.get_url()
        self.noticias.get_manchete()
        
    #Este método faz com que quando os pinos P8_12 e P8_14 da beagle sejam pressionados haja uma interrupção no processo e os métodos my_callback_one e my_callback_two sejam chamados.   
    def gpio(self, event=None):       
        GPIO.add_event_detect("P8_12", GPIO.RISING, callback = self.my_callback_one)
        GPIO.add_event_detect("P8_14", GPIO.RISING, callback = self.my_callback_two)

if __name__ == '__main__':
    w = FullscreenWindow() #criação de uma instância da classe FulscreenWindow.
    w.tk.mainloop() #Faz com que haja um loop da instância criada.
        
