`timescale 1 ns /  100 ps

module decoder_tb();

reg [3:0] A;
wire [15:0] Z;


decoder DUT0 (.A(A), .Z(Z));

initial begin
  A <= 4'd0;
  #1 A<= 4'd1;
  #1 A<= 4'd2;
  #1 A<= 4'd3;
  #1 A<= 4'd4;
  #1 A<= 4'd5;
  #1 A<= 4'd6;
  #1 A<= 4'd7;
  #1 A<= 4'd9;
  #1 A<= 4'd9;
  #1 A<= 4'd10;
  #1 A<= 4'd11;
  #1 A<= 4'd12;
  #1 A<= 4'd13;
  #1 A<= 4'd14;
  #1 A<= 4'd15;

end

initial begin
  $monitor($time,": A=%b, Z=%b", A, Z);
end


endmodule
