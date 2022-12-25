library ieee;
use ieee.std_logic_1164.all;

entity one_shot is 
port(
	i_clk : in std_ulogic;
	i_rst : in std_ulogic;
	i_s   : in std_ulogic;		-- signal with potential pulse length > 1 clock
	o_s   : out std_ulogic);	-- signal with pulse length limited to 1 clock
end one_shot;

architecture rtl of one_shot is
	signal r_sync : std_ulogic_vector(1 downto 0);
	signal r_s : std_ulogic;
begin

	sync : process(i_clk)
	begin
		if(i_rst = '1')then
			r_sync <= "00";
		elsif(rising_edge(i_clk))then
			r_sync(0) <= i_s;
			r_sync(1) <= r_sync(0);
			r_s <= r_sync(1);
		end if;
	end process;

	o_s <= r_sync(1) and (not r_s);
end rtl;