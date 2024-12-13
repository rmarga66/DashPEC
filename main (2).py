from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Initialize DataFrame for patient data
data = pd.DataFrame(columns=[
    'Nom', 'Prenom', 'Date_naissance', 'Indication', 'Debut_traitement', 'Fin_traitement', 'Actif'
])

# User credentials (example)
users = {
    "admin": "password123",  # Replace with your credentials
    "user": "userpass"
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['user'] = username
        return redirect(url_for('form'))
    else:
        return "Invalid credentials, please try again.", 401

@app.route('/form')
def form():
    if 'user' not in session:
        return redirect(url_for('login'))

    indications = [
        'ALR Post Opératoire', 'Antibio intraveineuse', 'Hydratation Diffuseur',
        'Hydratation Pompe', 'Perfusion Diffuseur', 'Perfusion Gravité',
        'Perfusion Pompe', 'Post op/RAAC', 'Solumédrol',
        "Entretien gastrostomie en vu d'une NED", 'Entretien PICC LINE/VVC',
        'Immuno IV', 'Immuno SC', 'Ned Pompe', 'NPAD', 'PCA',
        'Chimiothérapie', 'Radiothérapie', 'Suivi post-opératoire', 'Traitement palliatif'
    ]
    return render_template('form.html', indications=indications)

@app.route('/add', methods=['POST'])
def add_patient():
    if 'user' not in session:
        return redirect(url_for('login'))

    global data

    # Retrieve form data
    nom = request.form['nom']
    prenom = request.form['prenom']
    date_naissance = request.form['date_naissance']
    indication = request.form['indication']
    debut_traitement = request.form['debut_traitement']
    fin_traitement = request.form['fin_traitement']
    actif = request.form['actif']

    # Add data to DataFrame
    new_data = {
        'Nom': nom,
        'Prenom': prenom,
        'Date_naissance': date_naissance,
        'Indication': indication,
        'Debut_traitement': debut_traitement,
        'Fin_traitement': fin_traitement,
        'Actif': actif
    }
    data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    global data

    # Calculate statistics
    active_count = len(data[data['Actif'] == 'Actif'])
    inactive_count = len(data[data['Actif'] == 'Inactif'])
    indication_counts = data['Indication'].value_counts()
    indication_percentages = (indication_counts / len(data)) * 100

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(indication_percentages, labels=indication_percentages.index, autopct='%1.1f%%')
    ax.set_title('Répartition des indications')

    # Save chart to memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render_template(
        'dashboard.html',
        active_count=active_count,
        inactive_count=inactive_count,
        chart_data=chart_data,
        indications=indication_counts.to_dict()
    )

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
