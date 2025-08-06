# main.py

from src.procesor import Procesor

def main():
    cpu = Procesor(debug=True)
    # Load your assembly file; path is relative to where you run main.py
    if not cpu.load_program("programs/myprog.asm"):
        return
    cpu.run()

if __name__ == "__main__":
    main()
