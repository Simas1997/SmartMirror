# SmartMirror
# Sistemas Embarcados - USP São Carlos
Apresentado por:
  
  Cainan Colaço Brunhera
  
  Fernando Santurbano Tavares Simas
  
  Gabriel Maurício Marques
  
  Leonardo Luís da Silva
  
# Instalando bibliotecas
Para rodar o código do "Smart Mirror" precisa-se instalar algumas bibliotecas, mas antes vamos conectar nossa BeagleBoneBlack a um monitor. Para isso você precisará de um cabo microHDMI, mouse e teclado. Após conectar os cabos, alimente a Beagle com uma fonte 5V e aguarde até aparecer uma tela inicial como a seguinte:
![Tela_inicial_beagle](https://user-images.githubusercontent.com/48104891/58729763-a6fbf380-83c0-11e9-8746-653465f2bfa7.jpg)
Agora já estamos quase prontos para instalar as bibliotecas, porém para isso precisamos de internet, então se estiver usando a BeagleBoneBlackWireless digite os seguintes comandos no seu terminal:
  
  sudo connmanctl
  
  connmanctl> enable wifi
  
  Enabled wifi
  
  connmanctl> scan wifi
  
  Scan completed for wifi
  
  connmanctl> services
  
  AO TNCAPA97AB9 wifi_506583d4fc5e_544e434150413937414239_managed_psk
  wifi_506583d4fc5e_hidden_managed_psk
  
  DIRECT-roku-876 wifi_506583d4fc5e_4449524543542d726f6b752d383736_managed_psk
  
  BTHub6-H5H7 wifi_506583d4fc5e_4254487562362d48354837_managed_psk
  
  virginmedia2029431 wifi_506583d4fc5e_76697267696e6d6564696132303239343331_managed_psk
  
  VM046693-2G wifi_506583d4fc5e_564d3034363639332d3247_managed_psk
  
  BTWifi-with-FON wifi_506583d4fc5e_4254576966692d776974682d464f4e_managed_none
  
  connmanctl> agent on
  
  Agent registered
  
  connmanctl> connect wifi_506583d4fc5e_544e434150413937414239_managed_psk
  
  Passphrase? xxxxxxxxxxx
  
  connected wifi_506583d4fc5e_544e434150413937414239_managed_psk
  
  connmanctl> quit

Note que quando você digitar o comando services aparecerão todas as redes wifi disponíveis, então basta você escolher uma para se conectar. Se você não usar a BeagleBoneWireless, pode conectar-se usando um cabo de rede.

Antes de iniciar a instalação das bibliotecas, você deve clonar esse repositório em sua máquina, para isso acesse o local de sua preferência e execute o comando:

	git clone https://github.com/Simas1997/SmartMirror.git

Com a placa conectada a internet, agora iniciaremos o processo de instalação das bibliotecas. Para isso, precisamos inicialmente instalar o pip, então digite os seguintes comandos no seu terminal:

	sudo apt-get update

	sudo apt-get install python-pip
	
Agora, realizaremos a instalação das bibliotecas utilizadas no projeto.Para isso, execute os seguintes comandos no seu terminal:

	sudo apt-get install python-tk
	
	sudo pip install -r requirements.txt
	
	sudo pip install -U googlemaps
	
	sudo pip install pil
	
	sudo pip install Adafruit_DHT
	
	sudo pip install Adafruit_BBIO
	
Terminada a instalação das bibliotecas, vamos agora montar o circuito necessário para rodar o programa.

# Montagem do circuito

Para montar o circuito deste projeto, você precisará de:

* Uma protoboard;

* Dois resistores de 1K;

* Dois botões (*push button*);

* Um sensor DHT22 de temperatura e umidade.

Com todos estes materiais, monte o circuito como o da imagem a seguir:

![Circuito](https://github.com/Simas1997/SmartMirror/blob/master/Imagens/Circuito.JPG)

Fique atento às portas utilizadas na BBB, além do GND e do VCC 3.3V, utilizamos a porta P8_11 para o sensor e as portas P8_12 e P8_14 para os botões.

Note que um botão será destinado a mudança de cor dos caracteres enquanto o outro será para a mudança de perfis.

Confira todas as ligações feitas no circuito e se estiver tudo certo, sigamos para o próximo passo: rodar o programa.

# Rodando o programa

Para executar o programa, vá até a pasta onde você clonou o repositório (use o comando *cd*). Então execute os seguintes comandos:

	cd SmartMirror
	
	cd SmartMirrorFolder
	
Agora já estamos na pasta onde está salvo o programa, então para rodar o programa basta executar o seguinte comando:

	sudo python SmartMirrorFinal.py
	
Aguarde alguns segundos e então você verá a seguinte tela:

![WhatsApp Image 2019-06-05 at 13 42 44](https://user-images.githubusercontent.com/48104891/58976759-9a034980-879e-11e9-9ee2-644561c7756b.jpeg)

Porém ela ainda não estará em tela cheia, para isso pressione *Enter* no teclado.

Para encerrar, gostaria de convidá-los a assistir nosso vídeo, onde explicamos com mais detalhes o projeto: *linkdovídeo*
