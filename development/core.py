"""
core.py — Data model for the Digital IC environment builder.

This module defines the in-memory representation of a design project.
Nothing is written to disk here; parsers.py builds these objects from JSON,
and generators.py reads them to produce output folders.

Pipeline role:
    JSON entity file  →  parsers.py  →  Project / Module / Signal  →  generators.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class Signal:
    """
    One port on a module, matching a single entry in the JSON "Signals" array.

    Attributes:
        name:      Port name from JSON (e.g. "data_bus").
        direction: "input" or "output".
        width:     Bit width; defaults to 1 when omitted in JSON.
        init:      Initial/reset value written into RTL assigns and TB init tasks.
    """
    name: str
    direction: str
    width: int = 1
    init: int = 0


@dataclass
class Module:
    """
    One RTL block (top-level module for now).

    Holds all signals and exposes helpers that format SystemVerilog snippets
    used by RTLGenerator and TestbenchGenerator.
    """
    name: str
    signals: List[Signal] = field(default_factory=list)

    def design_ports(self):
        """
        Build RTL port list and placeholder assign statements.

        Step 1 — Walk every Signal on this module.
        Step 2 — For multi-bit signals, format width as [N-1:0].
        Step 3 — Prefix ports with i_ (input) or o_ (output) to avoid name clashes.
        Step 4 — For outputs, add dummy assign lines using the signal init value.

        Returns:
            (interface_list, assign_list) — two strings joined for template substitution.
        """
        ports, assigns = [], []
        for s in self.signals:
            w = f"[{s.width - 1}:0] " if s.width > 1 else ""
            if s.direction == "output":
                ports.append(f",output logic {w}o_{s.name}")
                assigns.append(f"assign o_{s.name} = 'h{s.init};")
            elif s.direction == "input":
                ports.append(f",input  logic {w}i_{s.name}")
        return "\n \t".join(ports), "\n \t".join(assigns)

    def tb_ports(self):
        """
        Build testbench signal declarations and input initialization lines.

        Step 1 — Walk every Signal on this module.
        Step 2 — Declare logic variables matching DUT port names (i_/o_ prefix).
        Step 3 — For inputs only, emit init assignments for the Initialization task.

        Returns:
            (signals_list, init_list) — two strings joined for template substitution.
        """
        sigs, inits = [], []
        for s in self.signals:
            w = f"[{s.width - 1}:0] " if s.width > 1 else ""
            if s.direction == "output":
                sigs.append(f"logic {w}o_{s.name};")
            elif s.direction == "input":
                sigs.append(f"logic {w}i_{s.name};")
                inits.append(f" i_{s.name} = 'h{s.init};")
        return "\n \t".join(sigs), "\n \t \t".join(inits)


@dataclass
class Project:
    """
    Root container for one generated environment.

    Attributes:
        name:        Project / top-module name (from JSON "Name").
        source_path: Path to the JSON entity file (used by DocsGenerator).
        modules:     List of Module objects (one top module today; submodules later).
        generators:  Generator instances that will write each output folder.
    """
    name: str
    source_path: str = ""
    modules: List[Module] = field(default_factory=list)
    generators: list = field(default_factory=list)


class BaseGenerator(ABC):
    """
    Abstract base for all output-folder writers.

    Each concrete generator implements generate() and is responsible for
    one project subfolder (rtl/, testbench/, sim/, docs/, etc.).
    """

    @abstractmethod
    def generate(self, project: Project, module: Module, root: str) -> None:
        """
        Write generated files under root/<folder>/.

        Args:
            project: Full project context (name, generator list, etc.).
            module:  The module whose ports drive this generation pass.
            root:    Absolute path to the project output directory.
        """
        pass
