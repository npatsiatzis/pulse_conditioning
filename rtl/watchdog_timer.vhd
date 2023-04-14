--A programmable watchdog timer

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity watchdog_timer is 
	generic(
		g_watchdog_size : natural := 8);
	port(
		i_clk : in std_ulogic;
		i_rst : in std_ulogic;
		i_dv : in std_ulogic;
		i_restart : in std_ulogic;										--restarts watchdog timer
		i_time : in std_ulogic_vector(g_watchdog_size -1 downto 0);		--watchdog cycles
		o_timeout : out std_ulogic);		
end watchdog_timer;

architecture arch of watchdog_timer is
	signal w_watchdog_cycles_reg : std_ulogic_vector(g_watchdog_size -1 downto 0);
begin
	watchdog : process(i_clk) 
		variable cnt : integer range 0 to 2**g_watchdog_size -1;
	begin
		if(rising_edge(i_clk)) then
			if(i_rst = '1') then
				o_timeout <= '0';
				cnt := 0;
				w_watchdog_cycles_reg <= (others => '0');
			else
				if(i_dv = '1') then
					w_watchdog_cycles_reg <= i_time;
				end if;

				if(i_restart = '1') then
					cnt := to_integer(unsigned(i_time));
					o_timeout <= '0';
				else
					if(cnt > 1) then
						cnt := cnt -1;
					elsif(cnt = 1) then
						cnt := cnt -1;
						o_timeout <= '1';
					else
						o_timeout <= '0';
						cnt := to_integer(unsigned(w_watchdog_cycles_reg));
					end if;
				end if;
			end if;
		end if;
	end process; -- watchdog
end arch;