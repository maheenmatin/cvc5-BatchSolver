# Welcome to cvc5-BatchSolver!

**cvc5-BatchSolver** is a Python tool for batch-processing `.smt2` files using the cvc5 solver and exporting detailed results to a single `.csv` file.

---

**### 🧰 Installation**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/maheenmatin/cvc5-BatchSolver
   cd cvc5-BatchSolver
   ```

2. **Optional: Install Poetry** (if not already installed):
   ```bash
   pipx install poetry
   ```

3. **Install dependencies:**
   ```bash
   poetry install
   ```

4. **Activate the environment:**
   ```bash
   poetry env activate
   ```

5. **Run the solver:**
   ```bash
   poetry run python -m cvc5_batchsolver.cvc5_solver
   # or
   poetry run python src/cvc5_batchsolver/cvc5_solver.py
   ```

---

### 🚀 Why This Project?

While building [CRTSolver](https://github.com/maheenmatin/CRTSolver), a program that leverages the Chinese Remainder Theorem for increased performance in solving non-linear integer equations, I realized there was no easy way to batch-process a folder of SMT-LIB problems using cvc5 while retrieving:

- Satisfiability results
- Variable assignments (models) for satisfiable problems
- Solver runtime
- Problem metadata (e.g. max polynomial degree, number of variables, number of assertions, etc)

To evaluate CRTSolver against native cvc5 and Z3 performance, I built custom batch runners — this tool is the result of generalizing and polishing that effort.

---

### 🔍 What It Does

- Recursively processes all `.smt2` files in a given folder
- Uses cvc5's **base Python API** (more feature-complete than the Pythonic API)
- For each file, extracts:
  - Solver status (`sat`, `unsat`, or `unknown`)
  - Model values (for satisfiable problems)
  - Solver runtime
  - Problem metadata
- Aggregates results into a clean, analyzable `.csv` file

---

### 🧠 Why It’s Different

Most SMT tools are solver-agnostic, and geared toward large-scale experiments with comparisons across different solvers and solver configurations. This project is:
- **Lightweight** and specifically **cvc5-focused**
- Optimized for **CSV output** and **donwstream analysis**
- Intended for **general use cases** where solving a batch of problems takes precedence over benchmarking
- **Easy to integrate** into solver pipelines or research workflows

---

### 📦 Coming Soon
- Support for Z3 via a similar program
- CLI options for controlling timeout and file paths

---

### 🛠️ Feature Comparison

| Project | Description | Focus | Input | Output |
|---------|-------------|-------|--------|--------|
| **[cvc5-BatchSolver](https://github.com/maheenmatin/cvc5-BatchSolver)** | Lightweight batch processor with rich per-file analytics, using cvc5 | Single-solver `.smt2` evaluation and CSV reporting | `.smt2` files | CSV (incl. result, model, and metadata) |
| **[solverpy](https://github.com/cbboyan/solverpy)** | Designed for multi-solver testing and parameter exploration | Multi-solver benchmarking and strategy experimentation | `.smt2` files | JSON (strategy comparison) |
| **[jsi](https://github.com/a16z/jsi)** | Solver portfolio CLI - selects fastest result via parallel runs | Parallel execution and solver competition benchmarking | `.smt2` files | Terminal + optional CSV (basic logs) |
| **[pySMT](https://github.com/pysmt/pysmt)** | Toolkit for building and reasoning about SMT formulas in code | SMT formula construction, manipulation, and solving | Python-defined formulas | No batch output / result aggregation |
