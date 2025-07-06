import os
import string
import subprocess
#####################################################
######## Step 1: Creating the project Folder ########
#####################################################
# project_name   = input("Write Project Name:")
project_name = "example"
testbench_name = f"tb_{project_name}"
os.makedirs(project_name, exist_ok=True)
subprocess.run(["git","init"])
#####################################################
######## Step 2: Creating the Design Folder #########
#####################################################

# Step 2.1: Folder Creation
design_folder = os.path.join(project_name, "Design")
os.makedirs(design_folder, exist_ok=True)

# Step 2.2: Content
design_file_template = string.Template("""module $project_name (
// Clock and active low Asynchronous Reset
    input logic clk,rst_n 
// Signals    
    //,
);
// Enter your code here
endmodule
""")

# Step 2.3: Create a SystemVerilog file in 'Design'
design_file_path = os.path.join(design_folder, f"{project_name}.sv")
with open(design_file_path, "w") as f:
    f.write(design_file_template.substitute(project_name = project_name))

#####################################################
##### Step 3: Creating the Simulation Folder ########
#####################################################

# Step 3.1: Folder Creation
simulation_folder = os.path.join(project_name, "Simulation")
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
testbench_folder = os.path.join(project_name, "Testbench")
os.makedirs(testbench_folder, exist_ok=True)
# Step 4.2: Content
testbench_text = string.Template("""
module $testbench_name ;
//////////////////////////////////////
////////////// Signals //////////////
////////////////////////////////////
    logic clk,rst_n;

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
    endtask
    task Main_Scenario();
        // Write your Test Scenario Here
    endtask
endmodule
""")
# Step 4.3: Create testbench.sv in 'Testbench'
testbench_file_path = os.path.join(testbench_folder, f"{testbench_name}.sv")
with open(testbench_file_path, "w") as f:
    f.write(testbench_text.substitute(testbench_name = testbench_name,project_name = project_name))

#####################################################
########### Step 5: Commiting the Changes ###########
#####################################################
subprocess.run(["git","add","--all"])
subprocess.run(["git","commit","-m\"first_commit\""])