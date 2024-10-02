import requests
import RPi.GPIO as GPIO
import time

# Servo motor setup
GPIO.setmode(GPIO.BCM)
servo_pin = 18  # Servo pin
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency
pwm.start(0)

def set_servo_angle(angle):
    duty = angle / 18 + 2 
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def send_image_to_server(image_path):
    url = 'http://yourserveraddress.com/classify'  # Replace with your server's URL
    files = {'file': open(image_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            return response.json()  # Assuming the server returns JSON
        else:
            print(f"Error: Server responded with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error sending image to server: {e}")
        return None

# Image path on Raspberry Pi
image_path = '/path/to/your/image.jpg'  # Replace with the actual image path

# Send image to server and get response
response_data = send_image_to_server(image_path)

if response_data:
    # Assuming the server returns a choice 1 or 2
    if response_data['choice'] == 1:
        set_servo_angle(90)  # Move servo to 90 degrees
    elif response_data['choice'] == 2:
        set_servo_angle(0)   # Move servo to 0 degrees

# Cleanup
pwm.stop()
GPIO.cleanup()
