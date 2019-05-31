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
  
  * AO TNCAPA97AB9 wifi_506583d4fc5e_544e434150413937414239_managed_psk
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
