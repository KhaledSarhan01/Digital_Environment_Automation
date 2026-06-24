"""
generators.py — Write project subfolders from templates.

Each generator subclass owns one output folder under the project root.
Templates live in templates/ and use string.Template placeholders.

Output folder map:
    RTLGenerator         → <root>/rtl/<module>.sv
    TestbenchGenerator   → <root>/testbench/tb_<module>.sv
    SimulationGenerator  → <root>/sim/*.do + sourcefile.txt
    DocsGenerator        → <root>/docs/readme.txt
"""

import os
from datetime import date
from string import Template

from core import BaseGenerator, Module, Project

TPL = os.path.join(os.path.dirname(__file__), "templates")


def _header(name: str) -> str:
    """Return the standard file header comment block inserted into .sv files."""
    return f"""////////////////////////////////////////////////
///// Project   : {name}
///// Created on: {date.today()}
////////////////////////////////////////////////
"""


class RTLGenerator(BaseGenerator):
    """Generates <root>/rtl/<module.name>.sv from templates/rtl.sv."""

    def generate(self, project: Project, module: Module, root: str) -> None:
        d = os.path.join(root, "rtl")
        os.makedirs(d, exist_ok=True)
        ports, assigns = module.design_ports()
        tpl = Template(open(os.path.join(TPL, "rtl.sv")).read())
        path = os.path.join(d, f"{module.name}.sv")
        with open(path, "w") as f:
            f.write(tpl.substitute(header=_header(module.name), name=module.name,
                                   interface_list=ports, assign_list=assigns))


class TestbenchGenerator(BaseGenerator):
    """Generates <root>/testbench/tb_<module.name>.sv from templates/testbench.sv."""

    def generate(self, project: Project, module: Module, root: str) -> None:
        d = os.path.join(root, "testbench")
        os.makedirs(d, exist_ok=True)
        tb = f"tb_{module.name}"
        sigs, inits = module.tb_ports()
        tpl = Template(open(os.path.join(TPL, "testbench.sv")).read())
        path = os.path.join(d, f"{tb}.sv")
        with open(path, "w") as f:
            f.write(tpl.substitute(header=_header(module.name), tb_name=tb,
                                   module_name=module.name, signals_list=sigs, init_list=inits))


class SimulationGenerator(BaseGenerator):
    """Generates <root>/sim/ QuestaSim scripts and sourcefile.txt."""

    _STATIC = ("reset.do", "done.do", "wave.do")

    def generate(self, project: Project, module: Module, root: str) -> None:
        d = os.path.join(root, "sim")
        os.makedirs(d, exist_ok=True)
        tb = f"tb_{module.name}"
        subs = {"module_name": module.name, "tb_name": tb}
        tpl = Template(open(os.path.join(TPL, "start.do")).read())
        with open(os.path.join(d, "start.do"), "w") as f:
            f.write(tpl.substitute(**subs))
        for name in self._STATIC:
            with open(os.path.join(TPL, name)) as src, open(os.path.join(d, name), "w") as f:
                f.write(src.read())
        tpl = Template(open(os.path.join(TPL, "sourcefile.txt")).read())
        with open(os.path.join(d, "sourcefile.txt"), "w") as f:
            f.write(tpl.substitute(**subs))


class DocsGenerator(BaseGenerator):
    """Generates <root>/docs/readme.txt — copy of the source JSON entity file."""

    def generate(self, project: Project, module: Module, root: str) -> None:
        d = os.path.join(root, "docs")
        os.makedirs(d, exist_ok=True)
        with open(project.source_path) as src, open(os.path.join(d, "readme.txt"), "w") as f:
            f.write(src.read())
