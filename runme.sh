#!/bin/bash
if [ $# -ne 3 ]; then
    echo usage: runme.sh verilog_module_name test_sequences vectors_per_sequence
    exit 1
fi

module_name=$1
num_seq=$2
num_vecs=$3

cp iscas85_verilog/$module_name.v src/$module_name.v
python scripts/generate_test_vectors.py iscas85_verilog/$module_name.v $num_seq $num_vecs input_test_vectors
python scripts/testbench_generator.py iscas85_verilog/$module_name.v input_test_vectors/input_test_vectors $num_vecs src/${module_name}_tb.v
python scripts/makefile_generator.py $module_name build-rvt/MakePowerEstimation
cd build-rvt/vcs-sim-rtl/
make clean
make
make run
