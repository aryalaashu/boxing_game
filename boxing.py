import serial
import pygame

# Define the serial port and baud rate.
# Replace 'COM12' with your port name on Windows or '/dev/ttyUSB0' or similar on Linux
ser = serial.Serial('COM12', 9600)

# Initialize pygame mixer
pygame.mixer.init()

def play_song(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

while True:
    try:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        print(line)
        if line:
            parts = line.split(",")
            print(parts)
            if len(parts) == 3:
                # Extracting the  sensor values and average force
                fsr1_str = parts[0].split(": ")[1]
                fsr2_str = parts[1].split(": ")[1]
                avg_force_str = parts[2].split(": ")[1]
                
                fsr1 = int(fsr1_str)
                fsr2 = int(fsr2_str)
                average_force = int(avg_force_str)
                
                print(f"FSR 1: {fsr1}, FSR 2: {fsr2}, Average Force: {average_force}")
                
                if average_force < 950:
                    print("Playing song 1")
                    play_song('barbie.mp3')  
                else:
                    print("Playing song 2")
                    play_song('cena.mp3')  
    except ValueError:
        continue
    except KeyboardInterrupt:
        print("Exiting...")
        break
