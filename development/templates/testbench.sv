$header
module $tb_name ;
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
    $module_name DUT (.*);

//////////////////////////////////////
////////// Testbench Core ///////////
////////////////////////////////////
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

    initial begin
        #1000000;
        $$display("Simulation is not working");
        $$stop;
    end

//////////////////////////////////////
//////// Testbench Scenarios ////////
////////////////////////////////////
    task Initialization;
        $init_list
    endtask
    task Main_Scenario();
    endtask
endmodule
