from cocotb_test.simulator import run
from cocotb.binary import BinaryValue
import pytest
import os

vhdl_compile_args = "--std=08"
sim_args = "--wave=wave.ghw"


tests_dir = os.path.abspath(os.path.dirname(__file__)) #gives the path to the test(current) directory in which this test.py file is placed
rtl_dir = tests_dir                                    #path to hdl folder where .vhdd files are placed


#run tests with generic values 
@pytest.mark.parametrize("g_sys_clk", [str(i) for i in [20*10**6,40*10**6]])
@pytest.mark.parametrize("g_pwm", [str(i) for i in [10*10**3,30*10**3]])
@pytest.mark.parametrize("g_bits_resolution", [str(i) for i in range(2,5,1)])
def test_pwm(g_sys_clk,g_pwm,g_bits_resolution):

    module = "testbench_pwm"
    toplevel = "pwm"   
    vhdl_sources = [
        os.path.join(rtl_dir, "../rtl/pwm.vhd"),
        ]

    parameter = {}
    parameter['g_sys_clk'] = g_sys_clk
    parameter['g_pwm'] = g_pwm
    parameter['g_bits_resolution'] = g_bits_resolution

    run(
        python_search=[tests_dir],                         #where to search for all the python test files
        vhdl_sources=vhdl_sources,
        toplevel=toplevel,
        module=module,

        vhdl_compile_args=[vhdl_compile_args],
        toplevel_lang="vhdl",
        parameters=parameter,                              #parameter dictionary
        extra_env=parameter,
        sim_build="sim_build/"
        + "_".join(("{}={}".format(*i) for i in parameter.items())),
    )
