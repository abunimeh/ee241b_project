`timescale 1 ns /  1 ps

module decoder_tb();

  reg [4:0] A = 0;
  wire [31:0] Z;
  reg clk = 0;
  integer cycle = 0;
  integer i;

  always #(`CLOCK_PERIOD * 0.5)  clk = ~clk;
  
  //decoder DUT0 (.A(A), .Z(Z), .clk(clk));
/*
  initial begin
    // Note: feeds in @ falling edge to allow for some 
    // gate propagation time
    $vcdpluson;
    #`CLOCK_PERIOD;
    for (i=0; i<32; i=i+1) begin
      A <= i;
      #`CLOCK_PERIOD;
      cycle = cycle + 1;
      `expect("Z", Z, 1 << i, cycle)
    end
    $vcdplusoff;
    $display("\t **Ran through all test vectors**"); $finish;

  end

  initial begin
    $monitor($time,": A=%d, Z=%b, cycle=%d", A, Z, cycle);
  end
*/
endmodule
