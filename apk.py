from flask import Flask, render_template, request, redirect, url_for, flash, session
import serial
import time
import atexit

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management and flash messages

# Mock user data (replace with database in production)
users = {
    'admin': '123'
}

# Initialize serial connection with error handling
arduino = None
def init_serial():
    global arduino
    try:
        arduino = serial.Serial('COM2', 9600, timeout=1)
        time.sleep(2)  # Wait for the connection to establish
        print("Connected to Arduino on COM2")
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        arduino = None

# Function to close the serial port
def close_serial():
    if arduino and arduino.is_open:
        arduino.close()
        print("Serial port closed")

# Register the close_serial function to run when the program exits
atexit.register(close_serial)

# Initialize serial connection at startup
init_serial()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('login'))
    return render_template('index2.html', username=session['username'])

@app.route('/on')
def onled():
    if 'username' not in session:
        return 'Unauthorized', 401
    if arduino and arduino.is_open:
        try:
            arduino.write(b'1')
            print("********LED ON********")
            return 'on'
        except serial.SerialException as e:
            print(f"Error writing to Arduino: {e}")
            return 'Error communicating with Arduino', 500
    else:
        return 'Arduino not connected', 500

@app.route('/off')
def offled():
    if 'username' not in session:
        return 'Unauthorized', 401
    if arduino and arduino.is_open:
        try:
            arduino.write(b'0')
            print("********LED OFF********")
            return 'off'
        except serial.SerialException as e:
            print(f"Error writing to Arduino: {e}")
            return 'Error communicating with Arduino', 500
    else:
        return 'Arduino not connected', 500

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    close_serial()  # Close serial port on logout
    return redirect(url_for('login'))

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)  # Enable debug mode for development
    except KeyboardInterrupt:
        print("Application stopped")
    finally:
        close_serial()  # Ensure the serial port is closed on exit