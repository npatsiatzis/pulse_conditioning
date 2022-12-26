import cocotb
from cocotb.clock import Clock
from cocotb.utils import get_sim_time
from cocotb.triggers import Timer,RisingEdge,FallingEdge,ClockCycles,Combine,Join
import random
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db

g_stable = int(cocotb.top.g_stable)
g_clk_freq = int(cocotb.top.g_clk_freq)
covered_number = [[] for _ in range(g_stable+1)]

#number of valid pulses to send in between of many other runt pulses
reps = 5	

actual_debounced_presses = 0

#Callback functions to capture the bin content showing
full = False
def notify():
	global full
	full = True

# at_least = value is superfluous, just shows how you can determine the amount of times that
# a bin must be hit to considered covered
@CoverPoint("top.data",xf = lambda x,y : x, bins = list(range(g_stable+1)), at_least=reps)
def number_cover(x,rep):
	covered_number[rep].append(x)

async def create_runt_pulses(dut,rep):
	for i in range(g_stable+1):
		pulse_len = random.randint(0,g_stable)
		while(pulse_len in covered_number[rep]):
			pulse_len = random.randint(0,g_stable)
		number_cover(pulse_len,rep)
		print(covered_number[rep])
		print(pulse_len)
		dut.i_btn.value = 1
		await Timer(pulse_len,'ms')
		dut.i_btn.value = 0 
		await Timer(pulse_len,'ms')


async def reset(dut,cycles=1):
	dut.i_rst.value = 1

	dut.i_btn.value = 0

	await ClockCycles(dut.i_clk,cycles)
	await FallingEdge(dut.i_clk)

	dut.i_rst.value = 0
	await RisingEdge(dut.i_clk)
	dut._log.info("the core was reset")


async def capture_debounced_press(dut):
	global actual_debounced_presses
	await RisingEdge(dut.o_btn)
	actual_debounced_presses  +=1
	await FallingEdge(dut.o_btn)

@cocotb.test()
async def test(dut):
	
	expected_debounced_presses = 0

	cocotb.start_soon(Clock(dut.i_clk, 1/g_clk_freq, units="sec").start())
	await reset(dut,5)

	for i in range(reps):
		print("rep is {}".format(i))
		expected_debounced_presses +=1
		await Combine(Join(cocotb.start_soon(capture_debounced_press(dut))),Join(cocotb.start_soon(create_runt_pulses(dut,i))))
		assert not (expected_debounced_presses != actual_debounced_presses),"Wrong Behavior"
