# IO Module Overview for Pearl Quantum Processor

This module provides input and output handling functionality for the Pearl Quantum Processor, including reading program files, parsing them, managing user input, and output logging.

---

## ProgramLoader

Responsible for loading and saving programs in different formats (assembly text, JSON).

### Methods

- `load_program(filename: str) -> List[Dict]`  
  Loads a program from a file. Supports `.asm`, `.txt`, `.json`, `.qasm` extensions.  
  Returns a list of instructions in dictionary form.

- `_parse_text_program(content: str) -> List[Dict]`  
  Parses assembly-like text programs line-by-line, ignoring comments and blank lines.

- `_parse_json_program(content: str) -> List[Dict]`  
  Parses JSON formatted programs expecting a list of instructions or a dictionary with an 'instructions' key.

- `save_program(instructions: List[Dict], filename: str, format='text')`  
  Saves instructions to a file in text or JSON format.

- `validate_program(instructions: List[Dict]) -> List[str]`  
  Validates the program for valid opcodes and instruction formatting.

- `create_sample_program(filename: str)`  
  Writes a sample assembly program to a file.

### Example Usage

```

loader = ProgramLoader()
program = loader.load_program("programs/test.asm")
errors = loader.validate_program(program)
if errors:
print("Validation errors:", errors)
else:
loader.save_program(program, "output_test.asm")

```

---

## InputHandler

Handles user input from keyboard or files, buffers inputs, and supports loading programs from strings.

### Methods

- `read_keyboard_input(prompt: str) -> str`  
  Reads a line of input from the user.

- `read_file_input(filename: str) -> str`  
  Reads entire contents of a file as a string.

- `load_program_from_string(program_str: str) -> bool`  
  Loads and parses a program from a multiline string. Returns True on success, False on failure.

- `buffer_input(data: str or list)`  
  Adds data to an internal input buffer.

- `get_buffered_input() -> Optional[str]`  
  Retrieves and removes the next item from the input buffer.

- `has_buffered_input() -> bool`  
  Checks if there is any buffered input available.

- `clear_buffer()`  
  Clears the input buffer.

### Example Usage

```

input_handler = InputHandler()
user_input = input_handler.read_keyboard_input()
file_content = input_handler.read_file_input("input.txt")

asm_code = '''
mov 5 p0
add p0 2
out p0
'''
success = input_handler.load_program_from_string(asm_code)
if success:
print("Program loaded successfully from string")

```

---

## OutputHandler

Manages output to the console and optional logging to a file with timestamped entries.

### Initialization

- `__init__(log_to_file=False, log_filename="processor_output.log")`  
  If `log_to_file` is `True`, output and errors are logged to the specified file.

### Methods

- `print_output(message: str, end='\n')`  
  Prints a message to stdout, also logs if enabled.

- `print_error(error_message: str)`  
  Prints error messages to stderr, also logs if enabled.

- `print_debug(debug_message: str, debug_enabled: bool)`  
  Prints debug messages only if debug is enabled, also logs if enabled.

- `write_to_file(filename: str, content: str)`  
  Writes content to a given file.

- `append_to_file(filename: str, content: str)`  
  Appends content to a given file.

- `buffer_output(message: str)`  
  Adds a message to an internal buffer.

- `flush_buffer()`  
  Prints all buffered output messages and clears the buffer.

- `clear_buffer()`  
  Clears the output buffer without printing.

### Notes

- All file operations handle IO errors and report accordingly without stopping the program.
- Logging entries are timestamped with the current time `[HH:MM:SS]`.

### Example Usage

```

output = OutputHandler(log_to_file=True)
output.print_output("Starting simulation...")
output.print_debug("Quantum gate applied", debug_enabled=True)
output.print_error("Error loading program")

output.buffer_output("Buffered message 1")
output.buffer_output("Buffered message 2")
output.flush_buffer()

```

---

## Summary

The `io` package of the Pearl Quantum Processor provides robust support for:

- Loading quantum assembly programs from files or strings.
- Validating and saving programs.
- Interactive or file-based input.
- Console and file logging output with debug support.
- Buffered message handling for cleaner output management.

These tools facilitate user interaction, program management, and detailed runtime diagnostics needed for effective quantum-classical hybrid simulations.

---

**Source Files:**

- `io/program_loader.py`  
- `io/input_handler.py`  
- `io/output_handler.py`  

Each implements parts described above used in your processor core and testing workflows.
