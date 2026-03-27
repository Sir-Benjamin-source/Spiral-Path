# tools/run_testbed.py
from testbed_integration import run_full_testbed

if __name__ == "__main__":
    test_input = input("Enter test spark (or press Enter for default): ") or "Evaluate continuity and provenance in multi-variable pattern propagation for agent systems."
    run_full_testbed(test_input, iterations=3, branches=3)