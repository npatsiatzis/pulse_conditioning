import cocotb
from cocotb.clock import Clock
from cocotb.utils import get_sim_time
from cocotb.triggers import RisingEdge,FallingEdge,ClockCycles
import random
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db
import numpy as np 


g_pwm = int(cocotb.top.g_pwm)
g_sys_clk = int(cocotb.top.g_sys_clk)
g_bits_resolution = int(cocotb.top.g_bits_resolution)

covered_value = []
covered_number = []

#Callback functions to capture the bin content showing
full_cycle = False
def notify_full_cyle():
	global full_cycle
	full_cycle = True

#Callback functions to capture the bin content showing
full = False
def notify():
	global full
	full = True

# at_least = value is superfluous, just shows how you can determine the amount of times that

@CoverPoint("top.duty_pwm_cycle",xf = lambda x: x.i_duty.value, bins = list(range(0,2**g_bits_resolution-1)), at_least=1)
def number_pwm_cycle_cover(x):
	covered_value.append(x.i_duty.value)

@CoverPoint("top.duty",xf = lambda x: x.i_duty.value, bins = list(range(0,2**g_bits_resolution-1)), at_least=1)
def number_cover(x):
	covered_number.append(x.i_duty.value)


async def reset(dut,cycles=1):
	dut.i_rst.value = 1

	dut.i_duty.value = 0

	await ClockCycles(dut.i_clk,cycles)
	await FallingEdge(dut.i_clk)

	dut.i_rst.value = 0
	await RisingEdge(dut.i_clk)
	dut._log.info("the core was reset")

#test that width of a pwm cycle is as it should be given the 
#user-defined pwm frequency and duty cycle
@cocotb.test()
async def test_pwm_cycle(dut):
	cocotb.start_soon(Clock(dut.i_clk, 1/g_sys_clk, units="sec").start())
	await reset(dut,5)

	while full_cycle != True:
		duty = random.randint(0,2**g_bits_resolution-2)
		while duty in covered_value:
			duty = random.randint(0,2**g_bits_resolution-2)
		dut.i_duty.value = duty

		await FallingEdge(dut.o_pwm)
		number_pwm_cycle_cover(dut)
		coverage_db["top.duty_pwm_cycle"].add_threshold_callback(notify_full_cyle, 100)

		await RisingEdge(dut.o_pwm)
		start_time = get_sim_time("sec")
		await RisingEdge(dut.o_pwm)
		end_time = get_sim_time("sec")
		#actual pwm cycle duration
		pwm_cycle = end_time-start_time

		#expected pwm cycle duration

		#check the actual against the expected pwm cycle duration
		expected_cycle = expected_high_cycle = (1/g_sys_clk) * np.ceil(g_sys_clk/(2**g_bits_resolution*g_pwm)) * (2**g_bits_resolution)
		assert not (round(pwm_cycle,3) != round(expected_cycle,3)),"Wrong Behavior!"
		

#test that the structure of a pwm cycle is as it should be given the 
#user-defined pwm frequency and duty cycle. Check the duration of 
#the high and low parts of the cycle.
@cocotb.test()
async def test(dut):

	cocotb.start_soon(Clock(dut.i_clk, 1/g_sys_clk, units="sec").start())
	await reset(dut,5)

	while full != True:
		duty = random.randint(0,2**g_bits_resolution-2)
		while duty in covered_number:
			duty = random.randint(0,2**g_bits_resolution-2)
		dut.i_duty.value = duty

		await RisingEdge(dut.o_pwm)
		number_cover(dut)
		coverage_db["top.duty"].add_threshold_callback(notify, 100)

		start_time = get_sim_time("sec")
		await FallingEdge(dut.o_pwm)
		end_time = get_sim_time("sec")
		#actual high cycle duration
		pwm_half_cycle = end_time-start_time

		#expected high cycle duration
		expected_high_cycle = (1/g_sys_clk) * np.ceil(g_sys_clk/(2**g_bits_resolution*g_pwm)) * (duty+1)
		#check the actual high cycles based on the generic pwm frequency and the generic duty cycle
		#against the expected values given these specs
		assert not (round(pwm_half_cycle,3) != round(expected_high_cycle,3)),"Wrong Behavior!"
