# Digital Design Environment Creation Tool

This tool is created to automate the Environment Creation of Digital IC Design and Verification Projects 
given their Entity Specifications only.

## How it work

1. write JSON Entity file describing the Name and Port Mapping of the project -same as Entity Construct in VHDL-.
2. run the Python Script to generate the Environment Setting to start building your Project.
3. To run the Environment on Questasim:
  a. Create New project in Simulation Folder 
    b. run the following script in Transcript

> do start.do
>
> 1. To debug the code in Questasim, run the following script in Transcript
>
> do reset.do
>
> 1. After finishing working on the project, close the project by running
>
> do done.do

## Generated Environment Example

### JSON Entity File

```
{
"Name": "Example",
"Signals":[
{"name":        "header_bus",
 "direcrion":   "input",
 "width":       32, 
 "inital":      0},
{"name":        "header_valid",
 "direcrion":   "input",
 "width":       1, 
 "inital":      0}, 
{"name":        "data_bus",
 "direcrion":   "input",
 "width":       32, 
 "inital":      0},
{"name":        "data_valid",
 "direcrion":   "input",
 "width":       1, 
 "inital":      0},
{"name":        "code_bus",
 "direcrion":   "output",
 "width":       32, 
 "inital":      0},
{"name":        "code_valid",
 "direcrion":   "output",
 "width":       1, 
 "inital":      0}
]
}
```

### Environment

```
Example
|- docs
| |- readme.txt
|- rtl
| |- Example.sv
|- sim
| |- start.do
| |- reset.do
| |- done.do
| |- sourcefile.txt
|- testbench
| |- tb_Example.sv
| .gitignore
```

## Versions

> Current Version: 1.5

### Latest Features

- improve the code maintainability and scalability for future improvements. 
- JSON file can be passed into script instead of txt file.
- improved Header in Design and testbench file.
- Markdown is created.
- some folder names are edited.
- Development Goals are clarified.

# Development Plan

## Version 1.0

- version 1.0: create a working script which uses .txt file as Entity
- version 1.1: add improvements to script
- version 1.2: use .json File instead of .txt file as Entity file.
- version 1.3: some folder names are edited.
- version 1.4: add .gitignore file.
- version 1.5: improve the code maintainability and scalability for future improvements.
- version 1.6: add more scripts for synthesis and linting.

## Version 2.0

- version 2.0: Use UVM Environment instead of SystemVerilog Testbench.
- version 2.1: handling multiple level project.

## Version 3.0

- version 3.0: Add GUI for further script running
- version 3.1: make website and deploy the code for others to use.****

