module decoder(
  input [4:0] A,
  output reg [31:0] Z,
  input clk
);

// NOTE: Testbench expects that the output Z is registered!

// Only one output should ever be high.  For example,
// Z[2] = !A[4] & !A[3] & !A[2] & A[1] & !A[0] of the previous clk cycle, etc
// When Z[2] is high, Z[0], Z[1], Z[3] to Z[31] should all be low

// Hint: a 2 to 1 mux looks like:
// assign y = (sel) ? b : a;
// Where y = b when sel is high; otherwise y = a
// And you can replace "a" with a further condition
// assign y = (sel1) ? c
//          : (sel2) ? b
//          : a ;
// and sel1 can be a condition like:
// A == 5'd0
// OR: Since a 5 to 32 decoder using this approach requires a lot of copy + pasting,
// I challenge you to come up with a shorter way to write the same thing ;)

endmodule





