# src/procesor.py

class Procesor:
    def __init__(self):
        self.running = True  # Control flag for the run loop, can be replaced as needed

    def step(self):
        # Placeholder: one step of the processor ("fetch-decode-execute") or quantum operation
        print("Procesor: Executing a cycle (quantum or classical emulation)")

    def run(self):
        # Main processor loop
        print("Procesor: Starting main run loop.")
        while self.running:
            self.step()
            # For demo, ask to continue (replace with your halt condition)
            cmd = input("Continue? (y/n): ").strip().lower()
            if cmd != 'y':
                self.running = False
        print("Procesor: Stopped.")
