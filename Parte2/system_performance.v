`timescale 1ns / 1ps
`include "micro_ucr_hash.v"

//============================================================
//======================== System  ===========================
//============================================================

module system (
    input               clk,
    input               reset,
    input      [7:0]    target,
    input      [95:0]   block,
    input               start,
    output reg          terminado,
    output reg [7:0]    state,
    output reg [31:0]   nonce       //4 bytes = 32 bits
);

parameter IDDLE      = 1;
parameter FINDNONCE  = 2;
parameter ITERATE    = 4;
parameter NEXT_NONCE = 8;
parameter HSH_DELAY = 16;
parameter SETUP     = 32;

reg [127:0] hash_input;
reg [7:0]   target_r, counter;
reg [31:0]  nonce_r;
reg [95:0]  bytes;
reg         valid_nonce, hash_init, valid, nonce_update;

wire [23:0] hash_w;
wire        hash_ready_w;

// segundo micro_ucr_hash
reg [31:0]  nonce_l;
reg [127:0] hash_input_l;
wire [23:0] hash_l;
wire        hash_ready_l;


micro_ucr_hash hash1(
//Inputs    
    .clk        (clk),
    .reset      (reset),
    .hash_init  (hash_init),
    .valid      (valid),
    .block_in   (hash_input),  //Bus de 127 bits
//Outputs    
    .hash       (hash_w),  //Senial para indicar que se ha terminado un hash (es valido)    
    .hash_ready (hash_ready_w)  //Senial para indicar que se ha terminado un hash (es valido)    
    //.ready      (),  //Senial multiuso para indicar que se ha terminado una transaccion 
    //.terminado  (terminado)
);

micro_ucr_hash hash2(
//Inputs    
    .clk        (clk),
    .reset      (reset),
    .hash_init  (hash_init),
    .valid      (valid),
    .block_in   (hash_input_l),  //Bus de 127 bits
//Outputs    
    .hash       (hash_l),  //Senial para indicar que se ha terminado un hash (es valido)    
    .hash_ready (hash_ready_l)  //Senial para indicar que se ha terminado un hash (es valido)    
    //.ready      (),  //Senial multiuso para indicar que se ha terminado una transaccion 
    //.terminado  (terminado)
);


always @(posedge clk) begin
    if (reset) begin
        counter <= 0;
        terminado <= 0;
        nonce     <= 0;
        bytes     <= 0;
        target_r  <= 0;
        nonce_r   <= 0;
        nonce_l   <= 0;
        state     <= IDDLE;
        hash_input <= 0;
        hash_init  <= 0;
        valid_nonce <= 0;
        valid       <= 0;
        nonce_update <= 0;

    end
    else begin
        case (state)
            IDDLE : begin                       //A la espera de la actualizacion del target y/o start signal
//--------Segmento Setup-------------------------------
                target_r <= target;             //Actualiza el target (solo aqui puede)
                bytes     <= block;
                terminado <= 0;
                hash_init  <= 0;
                counter <= 0;
                nonce_r <= {8'h0, 8'h0, 8'h0, 8'h0};
                nonce_l <= {8'h1, 8'h0, 8'h0, 8'h0};
//-----------------------------------------------------                
                if (start) state <= FINDNONCE;
                else state <= IDDLE;
            end

            FINDNONCE : begin
                nonce_update <= 1;
                state <= HSH_DELAY;
                counter <= 3; //Borrar
            end
            
            ITERATE: begin
                if (~valid_nonce)begin
                    if ((hash_w[23:16]<=target_r)&&(hash_w[15:8]<=target_r))begin    
                        valid_nonce <= 1;
                        nonce <= {nonce_r[7:0], nonce_r[15:8], nonce_r[23:16], nonce_r[31:24]};
                        terminado <= 1;
                    end
                    else if ((hash_l[23:16]<=target_r)&&(hash_l[15:8]<=target_r))begin    
                        valid_nonce <= 1;
                        nonce <= {nonce_l[7:0], nonce_l[15:8], nonce_l[23:16], nonce_l[31:24]};
                        terminado <= 1;
                    end
                    else begin       //Caso donde se debe meter el siguiente nonce
                        counter <= 3;
                        state <= NEXT_NONCE;    
                    end
                end
            end

            NEXT_NONCE: begin
            
                if (counter != 0) begin
                    // para hash right
                    if (nonce_r[counter*8 +: 8] == 'hff)begin
                        nonce_r[counter*8 +: 8] <= nonce_r[counter*8 +: 8] & 'hff;            
                        nonce_r[(counter-1)*8 +: 8] <= nonce_r[(counter-1)*8 +: 8] + 2;            
                    end
                    else if (nonce_r[counter*8 +: 8] == 'hfe)begin
                        nonce_r[counter*8 +: 8] <= nonce_r[counter*8 +: 8] & 'hff;            
                        nonce_r[(counter-1)*8 +: 8] <= nonce_r[(counter-1)*8 +: 8] + 1;            
                    end
                    else begin
                        nonce_r <= nonce_r;
                    end

                    // para hash left
                    if (nonce_l[counter*8 +: 8] == 'hff)begin
                        nonce_l[counter*8 +: 8] <= nonce_l[counter*8 +: 8] & 'hff;            
                        nonce_l[(counter-1)*8 +: 8] <= nonce_l[(counter-1)*8 +: 8] + 2;            
                    end
                    else if (nonce_l[counter*8 +: 8] == 'hfe)begin
                        nonce_l[counter*8 +: 8] <= nonce_l[counter*8 +: 8] & 'hff;            
                        nonce_l[(counter-1)*8 +: 8] <= nonce_l[(counter-1)*8 +: 8] + 1;            
                    end
                    else begin
                        nonce_l <= nonce_l;
                    end

                    state <= NEXT_NONCE;
                    counter <= counter -1;
                end
                else begin
                    // para hash right
                    if ((nonce_r[counter*8 +: 8] == 'hff) && (counter==0))begin
                        nonce_r[counter*8 +: 8] <= nonce_r[counter*8 +: 8] & 'hff;                                  
                    end
                    else begin
                        nonce_r[31:24] <=  nonce_r[31:24] + 2;                                    
                    end

                    // para hash left
                    if ((nonce_l[counter*8 +: 8] == 'hff) && (counter==0))begin
                        nonce_l[counter*8 +: 8] <= nonce_l[counter*8 +: 8] & 'hff;                                   
                    end
                    else begin
                        nonce_l[31:24] <=  nonce_l[31:24] + 2;                                    
                    end

                    nonce_update <= 1; 
                    state <= HSH_DELAY;  
                end                                 
            end

            HSH_DELAY: begin                    //Espera hasta que se reciba todos los hash
                if (nonce_update)begin
                    valid      <= 1;
                    hash_input <= {nonce_r, bytes}; 
                    hash_input_l <= {nonce_l, bytes}; 
                    hash_init  <= 1;                //Activa a UCR HASH para obtener un hash;
                    nonce_update <= 0;
                    state <= HSH_DELAY;
                end
                else begin
                    hash_init  <= 0;
                    if (hash_ready_w && hash_ready_l) state <= ITERATE;
                    else state <= HSH_DELAY; 
                end                
            end


            default : state <= IDDLE;
        endcase
    end
end
endmodule

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