import RPi.GPIO as GPIO
import subprocess
import time

# Set up GPIO pin for button
BUTTON_PIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define debounce interval in seconds
DEBOUNCE_INTERVAL = 45  # Adjust as needed

# Variable to track last button press time
last_button_press_time = 0

# Function to capture photo and call Node.js script for uploading
def capture_and_upload():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    image_path = f"captured_image_{timestamp}.jpg"

    # Capture photo using Raspberry Pi camera module
    subprocess.run(["raspistill", "-o", image_path, "-rot", "90"])

    # Call Node.js script to upload image
    subprocess.run(["node", "upload_to_instagram.js", image_path])

# Callback function for button press
def button_callback(channel):
    global last_button_press_time

    # Get current time
    current_time = time.time()

    # Check if debounce interval has passed since last button press
    if current_time - last_button_press_time > DEBOUNCE_INTERVAL:
        print("Button pressed")
        capture_and_upload()
        last_button_press_time = current_time  # Update last button press time

# Set up event detection for button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

print("Waiting for button press to capture photo...")

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
