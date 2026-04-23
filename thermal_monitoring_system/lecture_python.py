import serial
import time
import csv
import matplotlib.pyplot as plt

# CONFIGURATION
PORT = 'COM3'   
BAUD_RATE = 9600
FICHIER = "donnees.csv"

# CONNEXION 
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(10)
    print(f"Connecté à {PORT}")
except:
    print("Erreur connexion port")
    exit()

# DONNÉES 
temps_data = []
temp_data = []
pot_data = []

# GRAPHIQUE 
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.tight_layout(pad=3)

# FICHIER CSV 
with open(FICHIER, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Temps (s)", "Température (°C)", "Potentiomètre"])

    start = time.time()

    try:
        while True:
            ligne = ser.readline().decode().strip()

            if not ligne:
                continue

            print("RAW:", ligne)  

            # PARSING 
            if "TEMP:" in ligne and "POT:" in ligne:
                try:
                    parts = ligne.split(";")

                    temp = float(parts[0].split(":")[1])
                    pot = float(parts[1].split(":")[1])

                    t = round(time.time() - start, 2)

                    # SAUVEGARDE CSV 
                    writer.writerow([t, temp, pot])
                    f.flush()

                    # STOCKAGE 
                    temps_data.append(t)
                    temp_data.append(temp)
                    pot_data.append(pot)

                    # LIMITATION AFFICHAGE 
                    temps_aff = temps_data[-50:]
                    temp_aff = temp_data[-50:]

                    # GRAPHIQUE TEMP / TEMPS 
                    ax1.clear()
                    ax1.plot(temps_aff, temp_aff)
                    ax1.set_title("Température vs Temps")
                    ax1.set_ylabel("Temp (°C)")
                    ax1.grid()

                    # GRAPHIQUE TEMP / POT 
                    ax2.clear()
                    ax2.scatter(pot_data, temp_data)
                    ax2.set_title("Température vs Potentiomètre")
                    ax2.set_xlabel("Pot (0-1023)")
                    ax2.set_ylabel("Temp (°C)")

                    plt.pause(0.01)

                    print(f"T={temp}°C | POT={pot}")

                except:
                    print("Erreur parsing")

    except KeyboardInterrupt:
        print("\nArrêt du programme")

    finally:
        ser.close()
        plt.ioff()
        plt.show()