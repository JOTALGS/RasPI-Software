import os
import time
from gpiozero import PWMOutputDevice

FAN_PIN = 14  # Pin GPIO donde está conectado el ventilador (cambia si es necesario)
ON_TEMP = 40  # Temperatura (°C) para que el ventilador se encienda
OFF_TEMP = 38  # Temperatura (°C) para que el ventilador se apague

fan = PWMOutputDevice(FAN_PIN)  # Inicializa el ventilador con control PWM

def get_cpu_temp():
    """Obtiene la temperatura de la CPU del Raspberry Pi."""
    temp = os.popen("vcgencmd measure_temp").readline()
    return float(temp.replace("temp=", "").replace("'C\n", ""))

def set_fan_speed(temp):
    """Establece la velocidad del ventilador según la temperatura."""
    if 40 <= temp < 45:
        fan.value = 0.20  # 20% de la capacidad
    elif 45 <= temp < 50:
        fan.value = 0.35  # 35% de la capacidad
    elif 50 <= temp < 55:
        fan.value = 0.50  # 50% de la capacidad
    elif 55 <= temp < 60:
        fan.value = 0.65  # 65% de la capacidad
    elif 60 <= temp < 65:
        fan.value = 0.80  # 80% de la capacidad
    elif temp >= 65:
        fan.value = 1.00  # 100% de la capacidad
    elif temp <= OFF_TEMP:
        fan.value = 0  # Apagar el ventilador si la temperatura es menor que OFF_TEMP

while True:
    temp = get_cpu_temp()
    
    if temp >= ON_TEMP:
        set_fan_speed(temp)
        print(f"Fan Speed {fan.value*100}% at {temp}°C")
    else:
        fan.value = 0  # Si la temperatura es menor que ON_TEMP, el ventilador se apaga
        print(f"Fan OFF at {temp}°C")
    
    time.sleep(5)  # Revisar la temperatura cada 5 segundos
