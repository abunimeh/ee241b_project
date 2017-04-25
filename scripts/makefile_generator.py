"""
This script should write the /build-rvt/MakePowerEstimation file whose arguments
are used in the toolchain to select the RTL sources to build.

Calling Convention: python makefile_generator.py <circuit to test> <output makefrag path and filename>

Arguments:
    <circuit to test> = the name of the Verilog source file in src/ (without the .v extension)
    <output makefrag path and filename> = a relative or absolute path to where the Makefrag should be written to
"""
import sys
import shutil
import os

verilog_file_name = sys.argv[1]
output_makefrag_path = sys.argv[2]

with open(output_makefrag_path, "w") as makefrag_file:
    makefrag_file.write("vcs_rtl_vsrcs = \\\n")
    makefrag_file.write("   $(srcdir)/%s.v \\\n" % (verilog_file_name))
    makefrag_file.write("   $(srcdir)/%s_tb.v \\\n" % (verilog_file_name))

    makefrag_file.write("\n")

    makefrag_file.write("vcs_syn_toplevel = %s\n" % (verilog_file_name))
    makefrag_file.write("vcs_syn_vsrcs = \\\n")
    makefrag_file.write("   $(srcdir)/%s_tb.v \\\n" % (verilog_file_name))
    makefrag_file.write("   ../dc-syn/current-dc/results/$(toplevel).mapped.v \\\n")

    makefrag_file.write("\n")

    makefrag_file.write("dc_syn_toplevel = %s\n" % (verilog_file_name))
    makefrag_file.write("dc_syn_testharness = %s_tb\n" % (verilog_file_name))
    makefrag_file.write("dc_syn_toplevelinst = %s_inst\n" % (verilog_file_name))
    makefrag_file.write("dc_syn_vsrcs = \\\n")
    makefrag_file.write("   $(srcdir)/%s.v \\\n" % (verilog_file_name))
    #makefrag_file.write("   $(srcdir)/%s_tb.v \\\n" % (verilog_file_name))

    makefrag_file.write("\n")

    makefrag_file.write("icc_par_toplevel = %s\n" % (verilog_file_name))
    makefrag_file.write("icc_par_testharness = %s_tb\n" % (verilog_file_name))
    makefrag_file.write("icc_par_toplevelinst = %s_inst\n" % (verilog_file_name))

    makefrag_file.write("\n")

    makefrag_file.write("vcs_par_toplevel = %s\n" % (verilog_file_name))
    makefrag_file.write("vcs_par_vsrcs = \\\n")
    makefrag_file.write("   $(srcdir)/%s_tb.v \\\n" % (verilog_file_name))
    makefrag_file.write("   ../icc-par/current-icc/results/$(toplevel).output.v \\\n")

    makefrag_file.write("\n")

    makefrag_file.write("pt_toplevel = %s\n" % (verilog_file_name))
    makefrag_file.write("pt_testharness = %s_tb\n" % (verilog_file_name))
    makefrag_file.write("pt_toplevelinst = %s_inst\n" % (verilog_file_name))
