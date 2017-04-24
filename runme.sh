python scripts/generate_test_vectors.py iscas85_verilog/c17.v 10 10 input_test_vectors
python scripts/testbench_generator.py iscas85_verilog/c17.v input_test_vectors/input_test_vectors 10 src/c17_tb.v
