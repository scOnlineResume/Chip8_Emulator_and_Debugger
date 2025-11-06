from emulator import Emulator
import sys

print("***** INSTRUCTIONS *****")
print(" > python  main.py [filepath to game]\n")
print("To run with Debugger:")
print(" > python main.py [filepath to game] DEBUG")
print("Before starting emulator")

arguments = sys.argv

emu = Emulator(arguments)

print("Successfully started emulator")

while True:
    emu.master_loop()