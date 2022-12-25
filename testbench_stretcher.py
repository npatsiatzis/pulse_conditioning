import cocotb
from cocotb.clock import Clock
from cocotb.utils import get_sim_time
from cocotb.triggers import RisingEdge,FallingEdge,ClockCycles
import random
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db


covered_number = []
g_stretch_width = int(cocotb.top.g_stretch_width)


# #Callback functions to capture the bin content showing
full = False
def notify():
	global full
	full = True

# at_least = value is superfluous, just shows how you can determine the amount of times that
# a bin must be hit to considered covered
@CoverPoint("top.data",xf = lambda x : x.i_stretch_amt.value, bins = list(range(2**g_stretch_width)), at_least=1)
def number_cover(dut):
	covered_number.append(dut.i_stretch_amt.value)

async def reset(dut,cycles=1):
	dut.i_rst.value = 1

	dut.i_d.value = 0
	dut.i_stretch_amt.value = 0

	await ClockCycles(dut.i_clk,cycles)
	await FallingEdge(dut.i_clk)

	dut.i_rst.value = 0
	await RisingEdge(dut.i_clk)
	dut._log.info("the core was reset")



@cocotb.test()
async def test(dut):
	cocotb.start_soon(Clock(dut.i_clk, 10, units="ns").start())
	await reset(dut,5)


	#cover the input space
	while(full != True):
		stretch_amt = random.randint(0,2**g_stretch_width-1)
		while(stretch_amt in covered_number):
			stretch_amt = random.randint(0,2**g_stretch_width-1)
		dut.i_stretch_amt.value = stretch_amt 
		dut.i_d.value = 1

		await RisingEdge(dut.i_clk)
		dut.i_d.value = 0
		await RisingEdge(dut.o_q)
		start_time = get_sim_time()
		await FallingEdge(dut.o_q)
		end_time = get_sim_time()
		assert not ((end_time-start_time)<stretch_amt*10),"Wrong Behavior!"
		coverage_db["top.data"].add_threshold_callback(notify, 100)
		number_cover(dut)

