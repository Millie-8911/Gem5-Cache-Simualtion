import m5
from m5.objects import *
from m5.util import convert

# Define L1 Instruction Cache
class L1ICache(Cache):
    size = "256kB"
    assoc = 1  # Default value, will be overridden in run_simulation
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20
    write_buffers = 8
    writeback_clean = True

# Define L1 Data Cache
class L1DCache(Cache):
    size = "256kB"
    assoc = 1  # Default value, will be overridden in run_simulation
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20
    write_buffers = 8
    writeback_clean = True

def run_simulation(assoc):
    system = System()
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "1GHz"
    system.clk_domain.voltage_domain = VoltageDomain()
    system.mem_mode = "timing"
    system.mem_ranges = [AddrRange("4GB")]
    system.cpu = TimingSimpleCPU()  # Use TimingSimpleCPU for simplicity

    # L1 Instruction Cache with dynamic associativity based on input
    system.cpu.icache = L1ICache(assoc=assoc)
    
    # L1 Data Cache with dynamic associativity based on input
    system.cpu.dcache = L1DCache(assoc=assoc)
    
    system.cpu.icache_port = system.cpu.icache.cpu_side
    system.cpu.dcache_port = system.cpu.dcache.cpu_side

    system.membus = SystemXBar(width=32)
    system.cpu.icache.mem_side = system.membus.cpu_side_ports
    system.cpu.dcache.mem_side = system.membus.cpu_side_ports

    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports
    system.system_port = system.membus.cpu_side_ports

    system.cpu.createInterruptController()

    binary = "/resources/matmult"  # Ensure you change this to the correct path
    system.workload = SEWorkload.init_compatible(binary)

    process = Process()
    process.cmd = [binary]
    system.cpu.workload = process
    system.cpu.createThreads()

    return system

associativities = [1]
root = Root(full_system=False)

for assoc in associativities:
    system = run_simulation(assoc)
    root.system = system
    m5.instantiate()
    print(f"Beginning simulation with associativity {assoc}!")
    exit_event = m5.simulate()
    print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")