`timescale 1ns / 1ps

module micro_ucr_hash (
    input           clk,
    input           reset,
    input           hash_init,

    input           valid,
    input [127:0]   block_in,       //Bus de 127 bits
    output reg [23:0] hash,         //Senial para indicar que se ha terminado un hash (es valido)    
    output reg [6:0] state,         //Senial para indicar que se ha terminado un hash (es valido)    
    output reg      hash_ready     //Senial para indicar que se ha terminado un hash (es valido)    
    //output reg      ready           //Senial multiuso para indicar que se ha terminado una transaccion 
    //output reg      terminado
);
//---------------------Parametros de tamanio-----------------------
    parameter W_bits = 32*8;      //32 variables de 8 bits
    parameter Block_bits = 16*8;  //16 variables de 8 bits
//-----------------------------------------------------------------
//-------------------------Estados---------------------------------
//Codificacion de estados en one-hot    
    parameter IDDLE      = 1;
    parameter LOAD_BCK   = 2;
    parameter GET_W      = 4;
    parameter ITERATE    = 8;
    parameter OUTPUT     = 16;
    parameter UPDATE_ABC = 32;

    reg [23:0]              H;           //Resultado del Hash
    reg [W_bits-1:0]        W;           //Definida la W_bits cantidad de bits para todas las w variables
    reg [Block_bits-1:0]    block;       //Espacio de memoria donde se guarda el bloque de entrada para el Hash
    reg [8:0]               counter;     //Variable multiuso para contar, especialmente en ciclos
    reg                     block_ready; //%%FLAG%% para empezar a trabajar cuando se tiene todos los bloques
    reg [7:0]               a,b,c,c2,k,eggs;//Un byte por cada variable          

always @(posedge clk)begin
    if (reset) begin
        W <= 0;
        H <= 0;
        block <= 0;
        //terminado   <= 0;
        counter     <= 0;
        hash        <= 0;
        hash_ready  <= 0;
        block_ready <= 0;    //%%FLAG%%
        a <= 'h01;
        b <= 'h89;
        c <= 'hfe;
        c2 <= 'hfe;
        k <= 0;
        eggs <= 0;
        state <= IDDLE;
    end
    else begin
        case (state)
            IDDLE: begin
                if (hash_init) begin
                    state <= LOAD_BCK;                    
                end
                else begin
                    hash_ready <= 0;
                    state <= IDDLE;
                    block_ready <= 0;
                end
            end

            LOAD_BCK: begin
                if (~block_ready)begin //Capta las variables del bloque (optimizado en area)
                    if (valid) begin                //Si los datos transmitidos son validos, guardelos
                        block <= block_in;          //Guarda el bloque completo obtenido
                        block_ready <= 1;
                        counter <= 0;
                        state <= GET_W;
                    end
                    else state <= LOAD_BCK;         //Recordemos que sin este else, sale un latch inferido
                end
                else state <= LOAD_BCK;
            end

            GET_W: begin
                if (counter<16) begin
                    W[counter*8 +: 8] <= block[counter*8 +: 8];     
                    counter <= counter + 1;
                    state <= GET_W;
                end
                else if (counter<32)begin
                    W[counter*8 +: 8] <= W[((counter-3)*8) +: 8] | W[((counter-9)*8) +: 8]^W[((counter-14)*8) +: 8];
                    counter <= counter + 1;
                    state <= GET_W;
                end
                else begin //Setup incluido
                    a <= 'h01;
                    b <= 'h89;
                    c <= 'hfe;

                    H[23:16] <= 'h01;
                    H[15:8]  <= 'h89;
                    H[7:0]   <= 'hfe;

                    counter <= 0;
                    state <= ITERATE;
                end 
            end
            
            ITERATE: begin
                if(counter != 32)begin
                    if(counter < 17)begin
                        k    <= 'h99;
                        eggs <= a^b;
                        //counter <= counter + 1;
                    end
                    else if (counter<32)begin
                        k    <= 'ha1;
                        eggs <= a|b;
                        //counter <= counter + 1;
                    end
                    state <= UPDATE_ABC;                    
                end
                else begin
                    H[23:16] <= H[23:16] + a;
                    H[15:8]  <= H[15:8] + b;
                    H[7:0]   <= H[7:0] + c;

                    counter <= 0;
                    state <= OUTPUT;
                end 
            end

            UPDATE_ABC: begin
                a <= b^c;
                b <= c<<4;
                c <= eggs + k + W[counter*8 +: 8];
                counter <= counter + 1;
                state <= ITERATE;
            end

            OUTPUT : begin
                hash <= H[23:0];
                hash_ready <= 1;
                //terminado <= 1;
                state <= IDDLE;
            end

            default: state <= IDDLE;            
        endcase
    end
end
endmodule   
