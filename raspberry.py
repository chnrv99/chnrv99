import time
import requests
import Adafruit_DHT
import RPi.GPIO as GPIO

# Configuration for sensors
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4             # GPIO pin for DHT11
TRIG_PIN = 23           # GPIO pin for Ultrasonic Trigger
ECHO_PIN = 24           # GPIO pin for Ultrasonic Echo
GAS_SENSOR_PIN = 17     # GPIO pin for MQ Gas Sensor (analog or digital depending on sensor setup)

# Publicly hosted URL endpoint
URL = "http://<PUBLIC_URL>/api/sensor-data"  # Replace <PUBLIC_URL> with your public server URL

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(GAS_SENSOR_PIN, GPIO.IN)

def read_dht11():
    """Reads temperature and humidity from DHT11."""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

def read_ultrasonic():
    """Reads distance from ultrasonic sensor."""
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in air (34300 cm/s) / 2
    distance = round(distance, 2)
    return distance

def read_gas_sensor():
    """Reads gas level from MQ gas sensor."""
    gas_level = GPIO.input(GAS_SENSOR_PIN)
    # Some gas sensors give digital output; if analog, an ADC is needed to convert
    return gas_level

def send_sensor_data(distance, gas_value, temperature, humidity):
    """Sends sensor data to the REST API endpoint."""
    data = {
        "distance": distance,
        "gasValue": gas_value,
        "temperature": temperature,
        "humidity": humidity
    }
    try:
        response = requests.post(URL, json=data)
        if response.status_code == 200:
            print("Data sent successfully:", response.json())
        else:
            print("Failed to send data:", response.status_code)
    except Exception as e:
        print("Error sending data:", e)

try:
    while True:
        # Read sensors
        humidity, temperature = read_dht11()
        distance = read_ultrasonic()
        gas_value = read_gas_sensor()

        # Check if sensor readings are valid
        if humidity is not None and temperature is not None:
            # Send data to server
            send_sensor_data(distance, gas_value, temperature, humidity)
        else:
            print("Failed to retrieve data from DHT11 sensor")

        # Wait before the next reading
        time.sleep(10)

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.cleanup()
