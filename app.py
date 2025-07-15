import os
import string
import subprocess
from datetime import date

#####################################################
######## Step 0: Project Class and Functions ########
#####################################################
class Signal:
    def __init__(self, name, direction, width, init=0):
        self.name = name
        self.direction = direction
        self.width = width
        self.init = init

    def __str__(self):
        return f"{self.direction} {self.name} [{self.width}-bit]{' init=' + str(self.init) if self.init is not None else 0}"

class Block:
    def __init__(self, name):
        self.name = name
        self.signals = []

    def add_signal(self, signal: Signal):
        self.signals.append(signal)

    def __str__(self):
        result = f"Block: {self.name}\n"
        for sig in self.signals:
            result += f"  {sig}\n"
        return result

    def design_list(self):
        interface_list = []  # Hold Interface in Design
        assign_list = []     # Hold Assign Statements for the output
        for sig in self.signals:
            # Format the width as [width-1:0] only if width > 1
            width_str = f"[{sig.width - 1}:0] " if sig.width > 1 else ""
            # make Design interface
            if sig.direction == "output":
                interface_list.append(f",output logic {width_str} o_{sig.name}")
                assign_list.append(f"assign o_{sig.name} = 'h{sig.init};")
            elif sig.direction == "input":
                interface_list.append(f",input  logic {width_str} i_{sig.name}")
            else:
                continue
        return "\n \t".join(interface_list),"\n \t".join(assign_list)

    def testbench_list(self):
        signal_list = []  # Hold Signals Section in Testbench
        init_list   = []  # Hold Initialization Section in Testbench
        for sig in self.signals:
            # Format the width as [width-1:0] only if width > 1
            width_str = f"[{sig.width - 1}:0] " if sig.width > 1 else ""
            # make Design interface
            if sig.direction == "output":
                signal_list.append(f"logic {width_str} o_{sig.name};")
            elif sig.direction == "input":
                signal_list.append(f"logic {width_str} i_{sig.name};")
                init_list.append(f" i_{sig.name} = 'h{sig.init};")
            else:
                continue
        return "\n \t".join(signal_list),"\n \t \t".join(init_list)

def parse_signal_file(filename):
    # Create a dictionary to store the parsed data
    block = None
    # Open the file for reading
    with open(filename, 'r') as file:
        # Read all lines into a list
        lines = file.readlines()

    # Loop through each line with its index
    for i, line in enumerate(lines):
        # Remove leading/trailing whitespace
        line = line.strip()
        # If the line starts with "Name:", extract the name
        if line.startswith("Name:"):
            # Split at the first ":" and get the part after it
            block_name = line.split(":", 1)[1].strip()
            block = Block(block_name)
        # If the line is "Signals:", begin parsing signals starting from next lines
        elif line.startswith("Signals:") and block:
            # Loop through the rest of the lines starting from the next one
            for signal_line in lines[i + 1:]:
                signal_line = signal_line.strip() # Clean whitespace
                # Stop if we reach an empty line
                if not signal_line:
                    break
                # Split the line into parts: name, direction, width, (optional init)
                parts = signal_line.split()
                # Ignore lines that don't have at least 3 parts
                if len(parts) < 3:
                    continue
                # Extract signal Parts
                name = parts[0]
                direction = parts[1]
                width = int(parts[2])
                init = int(parts[3]) if len(parts) > 3 else 0
                # Add this signal to the signals list
                signal = Signal(name, direction, width, init)
                block.add_signal(signal)

            # Exit the loop since we've finished parsing the signals
            break
    # Return the full parsed data structure
    return block

#####################################################
######## Step 1: Creating the project Folder ########
#####################################################
filename = "example2.txt"              # Replace this with your file path
# Parse the file
block = parse_signal_file(filename)

project_name   = block.name
current_directory = os.getcwd()
testbench_name = f"tb_{project_name}"
today = date.today()
header = f"""////////////////////////////////////////////////
///// Project   : {project_name}             
///// Created on: {today}
///// Version   : 1.0                   
////////////////////////////////////////////////
"""
# Step 1.1: Making the Folder
project_folder = os.path.join(current_directory, project_name)
os.makedirs(project_folder, exist_ok=True)
# Step 1.2: Initiating the Git Repo
os.chdir(project_folder)
subprocess.run(["git", "init"], check=True)

#####################################################
######## Step 2: Creating the Design Folder #########
#####################################################

# Step 2.1: Folder Creation
design_folder = os.path.join(project_folder, "Design")
os.makedirs(design_folder, exist_ok=True)

