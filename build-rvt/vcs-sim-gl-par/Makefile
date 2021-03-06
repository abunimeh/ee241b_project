#=======================================================================
# UCB VLSI Makefile for vcs-sim-gl-par
#-----------------------------------------------------------------------
# Yunsup Lee (yunsup@cs.berkeley.edu)
#
# This makefile will build a rtl simulator and run various tests to
# verify proper functionality.
#

include ../Makefrag
include ../MakePowerEstimation
default : all

basedir  = ../..

#--------------------------------------------------------------------
# Sources
#--------------------------------------------------------------------

# Library components

vclibdir = $(UCB_VLSI_HOME)/install/vclib
vclibsrcs = \
	$(vclibdir)/vcQueues.v \
	$(vclibdir)/vcStateElements.v \
	$(vclibdir)/vcTest.v \
	$(vclibdir)/vcTestSource.v \
	$(vclibdir)/vcTestSink.v \

# Specify what the toplevel verilog module is
toplevel = $(vcs_par_toplevel)
#toplevel = decoder

# Verilog sources

srcdir = $(basedir)/src
vsrcs = $(vcs_par_vsrcs)
#vsrcs = \
#	$(srcdir)/decoder_tb.v \
#	../icc-par/current-icc/results/$(toplevel).output.v \

#--------------------------------------------------------------------
# Build rules
#--------------------------------------------------------------------

verilog_cells_dir = $(UCB_VLSI_HOME)/stdcells/$(UCB_STDCELLS)/verilog

VCS      = vcs -full64
VCS_OPTS = -notice -PP -line +lint=all,noVCDE,noTFIPC,noIWU,noOUDPE +v2k -timescale=1ns/1ps \
	-P ../icc-par/current-icc/access.tab -debug \
	+neg_tchk +sdfverbose \
	-sdf typ:$(toplevel):../icc-par/current-icc/results/$(toplevel).output.sdf \


#--------------------------------------------------------------------
# Build the simulator
#--------------------------------------------------------------------

vcs_sim = simv
$(vcs_sim) : Makefile $(vsrcs) $(vclibsrcs)
	$(VCS) $(VCS_OPTS) +incdir+$(srcdir) -o $(vcs_sim) \
	       +define+CLOCK_PERIOD=$(vcs_clock_period) \
	       +incdir+$(vclibdir) $(addprefix -v ,$(vclibsrcs)) \
               -v $(verilog_cells_dir)/cells_rvt.v \
               -v $(verilog_cells_dir)/cells_hvt.v \
               -v $(verilog_cells_dir)/cells_lvt.v \
				$(vsrcs) 
#--------------------------------------------------------------------
# Run
#--------------------------------------------------------------------

vpd = vcdplus.vpd
$(vpd): $(vcs_sim)
	./simv -ucli -do run.tcl +verbose=1
	date > timestamp

run: $(vpd)

#--------------------------------------------------------------------
# Convert
#--------------------------------------------------------------------

convert_saif = vcdplus.saif

$(convert_saif): %.saif: %.vpd
	vpd2vcd $(patsubst %.saif,%.vpd,$@) $(patsubst %.saif, %.vcd, $@)
	/home/ff/ee241/tools/icc/bin/vcd2saif -input $(patsubst %.saif, %.vcd, $@) -output $@
	date > timestamp

convert: $(convert_saif)

#--------------------------------------------------------------------
# Default make target
#--------------------------------------------------------------------

.PHONY: run convert

all : $(vcs_sim)

#--------------------------------------------------------------------
# Clean up
#--------------------------------------------------------------------

junk += simv* csrc *.vpd *.vcd *.saif *.key DVE* .vcs* sdf* timestamp

clean :
	rm -rf $(junk) *~ \#* *.log *.cmd *.daidir
