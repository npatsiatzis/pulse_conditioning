import cocotb
from cocotb.clock import Clock
from cocotb.utils import get_sim_time
from cocotb.triggers import Timer,RisingEdge,FallingEdge,ClockCycles,Combine,Join
import random
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db


covered_number = []
one_shot_pulse_period = 0
pulse_mult = 5
clk_period = 5

# #Callback functions to capture the bin content showing
full = False
def notify():
	global full
	full = True

# at_least = value is superfluous, just shows how you can determine the amount of times that
# a bin must be hit to considered covered
@CoverPoint("top.pulse_len",xf = lambda x : x, bins = list(range(2**pulse_mult)), at_least=1)
def number_cover(x):
	covered_number.append(x)

async def reset(dut,cycles=1):
	dut.i_rst.value = 1

	dut.i_s.value = 0

	await ClockCycles(dut.i_clk,cycles)
	await FallingEdge(dut.i_clk)

	dut.i_rst.value = 0
	await RisingEdge(dut.i_clk)
	dut._log.info("the core was reset")


async def measure_pulse(dut):
	global one_shot_pulse_period
	one_shot_pulse_period 
	await RisingEdge(dut.o_s)
	start_time = get_sim_time('ns')
	await FallingEdge(dut.o_s)
	end_time = get_sim_time('ns')
	one_shot_pulse_period = end_time - start_time

@cocotb.test()
async def test(dut):
	cocotb.start_soon(Clock(dut.i_clk, clk_period, units="ns").start())
	await reset(dut,5)

	#cover the input space
	while(full != True):
		pulse_len = random.randint(0,2**pulse_mult-1)
		while(pulse_len in covered_number):
			pulse_len = random.randint(0,2**pulse_mult-1)

		
		dut.i_s.value = 1
		await Combine(Join(cocotb.start_soon(measure_pulse(dut))),Timer(clk_period*pulse_len,'ns'))
		dut.i_s.value = 0 
		await Timer(clk_period*pulse_len,'ns')


		await RisingEdge(dut.i_clk)
		assert not (one_shot_pulse_period != clk_period),"Wrong Behavior!"
		number_cover(pulse_len)
		coverage_db["top.pulse_len"].add_threshold_callback(notify, 100)


	coverage_db.report_coverage(cocotb.log.info,bins=True)
	coverage_db.export_to_xml(filename="coverage_one_shot.xml") 
		

