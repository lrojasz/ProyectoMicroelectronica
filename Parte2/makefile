all:
	iverilog -o simulation system_area.v
	vvp simulation
	gtkwave simulation.vcd
area:
	iverilog -o simulation system_area.v
	vvp simulation
	gtkwave simulation.vcd
performance:
	iverilog -o simulation system_performance.v
	vvp simulation
	gtkwave simulation.vcd