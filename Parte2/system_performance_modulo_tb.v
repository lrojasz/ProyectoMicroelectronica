//============================================================
//========================Testbench===========================
//============================================================

module testbench (
    input               terminado,
    output reg          clk,
    output reg          reset,
    output reg          start_signal,
    output reg          valid,
    output reg  [7:0]   target,
    output reg  [95:0]  block_in
);

wire        terminado;

system system_dut (
//Inputs 
    .clk        (clk),
    .reset      (reset),
    .target     (target),
    .block      (block_in),
    .start      (start_signal),
//Outputs  
    .terminado  (terminado),
    .state      (),
    .nonce      ()       //4 bytes = 32 bits
);

//wire hash_ready_w;

initial begin
    $dumpfile("simulation.vcd");
    $dumpvars(0); 
    clk       <= 0;
    reset     <= 1;
    target    <= 10;
    start_signal <= 0;

    valid     <= 0;

    block_in[7:0]   <= 'h61;
    block_in[15:8]  <= 'h69;
    block_in[23:16] <= 'h63;
    block_in[31:24] <= 'h70;

    block_in[39:32] <= 'h21;
    block_in[47:40] <= 'h00;
    block_in[55:48] <= 'h00;
    block_in[63:56] <= 'h03;
    
    block_in[71:64] <= 'h17;
    block_in[79:72] <= 'h08;
    block_in[87:80] <= 'h00;
    block_in[95:88] <= 'hf3;

    #20 reset <= 0;
    #20 valid <= 1;
    start_signal <= 1;
//--------------------------Inicio de la simulacion    
    //#20 ini
end

always @(posedge clk)begin
    if(terminado) $finish;
end

always #5 clk = !clk;  
endmodule