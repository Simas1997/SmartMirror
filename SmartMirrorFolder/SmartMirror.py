from Tkinter import *

import requests
import json
import feedparser
#import traceback

from datetime import datetime

from PIL import Image, ImageTk


weather_api_token = '4ecc5df768c626180a20aa8bfdc0db96'
weather_lang = 'pt' 
weather_unit = 'si'
latitude = None 
longitude = None 
texto_gg = 94
texto_grande = 48
texto_medio = 28
texto_pequeno = 18


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
	self.eventNamelbl["fg"] = "white"
        self.eventNamelbl.pack(side=LEFT, anchor=N)





class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # news
        self.noticias = Noticias(self.bottomFrame)
        self.noticias.pack(side=LEFT, anchor=S, padx=100, pady=60)
        

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()



