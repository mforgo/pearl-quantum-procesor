# Pearl Quantum Procesor

A playful, educational “quantum processor” simulator built in Python with a tiny custom assembly language or Piquang, created at the Protab 2025 programming camp (Turnus C, 2–9 Aug 2025, Albrechtice v Jizerských horách) and voted the best project among 10 projects of the same turnus.

## Goals
- Program procesor emulator.

## Repository Structure
- src/ — Core simulator and instruction implementations.
- programs/ — Sample programs for the custom assembly language.
- docs/ — Project documentation and supporting materials.
- main.py — Entry point to run the simulator and load programs.
- ASSembly instructions instructions.txt — Instruction set overview and usage guide.
- README.md — This document.

## Installation
Prerequisites:
- Python 3.10+ (recommended)

Steps:
1. Clone the repository:
   - git clone https://github.com/mforgo/pearl-quantum-procesor
   - cd pearl-quantum-procesor
2. (Optional) Create and activate a virtual environment.
3. Install dependencies enviroment.yml. 

## Usage
Basic run:
- python main.py

Typical workflow:
- Pick or write a program in the custom assembly language (see programs/ for examples).
- Consult “ASSembly instructions instructions.txt” for the instruction set and syntax.
- Run with main.py to simulate execution and inspect results or traces.

Outputs may include:
- Register/state dumps after each instruction.
- Final state summary.
- Optional debug traces depending on flags exposed by main.py (check comments/help).

## The ASSembly Language
See “ASSembly instructions instructions.txt” for:
- Instruction set (operations, parameters, effects).
- Program structure and syntax (labels, comments, constants).
- Examples and common pitfalls.

Browse programs/ for working examples to adapt.

## How It Works (Conceptual)
- A small interpreter parses the custom assembly format and executes instruction primitives implemented in src/.
- The state model mimics a simplified, learner-friendly quantum-processor flavor, prioritizing clarity over physical accuracy.
- Step-by-step execution helps visualize how instructions transform state over time.

## Extending the Project
Ideas:
- Add new instructions (extend interpreter + update instruction manual).
- Create more example programs demonstrating control flow and algorithms.
- Improve error messages and validation in the parser.
- Add visualization or richer state inspection (e.g., flags in main.py or a small GUI).
- Write unit tests for parser and instruction semantics.

## Camp Context
- Built at Programátorský tábor Protab 2025, Turnus C (2–9 Aug 2025, Albrechtice v Jizerských horách).
- Voted best project among 10 projects in the same turnus.

## Acknowledgements
- Thanks to Protab organizers and mentors for the environment and guidance.
- Thanks to fellow participants for feedback and the best-project vote.