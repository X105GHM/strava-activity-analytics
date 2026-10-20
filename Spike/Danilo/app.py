import platform

system = platform.system()

if system == "Linux":
    print("Hallo Linux")
elif system == "Windows":
    print("Hallo Windows")
else:
    print("Unbekanntes Betriebssystem") 