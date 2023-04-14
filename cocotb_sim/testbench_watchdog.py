import cocotb
from cocotb.clock import Clock
from cocotb.utils import get_sim_time
from cocotb.triggers import Timer,RisingEdge,FallingEdge,ClockCycles,Combine,Join
import random
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db

g_watchdog_size = int(cocotb.top.g_watchdog_size)

#Callback functions to capture the bin content showing
full = False
def notify():
	global full
	full = True

covered_values = []

# at_least = value is superfluous, just shows how you can determine the amount of times that
# a bin must be hit to considered covered
@CoverPoint("top.watchdog_cycles",xf = lambda x : x, bins = list(range(2,2**g_watchdog_size)), at_least=1)
def number_cover(x):
	covered_values.append(x)




async def reset(dut,cycles=1):
	dut.i_rst.value = 1
	dut.i_dv.value = 0
	dut.i_restart.value = 0
	dut.i_time.value = 0
	await RisingEdge(dut.i_clk)
	await ClockCycles(dut.i_clk,cycles)
	dut.i_rst.value = 0
	await RisingEdge(dut.i_clk)
	dut._log.info("the core was reset")



@cocotb.test()
async def test(dut):
	

	cocotb.start_soon(Clock(dut.i_clk, 10, units="ns").start())
	await reset(dut,5)

	while full != True:
		
		dut.i_dv.value = 1
		cycles = random.randint(2,2**g_watchdog_size-1)

		while cycles in covered_values:
			cycles = random.randint(2,2**g_watchdog_size-1)		 
		
		dut.i_time.value = cycles
		await RisingEdge(dut.i_clk)
		dut.i_dv.value = 0
		await RisingEdge(dut.i_clk)

		await ClockCycles(dut.i_clk,cycles)
		await FallingEdge(dut.i_clk)
		assert not (1 != dut.o_timeout.value),"Wrong Behavior"

		number_cover(cycles)
		coverage_db["top.watchdog_cycles"].add_threshold_callback(notify, 100)

		dut.i_rst.value = 1
		await RisingEdge(dut.i_clk)
		dut.i_rst.value = 0

	coverage_db.report_coverage(cocotb.log.info,bins=True)
	coverage_db.export_to_xml(filename="coverage.xml") 