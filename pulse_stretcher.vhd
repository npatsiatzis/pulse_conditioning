--A programmable pulse stretcher 

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pulse_stretcher is
	generic(
		g_stretch_width : natural :=4);
	port(
		i_clk : in std_ulogic;
		i_rst : in std_ulogic;
		i_d	  : in std_ulogic;
		i_stretch_amt : in std_ulogic_vector(g_stretch_width -1 downto 0);
		o_q	  : out std_ulogic);
end pulse_stretcher;

architecture arch of pulse_stretcher is
begin
	pulse_stretch : process(i_clk)
		variable cnt : integer range 0 to 2**g_stretch_width-1;
	begin
		if(rising_edge(i_clk)) then
			if(i_rst = '1') then
				cnt := 0;
				o_q <= '0';
			else
				if(i_stretch_amt = std_ulogic_vector(to_unsigned(0,g_stretch_width))) then
					o_q <= i_d;
				else
					if(i_d = '1') then
						cnt := to_integer(unsigned(i_stretch_amt));
					end if;
					if(cnt > 0) then
						cnt := cnt -1;
						o_q <= '1';
					else
						o_q <= '0';
					end if;
				end if;
			end if;
		end if;
	end process; -- pulse_stretch
end arch;