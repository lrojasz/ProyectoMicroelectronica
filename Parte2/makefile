all:
	iverilog -o simulation system_area.v
	vvp simulation
	gtkwave simulation.vcd
