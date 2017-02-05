`timescale 1 ns /  100 ps

module decoder_tb();

reg [2:0] A;
wire [7:0] Z;
reg clk;

// Fake clock does nothing
decoder DUT0 (.A(A), .Z(Z), .clk(clk));

initial begin

$vcdpluson;
  A <= 3'd0;
 #`CLOCK_PERIOD A<= 3'd1;
 #`CLOCK_PERIOD A<= 3'd2;
 #`CLOCK_PERIOD A<= 3'd3;
 #`CLOCK_PERIOD A<= 3'd4;
 #`CLOCK_PERIOD A<= 3'd5;
 #`CLOCK_PERIOD A<= 3'd6;
 #`CLOCK_PERIOD A<= 3'd7;
$vcdplusoff;

end

initial begin
  $monitor($time,": A=%b, Z=%b", A, Z);
end


endmodule
