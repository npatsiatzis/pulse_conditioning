library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;


entity pwm is 
generic(
	g_sys_clk : integer := 10_000_000;	--frequency of the system clock in Hz
	g_pwm : integer := 10_000;			--frequency of PWM in Hz
	g_bits_resolution : integer :=5);  -- bits of resolution in setting the duty cycle
port(
	i_clk : in std_ulogic;
	i_rst : in std_ulogic;
	i_duty : in std_ulogic_vector(g_bits_resolution-1 downto 0);
	o_pwm : out std_ulogic);
end pwm;

architecture rtl of pwm is
	constant div_range : natural := natural(ceil(log2(real((g_sys_clk / (g_pwm * (2**g_bits_resolution)))))));
	constant div_duty  : natural := natural(ceil(log2(real((2**g_bits_resolution) -1))));
	signal count_div_ena : std_ulogic;
	signal dir : std_ulogic;
begin
	clk_div_counter : process(i_clk) is
		variable count_div : unsigned(div_range -1 downto 0);
		--variable count_div : integer range 0 to (g_sys_clk / (g_pwm * (2**g_bits_resolution)));
	begin
		if(i_rst = '1')then
			count_div :=(others => '0');
			count_div_ena <= '0';
		elsif(rising_edge(i_clk))then
			count_div_ena <= '0';
			if(count_div < (g_sys_clk / (g_pwm * (2**g_bits_resolution))))then
				count_div := count_div + 1;
			else
				count_div :=(others => '0');
				count_div_ena <= '1';
			end if;
		end if;
	end process; 

	duty_counter : process(i_clk) is
		variable count_duty : unsigned(div_duty -1 downto 0);
		--variable count_duty : integer range 0 to (2**g_bits_resolution) -2;
	begin
		if(i_rst = '1')then
			count_duty := (others => '0');
			o_pwm <= '0';
		elsif(rising_edge(i_clk))then
			if(count_div_ena = '1')then
				if(count_duty < (2**g_bits_resolution)-1)then
					count_duty := count_duty + 1;	
				else 
					count_duty :=(others => '0');
				end if;
			end if;
			if(to_integer(unsigned(i_duty)) < count_duty)then
				o_pwm <= '0';
			else
				o_pwm <= '1';
			end if;
		end if;
	end process; 

	--duty_counter : process(i_clk)
	--	variable count_duty : integer range 0 to (2**g_bits_resolution) -2;
	--begin
	--	if(i_rst  = '1')then
	--		dir <= '0';
	--		count_duty := 0;
	--      o_pwm <= '0';
	--	elsif(rising_edge(i_clk))then
	--		if(count_div_ena = '1')then
	--			if(dir = '0')then
	--				if(count_duty < (2**g_bits_resolution)-2)then
	--					count_duty := count_duty +1;
	--				else 
	--					dir <= '1';
	--					count_duty := count_duty -1;
	--				end if;	
	--			else
	--				if(count_duty >0)then
	--					count_duty := count_duty  -1;
	--				else
	--					count_duty := count_duty +1;
	--					dir <= '0';
	--				end if;
	--			end if;
	--		end if;
	--		if(to_integer(unsigned(i_duty)) < count_duty)then
	--			o_pwm <= '0';
	--		else
	--			o_pwm <= '1';
	--		end if;
	--	end if;
	--end process; -- duty_counter
end rtl;