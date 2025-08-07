# main.py

from src.procesor import Procesor

def main():
    cpu = Procesor(debug=True, mode="hybrid")
    # Load your assembly file; path is relative to where you run main.py
    if not cpu.load_program("programs/quantum_bell.asm"):
        return
    cpu.run()

if __name__ == "__main__":
    main()
