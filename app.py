###########################################################################################################
#            ** Digital Design Environment Setup Application **
# ** Overview:
#   The idea behind this python script is to automate the setup of Digital
# IC Design and verification Environment since it was noticed that the setup
# operation is repetitive and straight forward and I see this Python app as
# Good practicing on real life application that can be useful for my development.
#
# ** Main Features
#   --> Setting up a "Design" Folder that contains
#       - Design Module with given "module_name.sv" contain the basic module features
#           . Basic Module Features:
#                 module <module_name> #(//write your parameters here)
#                 (// write your interface here);
#                       // Start your code here
#                 endmodule
#   --> Setting up a "Verification" Folder that contains
#       - "top.sv" module which contain the basic testbench component
#           . Basic Testbench Features:
#               module tb_<module_name>;
#                   // Add your Signals and Variables here
#                       bit tb_clock;
#                       // add DUT interface Signals here
#                   // DUT Instantiation
#                       <module_name> DUT
#                       (// connect DUT interface Signals with Testbench Signals);
#                   // Clock Generation
#                       localparm Clock_Period = 1;
#                       always #(Clock_Period/2) tb_clock =~ tb_clock;
#                       initial tb_clock = 1'b0;
#                   // Testcases
#                       initial begin
#                           // write your Testcases here
#                           // End Testbench
#                               #10; $stop;
#                       end
#               endmodule
#   --> Setting up "Simulation" Folder that contains
#       - "sourcfile.txt" contains all folders names that was created by the script.
#       - "start.do" contains script for the questasim to start build up environment.
#       - "reset.do" contains script for the questasim to rebuild the environment during debugging.
#       - "done.do"  contains script for the questasim to finish the environment safely.
############################################################################################################
import argparse
import os

# ######################## Main Functions ########################
# def create_folder(folder_name):
#     """Creates a folder"""
#     os.makedirs(folder_name, exist_ok=True)
#     print(f"Folder '{folder_name}' created successfully!")
#
#
# def create_file(folder_name, file_name):
#     """Creates a file inside a specified folder"""
#     os.makedirs(folder_name, exist_ok=True)
#     file_path = os.path.join(folder_name, file_name)
#     with open(file_path, 'w') as f:
#         f.write("")
#     print(f"File '{file_path}' created successfully!")
#
#
# def Design_Folder():
#     create_folder("Design")
#

###################### Application Interfacing #####################
# parser = argparse.ArgumentParser(description="Create folders and files")
# parser.add_argument("command", choices=["create_folder", "create_file"], help="Command to execute")
# parser.add_argument("folder_name", help="Folder name")
# parser.add_argument("file_name", nargs="?", help="File name (required for create_file)")
#
# args = parser.parse_args()
#
# if args.command == "create_folder":
#     create_folder(args.folder_name)
# elif args.command == "create_file":
#     if not args.file_name:
#         print("Error: You must provide a file name for 'create_file'.")
#     else:
#         create_file(args.folder_name, args.file_name)

