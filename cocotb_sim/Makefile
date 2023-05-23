# Makefile

# defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl
EXTRA_ARGS += --std=08
SIM_ARGS += --wave=wave.ghw

VHDL_SOURCES += $(PWD)/../rtl/pulse_stretcher.vhd
VHDL_SOURCES += $(PWD)/../rtl/one_shot.vhd
VHDL_SOURCES += $(PWD)/../rtl/debounce.vhd
VHDL_SOURCES += $(PWD)/../rtl/pwm.vhd
VHDL_SOURCES += $(PWD)/../rtl/watchdog_timer.vhd

# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
# MODULE is the basename of the Python test file

test:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_stretcher TOPLEVEL=pulse_stretcher

test_debounce:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_debounce TOPLEVEL=debounce

test_one_shot:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_one_shot TOPLEVEL=one_shot

test_pwm:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_pwm TOPLEVEL=pwm

test_watchdog:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_watchdog TOPLEVEL=watchdog_timer

clean_dir:
		rm -f wave.*
		rm -f *.o 
		rm -f *.xml
		find . -maxdepth 1 -type f -executable -exec rm {} +
		find -mindepth 1 -maxdepth 1 -type d -print0 | xargs -r0 rm -R
# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim