# N-Way Negator Problem

This project explores the problem of constructing Boolean circuits that can negate multiple input variables using a limited number of NOT gates. Specifically, it investigates circuits that can compute the negation of all inputs simultaneously with minimal NOT gate usage.

## Problem Description

The n-way negator problem asks: What is the minimal number of NOT gates required to build a circuit that negates n input variables? The circuit must work for all possible combinations of Boolean inputs.

For n = 2^s - 1 inputs, the project demonstrates a construction using exactly s NOT gates.

## Files

- `main.py`: Generates Python code for a circuit that negates 2^s - 1 inputs using s NOT gates. The generated circuit uses only AND, OR, and NOT operations.

- `solve-for-3-circuit.py`: Uses a SAT solver to find a specific 3-negator circuit for 3 inputs. Requires the `pysat` library.

- `check-3-circuit.py`: Contains a hand-written implementation of a 3-negator circuit for 3 inputs, along with verification that it works for all input combinations.

## Requirements

- Python 3.14.3 100% works, for lesser version probably too.
- `pysat` library (for `solve-for-3-circuit.py`): Install with `pip install pysat`

## Usage

### Generating Circuits

Run `main.py` interactively:

```bash
python main.py
```

Available commands:

- `gen s [filename]`: Generate a circuit with s NOT gates. If filename is provided, saves to `./generated/filename`, otherwise prints to console.
- `test k`: Test circuits for s = 1 to k.
- `measure k`: Measure the length of generated code for s = 1 to k.

**Warning**: For s > 4, the generated code grows exponentially and may be very large.

### Solving for 3-Negator Circuit

```bash
python solve-for-3-circuit.py
```

This will output the SAT model defining the circuit structure.

### Verifying the 3-Negator Circuit

```bash
python check-3-circuit.py
```

This verifies that the hand-written circuit correctly negates all 3 inputs for every possible input combination.

## Results

- For 3 inputs (n=3), a circuit using 3 NOT gates exists (demonstrated in `check-3-circuit.py`).
- The general construction provides circuits for n = 2^s - 1 inputs using s NOT gates.
- The SAT solver confirms the existence of such circuits for small n.

Here is measured size of circuits.

| s | n  | code length | log2(code length) |
|---|----|-------------|-------------------|
| 1 | 1  | 85          | 6.41              |
| 2 | 3  | 499         | 8.96              |
| 3 | 7  | 14721       | 13.85             |
| 4 | 15 | 14835857    | 23.82             |

Best fit curve of code length versus n: y = 19.2 + 34.6 * 2.73^x
Wow that's very bad.
