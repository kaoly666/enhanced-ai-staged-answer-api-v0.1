print("starting...")

from app import app
import subprocess
import time

time.sleep(1)
print("working...")
time.sleep(1)

if __name__ == "__main__":
    # Inicia ngrok em background
    ngrok = subprocess.Popen(["ngrok", "http", "5000"])
    
    # Da tempo pro ngrok iniciar
    print("working...")
    time.sleep(2)
    print("starting subprocess")
    print("Server running in: http://127.0.0.1:5000")
    print("Ngrok in:")
    subprocess.call(["curl", "-s", "http://localhost:4040/api/tunnels"])
    print("starting flask...")
    time.sleep(1)

    # Inicia o Flask
    app.run(host="0.0.0.0", port=5000)
    print("flask running...")
