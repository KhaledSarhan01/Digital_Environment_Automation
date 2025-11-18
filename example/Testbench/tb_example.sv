////////////////////////////////////////////////
///// Project   : Example             
///// Created on: 2025-11-17                   
////////////////////////////////////////////////

module tb_Example ;
//////////////////////////////////////
////////////// Signals //////////////
////////////////////////////////////
    logic clk,rst_n;
    logic [31:0]  i_header_bus;
 	logic  i_header_valid;
 	logic [31:0]  i_data_bus;
 	logic  i_data_valid;
 	logic [31:0]  i_header_bus;
 	logic [31:0]  o_code_bus;
 	logic  o_code_valid;
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
    Example DUT (.*);

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
        $stop;
    endtask
// Watch dog works after 10 ms in simulation time 
    initial begin
        #1000000;
        $display("Simulation is not working");
        $stop; 
    end  

//////////////////////////////////////
//////// Testbench Scenarios ////////
////////////////////////////////////
    task Initialization;
        // Initialize your Signals Here
         i_header_bus = 'h0;
 	 	 i_header_valid = 'h0;
 	 	 i_data_bus = 'h0;
 	 	 i_data_valid = 'h0;
 	 	 i_header_bus = 'h0;
    endtask
    task Main_Scenario();
        // Write your Test Scenario Here
    endtask
endmodule
