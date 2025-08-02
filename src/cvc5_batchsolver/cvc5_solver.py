from pathlib import Path
import cvc5
import time
import argparse
import cvc5_batchsolver.input_output.reader as reader
import cvc5_batchsolver.input_output.writer as writer

# NOTE: Inspired by code and instructions from the following sources:
# NOTE: https://cvc5.github.io/docs-ci/docs-main/api/python/base/quickstart.html
# NOTE: https://cvc5.github.io/docs-ci/docs-main/examples/parser.html
class cvc5Solver:
    def __init__(self, time_limit, solver_name="cvc5", tests_dir=None):
        if tests_dir is None:
            # Set root directory using existing file structure
            # cvc5-BatchSolver -> src -> cvc5_batchsolver -> cvc5_solver.py
            self.ROOT = Path(__file__).resolve().parents[2]
            self.TESTS = self.ROOT / "tests"
        else:
            # Use provided tests directory to set root directory
            self.TESTS = Path(tests_dir)
            self.ROOT = self.TESTS.parents[0]

        # Results are in a sibling directory to the tests directory
        self.RESULTS = self.ROOT / "results"

        self.time_limit = time_limit
        self.solver_name = solver_name
        self.writer = writer.Writer(self.RESULTS, self.solver_name)
        
    def reinit(self):
        # Create solver
        self.solver = cvc5.Solver()
        
        # Set solver options
        self.solver.setOption("produce-models", "true") # allows model retrieval
        self.solver.setOption("produce-unsat-cores", "true") # allows unsat core retrieval
        self.solver.setOption("tlimit-per", self.time_limit) # time limit for each check-sat
        self.solver.setLogic("QF_ALL")

        self.start_time = time.time()
        self.sat_model = [] # if SAT, stores satisfying values

    def get_solver_name(self):
        return self.solver_name

    def execute(self):
        for file in reader.get_sorted_files(self.TESTS):
            if file.is_file():
                # Reinitialize data for new file
                self.reinit()
                print(f"Reading file: {file}")

                with file.open("r") as input:
                    input_code = input.read()

                # Create parser
                parser = cvc5.InputParser(self.solver)

                # Send input code to parser
                parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6, input_code, "")

                # Get symbol manager for parser
                sm = parser.getSymbolManager()

                # Parse all commands in input code
                while True:
                    command = parser.nextCommand()
                    if command.isNull():
                        break
                    # Invoke command using solver and symbol manager
                    print(command.invoke(self.solver, sm), end="")

                # Check satisfiability
                result = self.solver.checkSat()
                if result.isSat():
                    # Get all declared variable names and terms
                    declared_terms = sm.getDeclaredTerms()
                    for term in declared_terms:
                        name = str(term) # constant name
                        model = self.solver.getValue(term) # constant value
                        self.sat_model.append([name, model])
                elif result.isUnsat():
                    self.sat_model.append(["UNSAT"])
                elif result.isUnknown():
                    self.sat_model.append(["UNKNOWN (TIMEOUT)"])

                print()
                self.writer.store_result(file, self.start_time, self.sat_model)
        self.writer.write()

# CLI entry point
def main():
    parser = argparse.ArgumentParser(description="Run the cvc5 solver on a directory of SMT2 files.")
    parser.add_argument("--time_limit", required=True, type=int, 
        help="Time limit for each check-sat (in ms).")
    parser.add_argument("--solver_name", default="cvc5",
        help="Name for the solver run (used in output results).")
    parser.add_argument("--tests_dir", default=None, 
        help="Path to directory containing test SMT2 files.")
    args = parser.parse_args()

    solver = cvc5Solver(
        time_limit=str(args.time_limit),
        solver_name=args.solver_name,
        tests_dir=args.tests_dir
    )
    solver.execute()

if __name__ == "__main__":
    main()
