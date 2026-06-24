"""
parsers.py — Read JSON entity files and build Project objects.

This is the first transformation step after main.py receives a file path.
It converts the user-supplied entity specification into core.py data structures
and attaches the generator list that main.py will invoke.

Expected JSON shape:
    {
        "Name": "<module_name>",
        "Signals": [
            {"name": "...", "direction": "input|output", "width": N, "init": N},
            ...
        ]
    }
"""

import json
from core import Module, Project, Signal
from generators import DocsGenerator, RTLGenerator, SimulationGenerator, TestbenchGenerator


def parse_json(path: str) -> Project:
    """
    Parse a JSON entity file into a fully configured Project.

    Step 1 — Open and load the JSON file from disk.
    Step 2 — Create a Project using the "Name" field (fallback: "Unnamed").
    Step 3 — Create the top-level Module with the same name as the project.
    Step 4 — For each entry in "Signals":
                 skip entries missing name or direction;
                 build a Signal with optional width (default 1) and init (default 0);
                 append it to the module.
    Step 5 — Register generators in run order:
                 RTLGenerator       → rtl/
                 TestbenchGenerator → testbench/
                 SimulationGenerator → sim/
                 DocsGenerator      → docs/
    Step 6 — Return the Project ready for main.py to iterate.
    """
    with open(path) as f:
        data = json.load(f)

    project = Project(name=data.get("Name", "Unnamed"), source_path=path)
    mod = Module(name=project.name)

    for s in data.get("Signals", []):
        if s.get("name") and s.get("direction"):
            mod.signals.append(Signal(
                s["name"], s["direction"], s.get("width", 1), s.get("init", 0)))

    project.modules.append(mod)
    project.generators = [
        RTLGenerator(), TestbenchGenerator(), SimulationGenerator(), DocsGenerator()]
    return project
