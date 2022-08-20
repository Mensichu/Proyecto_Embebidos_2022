import serial
import time
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
#Thingspeak
import requests
t_TS=0

#Variables Globales
Tiempo_actual="11/1/2011-11:11:11"
Temp_actual=28
Hum_actual=75
Luz_actual=70


minTemp = 28
maxTemp = 29
minHum= 40
maxHum= 65
minLuz=40
maxLuz=80

x=0
y=2
z=2

step=2

#Tamaño de nuestra LCD 16x2
lcd_columns = 16
lcd_rows= 2

#Coneccion al bus I2C
i2c= board.I2C()


#Comunicacion serial
com = True
ser=""
def compruebaConexion():
	global com,ser
	try:
		ser=serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=5)
		print("Encontro")
		com=True
	except:
		ser=""
		com=False
		print("NO encontro")
#ser = serial.Serial('/dev/ttyUSB0',9600,5)
registroBackup="2022/7/10-10:30:12,11,11,11"

#Inicializamos la clase LCD

lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()
msg = "PROYECTO DE"
lcd.message = msg
lcd.cursor_position(0,1)
msg2 = "SISTEMAS EMBEBIDOS"
lcd.message = msg2
#Hacemos un scroll de animacion
for i in range(5):
	time.sleep(0.3)
	lcd.move_left()

lcd.color = [0,0,0]
lcd.clear()
#Menu z
#2
def titulo():
	global Tiempo_actual
	lcd.cursor_position(0,0)
	lcd.message="Est.Meteorologica"
	lcd.cursor_position(0,1)
	lcd.message= str(Tiempo_actual.replace("b'","")[2:17])+" "

#1
def menu(temp, hum, luz):
	lcd.cursor_position(0,0)
	lcd.message = "Temp="+str(temp)+"C Hum="+str(hum)+"%"
	lcd.cursor_position(0,1)
	tluz= str(luz) if luz>=10 else "0"+str(luz)
	lcd.message = "Luz="+str(tluz)+"%"
#0
def seleccion():
	lcd.cursor_position(0,0)
	lcd.message = "Modificar rangos"

#No-señal
def noSignal():
	lcd.cursor_position(0,0)
	lcd.message= "No hay"
	lcd.cursor_position(0,1)
	lcd.message = "comunicacion"


#Menu y
def modificar():
	global minTemp,minHum,minLuz
	global maxTemp,maxHum,maxLuz
	global y
	lcd.cursor_position(0,0)
	if y==2:
		lcd.message = "Temp: "+str(minTemp)+"-"+str(maxTemp)+"C"
	elif y==1:
		lcd.message = "Hum:  "+str(minHum)+"-"+str(maxHum)+"%"
	elif y==0:
		lcd.message = "Luz:  "+str(minLuz)+"-"+str(maxLuz)+"%"
	lcd.cursor_position(5,1)
	lcd.message = "Min-Max"

#Operacion suma y resta
def operacion(operador):
	global minTemp,minHum,minLuz
	global maxTemp, maxHum,maxLuz
	global y, x

	if x==1:
		lcd.cursor_position(6,0)
		if y==2:
			minTemp= minTemp + operador
			minTemp= 10 if minTemp<=10 else 98 if minTemp>98 else minTemp
			lcd.message=str(minTemp)
			if maxTemp<=minTemp:
				maxTemp=minTemp+1
				lcd.cursor_position(9,0)
				lcd.message=str(maxTemp)
		elif y==1:
			minHum= minHum + operador
			minHum =10 if minHum <=10 else 98 if minHum >98 else minHum
			lcd.message=str(minHum)
			if maxHum<=minHum:
				maxHum=minHum+1
				lcd.cursor_position(9,0)
				lcd.message=str(maxHum)
		elif y==0:
			minLuz= minLuz + operador
			minLuz = 10 if minLuz <=10 else 98 if minLuz > 98 else minLuz
			lcd.message=str(minLuz)
			if maxLuz<=minLuz:
				maxLuz=minLuz+1
				lcd.cursor_position(9,0)
				lcd.message=str(maxLuz)
	elif x==0:
		lcd.cursor_position(9,0)
		if y==2:
			maxTemp= maxTemp + operador
			maxTemp=11 if maxTemp<=11 else 99 if maxTemp>99 else maxTemp
			lcd.message=str(maxTemp)
			if minTemp>= maxTemp:
				minTemp=maxTemp-1
				lcd.cursor_position(6,0)
				lcd.message=str(minTemp)
		elif y==1:
			maxHum= maxHum + operador
			maxHum=11 if maxHum<=11 else 99 if maxHum>99 else maxHum
			lcd.message=str(maxHum)
			if minHum>= maxHum:
				minHum=maxHum-1
				lcd.cursor_position(6,0)
				lcd.message=str(minHum)
		elif y==0:
			maxLuz= maxLuz + operador
			maxLuz=11 if maxLuz<=11 else 99 if maxLuz>99 else maxLuz
			lcd.message=str(maxLuz)
			if minLuz>= maxLuz:
				minLuz=maxLuz-1
				lcd.cursor_position(6,0)
				lcd.message=str(minLuz)


