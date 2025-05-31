from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management and flash messages

import serial
import time
import atexit

# Mock user data (replace with database in production)
users = {
    'admin': 'solofo1.',
    'narivo': '123',
    'solofo':'123',
    'ENI':'azerty',
    'Groupe1':'12345'
}

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

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


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

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

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



@app.route('/photoresistance')
def get_photoresistance():
    if arduino and arduino.is_open:
        try:
            # Vider le tampon série pour obtenir la dernière valeur
            arduino.reset_input_buffer()
            # Lire une ligne depuis le port série
            ldr_value = arduino.readline().decode('utf-8').strip()
           
            print(ldr_value)
            if ldr_value:
                return ldr_value  # Retourner la valeur de la photoresistance
            else:
                return 'Aucune donnée reçue', 500
        except serial.SerialException as e:
            print(f"Erreur de lecture depuis l'Arduino : {e}")
            return 'Erreur de communication avec l\'Arduino', 500
    else:
        return 'Arduino non connecté', 500


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)  # Disable debug mode
    except KeyboardInterrupt:
        print("Application stopped")
    finally:
        close_serial()  # Ensure the serial port is closed on exit
        