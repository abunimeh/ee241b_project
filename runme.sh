#!/bin/bash
if [ $# -ne 1 ]; then
    echo usage: runme.sh verilog_module_name
    exit 1
fi

cp iscas85_verilog/$1.v src/$1.v
python scripts/generate_test_vectors.py iscas85_verilog/$1.v 10 10 input_test_vectors
python scripts/testbench_generator.py iscas85_verilog/$1.v input_test_vectors/input_test_vectors 10 src/$1_tb.v
python scripts/makefile_generator.py $1 build-rvt/MakePowerEstimation
cd build-rvt/vcs-sim-rtl/
make clean
make
make run
