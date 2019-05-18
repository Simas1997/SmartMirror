from Tkinter import *

#import Adafruit_DHT
import requests
import json
import feedparser
#import traceback
import googlemaps

from datetime import datetime

from PIL import Image, ImageTk

#configuracao do sensor de temperatura utilizado (DHT22)
#sensor = Adafruit_DHT.DHT22  
#configuracao do pino de leitura do sensor de temperatura
#pin = 'P8_11'

class aux():
    pushbutton=0
    color ="white"


weather_api_token = '4ecc5df768c626180a20aa8bfdc0db96'
weather_lang = 'pt' 
weather_unit = 'si'
latitude = None 
longitude = None 
texto_gg = 94
texto_grande = 48
texto_medio = 28
texto_pequeno = 10


pic_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}


class Clock(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.widget = Frame(self)  #colocar Frame(master) cria um widget dominante na regiao impedindo a divisao de tela com o widget_clima
        self.widget["bg"] = ("black")
        self.widget.pack(side=TOP)
     
	# Inicializar label de tempo
        self.time1 = ''
        self.timelbl = Label(self.widget, text = self.time1)
        self.timelbl["font"] = ("Helvetica", texto_grande)
        self.timelbl["bg"] = ("black")
        self.timelbl["fg"] = ("white")
        self.timelbl.pack(side=TOP, anchor=E)

            # Inicializar label de dia da semana
        self.d_of_w1 = ''
        self.d_of_wlbl = Label(self.widget, text = self.d_of_w1)
        self.d_of_wlbl["font"] = ("Helvetica", texto_pequeno)
        self.d_of_wlbl["bg"] = ("black")
        self.d_of_wlbl["fg"] = ("white")	     
        self.d_of_wlbl.pack(side=TOP, anchor=E)

            # Inicializar label de data
        self.date1 = ''
        self.datelbl = Label(self.widget, text = self.date1)
        self.datelbl["font"] = ("Helvetica", texto_pequeno)
        self.datelbl["bg"] = ("black")
        self.datelbl["fg"] = ("white")
        self.datelbl.pack(side=TOP, anchor=E)
        self.att()

    def att(self):
	
	now = datetime.now()
	time2 = now.strftime("%H:%M")
	d_of_w2 = now.strftime("%A")
	if d_of_w2 == "Sunday":		d_of_w2 = "Domingo"
	if d_of_w2 == "Saturday":	d_of_w2 = "Sabado" 
	if d_of_w2 == "Monday":		d_of_w2 = "Segunda-feira"
	if d_of_w2 == "Tuesday":	d_of_w2 = "Terca-feira"
	if d_of_w2 == "Wednesday":	d_of_w2 = "Quarta-feira"
	if d_of_w2 == "Thursday":	d_of_w2 = "Quinta-feira"
	if d_of_w2 == "Friday":		d_of_w2 = "Sexta-feira"
	date2 = now.strftime("%d/%m/%Y")
	
        # Verificar para atualizar
	if time2 != self.time1:
        	self.time1 = time2
                self.timelbl.config(text=time2)
		
        if d_of_w2 != self.d_of_w1:
                self.d_of_w1 = d_of_w2
                self.d_of_wlbl.config(text=d_of_w2)
		
        if date2 != self.date1:
                self.date1 = date2
                self.datelbl.config(text=date2)
		            
	self.timelbl.after(200, self.att)




class Weather(Frame): #Frame: elemento principal
    def __init__(self, master = None):
        Frame.__init__(self, master, bg='black') #construtor da classe base
        self.temp = '' 
        self.local = '' 
        self.prev = '' 
        self.atual = ''
        self.pic = '' 
	

        self.widget_clima = Frame(self)  #colocar Frame(master) cria um widget dominante na regiao impedindo a divisao de tela com o widget (de horas)
        self.widget_clima["bg"] = ("black")
        self.widget_clima.pack(side=TOP, anchor=N)

        self.templbl = Label(self.widget_clima) 
        self.templbl["font"] = ("Helvetica", texto_grande)
        self.templbl["bg"] = ("black")
        self.templbl["fg"] = ("white")	
        self.templbl.pack(side=LEFT, anchor=N)

        self.piclbl = Label(self.widget_clima) 
        self.piclbl["bg"] = ("black")
        self.piclbl.pack(side=LEFT, anchor=N, padx=20)

        self.atuallbl = Label(self.widget_clima)
        self.atuallbl["font"] = ("Helvetica", texto_medio)
        self.atuallbl["bg"] = ("black")
        self.atuallbl["fg"] = ("white")
        self.atuallbl.pack(side=TOP, anchor=W)

        self.locallbl = Label(self.widget_clima)
        self.locallbl["font"] = ("Helvetica", texto_pequeno)
        self.locallbl["bg"] = ("black")
        self.locallbl["fg"] = ("white")
        self.locallbl.pack(side=TOP, anchor=W)


        self.prevlbl = Label(self.widget_clima)
        self.prevlbl["font"] = ("Helvetica", texto_pequeno)
        self.prevlbl["bg"] = ("black")
        self.prevlbl["fg"] = ("white")
        self.prevlbl.pack(side=TOP, anchor=W)

        
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url) #request usado para obter informacoes de um site
            ip_json = json.loads(req.text) # json eh uma biblioteca propria para trabalhar com dados do Json
            return ip_json['ip']
        except Exception as e:	#exception as e: da para acessar o conteudo do obejto exception = e
            #traceback.print_exc() #printa um cabecalho com as ultimas funcoes chamadas, printa a exception (e) e o valor, se (e) e um erro de sintaxe e o valor esta no formato adequado, ele printa a linha onde o erro aconteceu
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:

            if latitude is None and longitude is None:
                # localizacao pelo ip
                location_req_url = "http://api.ipstack.com/%s?access_key=33a23fcdf35dc1446075208d4461cfec" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['latitude']
                lon = location_obj['longitude']

                local2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit) #tirar lang e unit
            else:
		#localizacao ja definida pelo usuario
                local2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            grau= u'\N{DEGREE SIGN}' 
            temp2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), grau)
            atual2 = weather_obj['currently']['summary']
            prev2 = weather_obj["hourly"]["summary"]

            pic_id = weather_obj['currently']['icon']
            pic2 = None

            if pic_id in pic_lookup:
                pic2 = pic_lookup[pic_id]

            if pic2 is not None:
                if self.pic != pic2:
                    self.pic = pic2
                    image = Image.open(pic2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.piclbl.config(image=photo)
                    self.piclbl.image = photo
            else:
                # remover imagem
                self.piclbl.config(image='')

            if self.atual != atual2:
                self.atual = atual2
                self.atuallbl.config(text=atual2)
            if self.prev != prev2:
                self.prev = prev2
                self.prevlbl.config(text=prev2)
            if self.temp != temp2:
                self.temp = temp2
                self.templbl.config(text=temp2)
            if self.local != local2:
                if local2 == ", ":
                    self.local = "Cannot Pinpoint Location"
                    self.locallbl.config(text="Cannot Pinpoint Location")
                else:
                    self.local = local2
                    self.locallbl.config(text=local2)
        except Exception as e:
            #traceback.print_exc()
            print "Error: %s. Cannot get weather." % e

        self.after(6000, self.get_weather)



class Noticias(Frame):
   	
    def __init__(self, master = None):
        Frame.__init__(self, master, bg='black')
       
        self.titulo = "Noticias"
        self.noticiaslbl = Label(self, text=self.titulo)
        self.noticiaslbl["font"] = ("Helvetica", texto_medio)
        self.noticiaslbl["bg"] = "black"
        self.noticiaslbl["fg"] = "white"
        self.noticiaslbl.pack(side=TOP, anchor=W)
        self.manchetes = Frame(self, bg="black")
        self.manchetes.pack(side=TOP)
	
        self.get_manchete()


    def get_manchete(self):
        try:
            # remove all children
            for widget in self.manchetes.winfo_children():
                widget.destroy()  
          
            manchetes_url = "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419"
            feed = feedparser.parse(manchetes_url)

            for post in feed.entries[0:5]:
                headline = Manchetes_foto(self.manchetes, post.title)
                headline.pack(side=TOP, anchor=W)
                
        except Exception as e:
            #traceback.print_exc()
            print "Error: %s. Cannot get news." % e

        self.after(600000, self.get_manchete)


class Manchetes_foto(Frame):
    def __init__(self, master= None, event_name=""):
        Frame.__init__(self, master, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.piclbl = Label(self, bg='black', image=photo)
        self.piclbl.image = photo
        self.piclbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNamelbl = Label(self, text=self.eventName)
        self.eventNamelbl["font"] = ("Helvetica", texto_pequeno)
        self.eventNamelbl["bg"] = "black"
        self.eventNamelbl["fg"] = aux.color
        self.eventNamelbl.pack(side=LEFT, anchor=N)
	
class Sensor(Frame):
   	
    def __init__(self, master = None):
        Frame.__init__(self, master, bg='black')
       
        self.titulo = "Temperatura Ambiente"
        self.sensorlbl = Label(self, text=self.titulo)
        self.sensorlbl["font"] = ("Helvetica", texto_pequeno)
        self.sensorlbl["bg"] = "black"
        self.sensorlbl["fg"] = "white"
        self.sensorlbl.pack(side=TOP, anchor=W)
        self.leituras = Frame(self, bg="black")
        self.leituras.pack(side=TOP)

class Rotas(Frame): #crio uma classe de funcoes (frame eh a classe pai)
    def __init__(self,master = None): #inicializo meu objeto, que se chama self e seus atributos (defino a funcao __init__)
        Frame.__init__(self,master,bg='black') #chamando o construtor(metodo) da classe pai

        self.widgetRota = Frame(self) #colocar Frame(master) cria um widget dominante na regiao impedindo a divisao de tela com o widget (de horas) 
        self.widgetRota["bg"] = ("black") 
        self.widgetRota.pack(side=TOP, anchor=N) #widgetRota eh um atributo do objeto self que eh um objeto da classe Rotas
        
        self.titulo = "Rota Desejada"
        self.rotaslbl = Label(self.widgetRota, text = self.titulo)
        self.rotaslbl["font"] = ("Helvetica", texto_pequeno)
        self.rotaslbl["bg"] = "black"
        self.rotaslbl["fg"] = "white"
        self.rotaslbl.pack(side=TOP, anchor=W)


        #self.directions = Frame(self, bg = "black")
        #self.directions.pack(side=TOP)
        self.get_rota()

    def get_rota(self):
        try:
            gmaps = googlemaps.Client(key='AIzaSyBiNUWP5FbEKdByztRyhINuDCjfemldWlg')
            #origin="%s"&","&"%s" %(lat,lon)
            #destination=Joao+Carbonari+Junior+64
            #language=pt-BR
            #units=metric
            #region=br
            #deparature_time=now

            map_url = "https://maps.googleapis.com/maps/api/directions/json?origin=-23.203,-46.9008&destination=Joao+Carbonari+Junior+64&language=pt-BR&units=metric&region=br&departure_time=now&key=AIzaSyBiNUWP5FbEKdByztRyhINuDCjfemldWlg"
            map_req = requests.get(map_url)
            map_obj = json.loads(map_req.text)
            #print(map_obj)

            self.tempo_est = map_obj['routes'][0]['legs'][0]['duration']['text']
            #print(tempo_est)
            self.time_estlbl = Label(self.widgetRota, text = self.tempo_est)
            self.time_estlbl["font"] = ("Helvetica", texto_pequeno)
            self.time_estlbl["bg"] = "black"
            self.time_estlbl["fg"] = "white"
            self.time_estlbl.pack(side=LEFT, anchor=E)

            #self.templbl = Label(self.widget_clima) 

            self.dist = map_obj['routes'][0]['legs'][0]['distance']['text']
            self.distlbl = Label(self.widgetRota, text = self.dist)
            self.distlbl["font"] = ("Helvetica", texto_pequeno)
            self.distlbl["bg"] = "black"
            self.distlbl["fg"] = "white"
            self.distlbl.pack(side=LEFT, anchor=W)
            #print(dist)

            #self.step = map_obj['routes'][0]['legs'][0]['steps'][0]['html_instructions']
            for self.step_ in map_obj['routes'][0]['legs'][0]['steps']:
                self.step = self.step_['html_instructions']
                for i in range(0,len(self.step)):
                    self.step = self.step.replace("<b>","")
                    self.step = self.step.replace("</b>","")
                    self.step = self.step.replace('<div style="font-size:0.9em">',". ")
                    self.step = self.step.replace("</div>","")

                self.step_dist = self.step_['distance']['text']
       
                self.step_temp = self.step_['duration']['text']
                #self.step_all = '{} ({};{})'.format(self.step[1], self.step_dist[2], self.step_temp[3])

                self.steplbl = Label(self.widgetRota, text = self.step)
                self.steplbl["font"] = ("Helvetica", texto_pequeno)
                self.steplbl["bg"] = "black"
                self.steplbl["fg"] = "white"
                self.steplbl.pack(side=TOP, anchor=W)

                self.step_distlbl = Label(self.widgetRota, text = self.step_dist)
                self.step_distlbl["font"] = ("Helvetica", texto_pequeno)
                self.step_distlbl["bg"] = "black"
                self.step_distlbl["fg"] = "white"
                self.step_distlbl.pack(side=TOP, anchor=W)

                self.step_templbl = Label(self.widgetRota, text = self.step_temp)
                self.step_templbl["font"] = ("Helvetica", texto_pequeno)
                self.step_templbl["bg"] = "black"
                self.step_templbl["fg"] = "white"
                self.step_templbl.pack(side=TOP, anchor=W)


                #print("%s (%s; %s)" % (step,step_dist,step_temp))
                
        except Exception as e:
            #traceback.print_exc()
            print "Error: %s. Cannot get routes." % e

        #self.after(600000, self.get_rota)



	
class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.centerFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.centerFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.bind("<space>", self.changeColor)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # news
        self.noticias = Noticias(self.bottomFrame)
        self.noticias.pack(side=LEFT, anchor=S, padx=100, pady=60)
        #sensor
        self.sensor = Sensor(self.centerFrame)
        self.sensor.pack(side=LEFT, anchor=N, padx=50, pady=30)
        #rotas
        self.rotas = Rotas(self.centerFrame)
        self.rotas.pack(side=RIGHT, anchor=N, padx=60, pady=100)
        
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def changeColor(self, event=None):         
        aux.pushbutton = aux.pushbutton+1
        if aux.pushbutton == 0:
            aux.color = "white"
        if aux.pushbutton == 1:
            aux.color = "red"
        if aux.pushbutton == 2:
            aux.color = "blue"
        if aux.pushbutton == 3:
            aux.color = "yellow"
            aux.pushbutton = -1
        self.clock.timelbl.configure(fg=aux.color)
        self.noticias.noticiaslbl.configure(fg=aux.color)
        self.weather.templbl.configure(fg=aux.color)
        self.weather.atuallbl.configure(fg=aux.color)
        self.weather.prevlbl.configure(fg=aux.color)
        self.weather.locallbl.configure(fg=aux.color)
        self.clock.d_of_wlbl.configure(fg=aux.color)
        self.clock.datelbl.configure(fg=aux.color)
        self.noticias.get_manchete()
	#self.Sensor.sensorlbl.configure(fg=aux.color)	
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()