#Actualizar menus y submenus
def actualizarZ():
	global Temp_actual,Hum_actual,Luz_actual
	global z, step
	if lcd.down_button:
		z= z-1 if z>0 else 2
		lcd.clear()
	elif lcd.up_button:
		z= z+1 if z<2 else 0
		lcd.clear()
	elif lcd.left_button:
		z=2
		lcd.clear()

	if z==2:
		titulo()
	elif z==1:
		menu(Temp_actual,Hum_actual,Luz_actual)
	elif z==0:
		seleccion()
		if lcd.right_button:
			step=1
			lcd.clear()

def actualizarY():
	global y
	global step
	modificar()
	if lcd.down_button:
		y= y-1 if y>0 else 2
		lcd.clear()
	elif lcd.up_button:
		y=y+1 if y<2 else 0
		lcd.clear()
	elif lcd.left_button:
		step=2
		lcd.clear()
	elif lcd.right_button:
		step=0
		lcd.cursor_position(7,0)
		lcd.cursor= True
		lcd.blink=  True

def actualizarX():
	global x
	global step
	lcd.cursor_position(10-3*x,0)
	if lcd.right_button:
		x=1 if x==0 else 0
	if lcd.left_button:
		step=1
		lcd.cursor= False
		lcd.blink = False
		lcd.clear()
	if lcd.down_button:
		operacion(-1)
	if lcd.up_button:
		operacion(+1)


def step_menus():
	global step
	if step==2:
		actualizarZ()
	elif step==1:
		actualizarY()
	elif step==0:
		actualizarX()

def alarma():
	global minTemp,minHum,minLuz
	global maxTemp,maxHum,maxLuz
	global Temp_actual,Hum_actual,Luz_actual

	if Temp_actual < minTemp  or Temp_actual > maxTemp:
		r=255
	else:
		r=0
	if Hum_actual < minHum or Hum_actual > maxHum:
		g=255
	else:
		g=0
	if Luz_actual < minLuz or Luz_actual > maxLuz:
		b=255
	else:
		b=0

	lcd.color = [r,b,g]

registro=registroBackup

def serialCom():
	global Temp_actual,Hum_actual,Luz_actual,Tiempo_actual
	global ser
	ser.write(b'B\n')
	cadena = ser.readline()
	if cadena.decode() != '':
		registro = str(cadena)
	else:
		registro= registroBackup
		print("dato perdido\n")
	datos=registro.split(",")
	if True:
		Tiempo_actual=datos[0].replace("'b","")
		Temp_actual= int(datos[1])
		Hum_actual = int(datos[2])
		Luz_actual = int(datos[3][0:2]) if len(datos[3])==7 else int(datos[3][0:1])
		Luz_actual = 0 if Luz_actual < 0 else 100 if Luz_actual>100 else Luz_actual
	else:
		print("Fallo en split!")
	print(registro)

blink = True


def thingSpeak():
	global t_TS
	t_TS=t_TS+1 if t_TS<3600 else 0
	Send = True if t_TS==3600 else False
	if Send :
		enviar = requests.get("https://api.thingspeak.com/update?api_key=TNWYC5DOCHOKE63R&field1="
		+str(Temp_actual)+"&field2="+str(Hum_actual)+"&field3="
		+str(Luz_actual))




while True:
	compruebaConexion()
	if com:
		serialCom()
		step_menus()
		thingSpeak()
		alarma()
	else:
		lcd.clear()
		noSignal()
		blink=1 if blink==0 else 0
		lcd.color = [255*blink,0,0]
		time.sleep(0.9)
		print("No hay comunicacion!")
	#lcd.cursor_position(15,1)
	#lcd.message=str(step)
	time.sleep(0.1)


time.sleep(10)
