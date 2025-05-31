from flask import Flask, render_template
import serial
import time
import atexit

# Initialize Flask app
app = Flask(__name__)

# Initialize serial connection with error handling
arduino = None
try:
    arduino = serial.Serial('COM2', 9600, timeout=1)
    time.sleep(2)  # Wait for the connection to establish
    print("Connected to Arduino on COM2")
except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")

# Function to close the serial port
def close_serial():
    if arduino and arduino.is_open:
        arduino.close()
        print("Serial port closed")

# Register the close_serial function to run when the program exits
atexit.register(close_serial)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/on')
def onled():
    if arduino and arduino.is_open:
        try:
            arduino.write(b'1')
            print("********on********")
            return 'on'
        except serial.SerialException as e:
            print(f"Error writing to Arduino: {e}")
            return 'Error communicating with Arduino', 500
    else:
        return 'Arduino not connected', 500

@app.route('/off')
def offled():
    if arduino and arduino.is_open:
        try:
            arduino.write(b'0')
            print("********off********")
            return 'off'
        except serial.SerialException as e:
            print(f"Error writing to Arduino: {e}")
            return 'Error communicating with Arduino', 500
    else:
        return 'Arduino not connected', 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)  # Disable debug mode
    except KeyboardInterrupt:
        print("Application stopped")
    finally:
        close_serial()  # Ensure the serial port is closed on exit
        