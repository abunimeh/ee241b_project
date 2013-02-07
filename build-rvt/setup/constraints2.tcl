# This constraint sets the target clock period for the chip in
# nanoseconds. Note that the first parameter is the name of the clock
# signal in your verlog design. If you called it something different than
# clk you will need to change this. You should set this constraint
# carefully. If the period is unrealistically small then the tools will
# spend forever trying to meet timing and ultimately fail. If the period
# is too large the tools will have no trouble but you will get a very
# conservative implementation.

create_clock Clock_In -name ideal_clock1 -period 1
set_load -pin_load 0.028 [all_outputs]

set_input_delay -clock ideal_clock1  0 [all_inputs]
#set_output_delay -clock ideal_clock1  1.3 [all_outputs]
set_output_delay -clock ideal_clock1  .85 [get_ports predecode_top_onehot]
set_output_delay -clock ideal_clock1  .85 [get_ports predecode_bottom_onehot]






#myway
#create_clock -period  -name my_clock [get_ports Clock_In]
#set_input_delay 660ps -max -clock my_clock [all_inputs]
#set_output_delay 660ps -max -clock my_clock [all_outputs]

#connnecting inputs to inverters and outputs to flipflops

#set_driving_cell -library saed90nm_typ -lib_cell INVX0 [all_inputs]  
#set_load [load_of saed90nm_typ/DFFX1/D] [all_outputs]

#end of my way


#create_clock clk -name ideal_clock1 -period ${CLOCK_PERIOD}

# This constrainst sets the load capacitance in picofarads of the
# output pins of your design. 4fF is reasonable if your design is
# driving another block of on-chip logic.

#set_load -pin_load 0.004 [all_outputs]

# This constraint sets the input drive strength of the input pins of
# your design. We specifiy a specific standard cell which models what
# would be driving the inputs. INVX1 is a small inverter and is
# reasonable if another block of on-chip logic is driving your inputs.


#/

