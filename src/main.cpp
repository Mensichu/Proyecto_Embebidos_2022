#include <SPI.h>
#include <Wire.h>

#include <avr/io.h>
#include <util/delay.h>

#include <stdio.h>
#include <uart.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>

#include <RTClib.h>

//Pantalla Oled Librerias
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define Ancho 128
#define Alto 64

#define Oled_reset 4
//Obejto Oled y sus caracteristicas
Adafruit_SSD1306 oled(Ancho, Alto, &Wire,Oled_reset);

#define DHTPIN 2
#define DHTTYPE DHT11

void init_ADC(){
   ADMUX = 0B01000011;	//AVCC- AREF (01), Justif derecha(0), -(0), y ADC3(0011)
   ADCSRA = 0B00000111;	//111 = prescaler-128
   //Apagado y sin arrancar (00), Modo auto(0), por inter(0), int terminada(0), PRE-SCALER  128
   ADCSRB = 0B00000000; 	//FREE RUNNING MODE
   DIDR0 = 0B00001000;	//ENABLE ANALOG MODE ADC3

}

DHT dht(DHTPIN, DHTTYPE);

RTC_DS3231 rtc;


void setup(){ 

   //Reloj
   rtc.begin();
   
   //Hum y Temp
   dht.begin();
   
   
   //ADC LDR
   init_ADC();
   serial_begin();
   
   //Oled
   Wire.begin();
   oled.begin(SSD1306_SWITCHCAPVCC,0x3C);

   //Pantalla de inicio
   oled.clearDisplay();
   oled.setTextColor(WHITE);
   oled.setCursor(0,0);
   oled.setTextSize(2);
   oled.print("ESTACION");
   oled.setCursor(0,20);
   oled.print("METEORO");
   oled.setCursor(0,40);
   oled.print("LOGICA");
   oled.display();
   _delay_ms(2000);

 }

String dato="";

void loop(){
      //LDR
      ADCSRA = 0B11000111; // ENABLED ANALOG CONVERTER & START CONVERSION
	   while(ADCSRA & (1<< ADSC)); // ADSC DISABLED? 
      //while (!is_data_ready()){_delay_ms(20);}
      //mensaje = get_RX_buffer();

      char LDR[20];
      int valor = ADC/10;
      valor= valor<0 ? (0) : (valor>100 ? 100 : valor);
      sprintf(LDR, "%d", valor);

      //RELOJ
      int dayint  = rtc.now().day();
      int monthint= rtc.now().month();
      int yearint  = rtc.now().year();
      int horaint  = rtc.now().hour();
      int minutoint  = rtc.now().minute();
      int segundoint  = rtc.now().second();

      char dia[20];
      char month[20];
      char year[20];
      char hora[20];
      char minuto[20];
      char segundo[20];
      
      sprintf(dia, "%d", dayint);
      sprintf(month, "%d", monthint);
      sprintf(year, "%d", yearint);
      sprintf(hora, "%d", horaint);
      sprintf(minuto, "%d", minutoint);
      sprintf(segundo, "%d", segundoint);


      //DHT11
      int temp = dht.readTemperature();
      char TEMP[20];
      sprintf(TEMP, "%d", temp);
      
      int hum = dht.readHumidity();
      char HUM[20];
      sprintf(HUM, "%d", hum);
      
      //Datos
      char concat[80]="";
      strcat(concat,year);
      strcat(concat,"/");
      strcat(concat,month);
      strcat(concat,"/");
      strcat(concat,dia);
      strcat(concat,"-");
      strcat(concat,hora);
      strcat(concat,":");
      strcat(concat,minuto);
      strcat(concat,":");
      strcat(concat,segundo);
      strcat(concat,",");
      
      strcat(concat,TEMP);
      strcat(concat,",");
      strcat(concat,HUM);
      strcat(concat,",");
      strcat(concat,LDR);
      //serial_println_str("Aqui estoy");
      /*
      if (is_data_ready()) {
         serial_println_str("Es verdadero");
      }else{
         serial_println_str("Es falso");
      }
      */

     //Se envia los datos unicamente cuando el Raspberry los solicite
      if (solicita_Enviar_Datos()){
         serial_println_str(concat);
      }
      
      //OLED
      char TempOled[20]="Temp: ";
      strcat(TempOled,TEMP);
      strcat(TempOled,"C");
      char HumOled[20]="Hum:  ";
      strcat(HumOled,HUM);
      strcat(HumOled,"%");
      char LuzOled[20]="Luz:  ";
      strcat(LuzOled,LDR);
      strcat(LuzOled,"%");

      
      oled.clearDisplay();
      oled.setTextColor(WHITE);
      oled.setCursor(0,0);
      oled.setTextSize(1.8);
      oled.print("EST. METEOROLOGICA");
      oled.setTextSize(1.99);
      oled.setCursor(0,16);
      oled.print(TempOled);
      oled.setCursor(0,32);
      oled.print(HumOled);
      oled.setCursor(0,48);
      oled.print(LuzOled);
      oled.display();
   


      _delay_ms(100);
      
}

