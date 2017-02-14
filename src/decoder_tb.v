`timescale 1 ns /  1 ps

`define expect(nodeName, nodeVal, expVal, cycle) if (nodeVal !== expVal) begin \
  $display("\t ASSERTION ON %s FAILED @ CYCLE = %d, 0x%h != EXPECTED 0x%h", \
  nodeName,cycle,nodeVal,expVal); $stop; end

module decoder_tb();

  reg [4:0] A = 0;
  wire [31:0] Z;
  reg clk = 0;
  integer cycle = 0;
  integer i;

  always #(`CLOCK_PERIOD * 0.5)  clk = ~clk;
  always @(posedge clk) cycle = cycle + 1;
  
  decoder decoder_inst (.A(A), .Z(Z), .clk(clk));

  initial begin
    $vcdpluson;
    // Extra cycles to flush out any initial X's
    repeat(4) @(posedge clk);	
    for (i=1; i<=32; i=i+1) begin
      // Input + output events on clock rising edge
      @(posedge clk);
      #0.001;
      A = i;
      @(negedge clk);
      `expect("Z", Z, 1 << (i-1), cycle)
    end
    $vcdplusoff;
    $display("\t **Ran through all test vectors**"); $finish;

  end

  initial begin
    $monitor($time,": A=%d, Z=%b, cycle=%d", A, Z, cycle);
  end

endmodule
