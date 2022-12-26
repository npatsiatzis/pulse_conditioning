library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity debounce is 
	generic(
		g_clk_freq : integer := 50*10**6;		-- system clock frequency in Hz
		g_stable : integer := 10			-- time the signal must be stable in ms
		);
	port(
		i_clk : in std_ulogic;
		i_rst : in std_ulogic;
		i_btn : in std_ulogic;
		o_btn : out std_ulogic
		);
end debounce;

architecture rtl of debounce is
	signal r_btn   : std_ulogic_vector(1 downto 0);
	signal stable  : std_ulogic;
begin

	stable <= r_btn(1) and r_btn(0);

	reg_btn : process(i_clk) 
	begin
		if(i_rst = '1')then
			r_btn <= "00";
		elsif(rising_edge(i_clk))then
			r_btn(0) <= i_btn;
			r_btn(1) <= r_btn(0);
		end if;
	end process; 

	cout_stable : process(i_clk) 
		--if signal stable time is given in anything else than ms, change the divisor accordingly
		--e.g make the divisor 10**6 if the stable time is given in us
		variable counter : integer range 0 to g_clk_freq * (g_stable-1) / 1000;
	begin
		if(i_rst = '1')then
			counter := 0;
			o_btn <= '0';
		elsif(rising_edge(i_clk))then
			o_btn <= '0';
			if(stable = '0')then
				counter :=0;
			elsif(counter < g_clk_freq * (g_stable-1) / 1000)then
				counter := counter + 1;
			else
				o_btn <= r_btn(1);
			end if;
		end if;
		
	end process; 
end rtl;