# Step 2.2: Content
design_file_template = string.Template("""$header
module $project_name (
// Clock and active low Asynchronous Reset
    input logic clk,rst_n 
// Signals    
    $interface_list
);
// Enter your code here
// THIS IS DUMMY CODE
    $assign_list
endmodule
""")

# Step 2.3: Create a SystemVerilog file in 'Design'
design_file_path = os.path.join(design_folder, f"{project_name}.sv")
with open(design_file_path, "w") as f:
    f.write(design_file_template.substitute(project_name   = project_name,
                                            header          = header,
                                            interface_list = block.design_list()[0],
                                            assign_list    = block.design_list()[1]))

#####################################################
##### Step 3: Creating the Simulation Folder ########
#####################################################

# Step 3.1: Folder Creation
simulation_folder = os.path.join(project_folder, "Simulation")
os.makedirs(simulation_folder, exist_ok=True)
# Step 3.2: Content
start_do_text = string.Template("""
vlib work
vlog -f sourcefile.txt -svinputport=relaxed
vsim -voptargs=+acc work.$testbench_name
do wave.do
run -all
""")

reset_do_text = string.Template("""
vlog -f sourcefile.txt -svinputport=relaxed
restart -force
run -all
""")

done_do_text = string.Template("""
quit -sim
exit -force
""")

wave_do_text = string.Template("""
delete wave *
add wave *
""")

sourcefile_text = string.Template("""
../Design/$project_name.sv
../Testbench/$testbench_name.sv
""")
# Step 3.3: Create .do files and one .txt file in 'Simulation'
filepath = os.path.join(simulation_folder, "sourcefile.txt")
with open(filepath, "w") as f:
    f.write(sourcefile_text.substitute(testbench_name = testbench_name,project_name = project_name))

filepath = os.path.join(simulation_folder, "start.do")
with open(filepath, "w") as f:
    f.write(start_do_text.substitute(testbench_name = testbench_name))

filepath = os.path.join(simulation_folder, "reset.do")
with open(filepath, "w") as f:
    f.write(reset_do_text.template)

filepath = os.path.join(simulation_folder, "done.do")
with open(filepath, "w") as f:
    f.write(done_do_text.template)

filepath = os.path.join(simulation_folder, "wave.do")
with open(filepath, "w") as f:
    f.write(wave_do_text.template)

#####################################################
####### Step 4: Creating the Testbench Folder #######
#####################################################

# Step 4.1: Folder Creation
testbench_folder = os.path.join(project_folder, "Testbench")
os.makedirs(testbench_folder, exist_ok=True)
# Step 4.2: Content
testbench_text = string.Template("""$header
module $testbench_name ;
//////////////////////////////////////
////////////// Signals //////////////
////////////////////////////////////
    logic clk,rst_n;
    $signals_list
//////////////////////////////////////
///////// Clock Generation //////////
////////////////////////////////////
    localparam CLK_PERIOD = 10;
    initial begin
        clk = 1'b0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end
    
//////////////////////////////////////
/////////// Instantiation ///////////
////////////////////////////////////
    $project_name DUT (.*);

//////////////////////////////////////
////////// Testbench Core ///////////
////////////////////////////////////

// Core
    initial begin
        Initialization();
        Reset();
        Main_Scenario();
        Finish();
    end
    
    task Reset;
        rst_n = 1'b0;
        @(negedge clk);
        rst_n = 1'b1;
    endtask
    
    task Finish;
        repeat(100) @(negedge clk);
        $$stop;
    endtask
// Watch dog works after 10 ms in simulation time 
    initial begin
        #1000000;
        $$display("Simulation is not working");
        $$stop; 
    end  

//////////////////////////////////////
//////// Testbench Scenarios ////////
////////////////////////////////////
    task Initialization;
        // Initialize your Signals Here
        $init_list
    endtask
    task Main_Scenario();
        // Write your Test Scenario Here
    endtask
endmodule
""")
# Step 4.3: Create testbench.sv in 'Testbench'
testbench_file_path = os.path.join(testbench_folder, f"{testbench_name}.sv")
with open(testbench_file_path, "w") as f:
    f.write(testbench_text.substitute(testbench_name = testbench_name,
                                      header         = header,
                                      project_name   = project_name,
                                      signals_list   = block.testbench_list()[0],
                                      init_list      = block.testbench_list()[1]))

#####################################################
########### Step 5: Commiting First Commit ##########
#####################################################
os.chdir(project_folder)
subprocess.run(["git", "add","--all"], check=True)
subprocess.run(["git", "commit",f"-m\"Environment Setup for {project_name} Project\""], check=True)