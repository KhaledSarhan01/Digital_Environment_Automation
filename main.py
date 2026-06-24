"""
main.py — Entry point for the Digital IC environment builder.

Run:
    python main.py                  # uses example.json in cwd
    python main.py my_entity.json   # uses a custom entity file

End-to-end flow:
    Step 1 — Parse JSON entity file into a Project (development/parsers.py).
    Step 2 — Create the project root folder named after the entity.
    Step 3 — Initialize git repo and write .gitignore.
    Step 4 — For each Module, run every registered Generator (development/generators.py).
    Step 5 — Stage all files and create the initial git commit.
    Step 6 — Print confirmation with the output path.

Generated folder layout:
    <ProjectName>/
    ├── .gitignore
    ├── rtl/        RTL SystemVerilog module          (RTLGenerator)
    ├── testbench/  SystemVerilog testbench            (TestbenchGenerator)
    ├── sim/        QuestaSim .do scripts + file list (SimulationGenerator)
    └── docs/       Entity spec copy (readme.txt)     (DocsGenerator)
"""

import os
import subprocess
import sys

DEV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "development")
sys.path.insert(0, DEV)

from parsers import parse_json

TPL = os.path.join(DEV, "templates")


def main(json_path="example.json"):
    project = parse_json(json_path)
    root = os.path.join(os.getcwd(), project.name)
    os.makedirs(root, exist_ok=True)

    subprocess.run(["git", "init"], cwd=root, check=True)
    with open(os.path.join(TPL, "gitignore")) as src, open(os.path.join(root, ".gitignore"), "w") as f:
        f.write(src.read())

    for mod in project.modules:
        for gen in project.generators:
            gen.generate(project, mod, root)

    subprocess.run(["git", "add", "--all"], cwd=root, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Environment Setup for {project.name} Project"],
        cwd=root, check=True)

    print(f"Generated {project.name} in {root}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "example.json")
