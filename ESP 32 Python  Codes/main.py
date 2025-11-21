import network
import machine
from machine import I2C, Pin
import time
import ujson
from umqtt.simple import MQTTClient
import esp32
import ntptime
import dht  # Import DHT module
from i2c_lcd import I2cLcd # Import I2c Lcd Display 


# Define I2C parameters
I2C_SDA = 21  # GPIO21 for SDA 
I2C_SCL = 22  # GPIO22 for SCL
I2C_ADDR = 0x27 
NUM_LINES = 2  
NUM_COLUMNS = 16

#mqtt broker
aws_broker="a1bbbp30ytbtx3-ats.iot.eu-north-1.amazonaws.com"
clientid='iotconsole-80277460-568f-4bc0-9595-c1130ba2c097'#name of client
pkey='hum1.private.pem.key'#private.pem.key
ccert='hum1.pem.crt'#pem.crt
#rroot_ca=''#root ca
pub_topic='hum/hum1'#topic
key=None
cert=None

with open(pkey, 'r') as f:
    key = f.read()
with open(ccert, 'r') as f:
    cert = f.read()
#with open(rroot_ca, 'r') as f:
#    root = f.read()
    
sslp = {"key":key, "cert":cert, "server_side":False}#ssl parameters

# Initialize DHT11 sensor
dht_pin = machine.Pin(4)  # Use GPIO4
sensor = dht.DHT11(dht_pin)

# Initialize I2C
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)


# Create an instance of the I2cLcd class
lcd = I2cLcd(i2c, I2C_ADDR, NUM_LINES, NUM_COLUMNS)

lcd.clear()
lcd.move_to(4, 0) 
lcd.putstr("Thermal")
lcd.move_to(2, 1) 
lcd.putstr("Distribution")



# Connect to Wi-Fi
wlan=network.WLAN(network.STA_IF)

print('ESP_32 WiFi program')
wlan.active(True)
wlan.connect(ssid,psk)
print("connecting to wifi")
while not wlan.isconnected():
    print(".",end=" ")
    time.sleep(0.5)
    #machine.idle()
print("connceted to wlan {} with ip:{}".format(ssid,wlan.ifconfig()[0]))

lcd.clear()
lcd.move_to(0, 0) 
lcd.putstr("Wifi Connected")

ntptime.settime()
time.sleep(1)

# Connect to MQTT broker    
print("Begin connection with MQTT Broker :: {}".format(aws_broker))
mqtt = MQTTClient(client_id=clientid, server=aws_broker,port=8883,keepalive=1200,ssl=True,ssl_params=sslp)
mqtt.connect()
print("Connected to MQTT  Broker :: {}".format(aws_broker))

# Main loop
while True:
    try:
        # Measure temperature and humidity using DHT11 sensor
        sensor.measure()
        temp = sensor.temperature()  # Get temperature in Celsius
        hum = sensor.humidity()  # Get humidity in percentage

        # Get current time
        current_time = "{}:{}:{}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])

        # Prepare JSON message
        mssg = ujson.dumps({"time": current_time, "temp": temp, "hum": hum})

        # Publish message to MQTT broker
        mqtt.publish(pub_topic, mssg)
        print("Published at {}: Temp = {}°C, Humidity = {}%".format(current_time, temp, hum))

        # Display temperature and humidity on the LCD
        lcd.clear()
        lcd.move_to(0, 0) 
        lcd.putstr("Temp: {}C".format(temp))
        lcd.move_to(0, 1)  # Move to second line
        lcd.putstr("Hum: {}%".format(hum))
        
        time.sleep(2)  # Wait for 2 seconds
        
    except OSError as e:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Waiting....")
        time.sleep(2)  # Wait for 2 seconds before retrying

# Disconnect
wlan.disconnect()
#machine.reset()
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Completed ;-)")
lcd.move_to(5, 1)
lcd.putstr("Thank You")






