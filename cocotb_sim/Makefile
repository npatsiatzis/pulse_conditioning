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

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim