////////////////////////////////////////////////
///// Project   : Example             
///// Created on: 2025-11-17                   
////////////////////////////////////////////////

module Example (
// Clock and active low Asynchronous Reset
    input logic clk,rst_n 
// Signals    
    ,input  logic [31:0]  i_header_bus
 	,input  logic  i_header_valid
 	,input  logic [31:0]  i_data_bus
 	,input  logic  i_data_valid
 	,input  logic [31:0]  i_header_bus
 	,output logic [31:0]  o_code_bus
 	,output logic  o_code_valid
);
// Enter your code here
// THIS IS DUMMY CODE
    assign o_code_bus = 'h0;
 	assign o_code_valid = 'h0;
endmodule
