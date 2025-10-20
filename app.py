from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'clave-secreta-débil-12345'

# Credenciales predecibles - Vulnerabilidad intencional
USUARIOS = {
    "admin": "1234",
    "manager": "@sTrid952!",
    "coordinator": "Hol@_soy_un@_ClaVe"
}

# Datos del evento (lo que ves después de login)
EVENTO_INFO = {
    "nombre": "Competencia CITT 2024",
    "fecha": "2024-11-15",
    "lugar": "Campus Principal",
    "participantes": 150,
    "equipos": 30,
    "flag": "CTF{cr3d3nc14l3s_pr3d3c1bl3s_s0n_m4l0s}"
}

def login_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def index():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        contraseña = request.form.get('contraseña', '').strip()
        
        # Validación vulnerable - sin protección contra fuerza bruta
        if usuario in USUARIOS and USUARIOS[usuario] == contraseña:
            session['usuario'] = usuario
            session['rol'] = usuario
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciales inválidas', usuario=usuario)
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
@login_requerido
def dashboard():
    usuario = session.get('usuario')
    return render_template('dashboard.html', 
                         usuario=usuario, 
                         evento=EVENTO_INFO)

@app.route('/api/evento', methods=['GET'])
@login_requerido
def api_evento():
    """Endpoint API que devuelve info del evento incluyendo la flag"""
    return jsonify(EVENTO_INFO)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar que el servidor está corriendo"""
    return jsonify({"status": "ok", "app": "CTF Coordinator Portal"})

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    os.makedirs('templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)