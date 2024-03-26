import m5
import sys
from m5.objects import *

### Run test.py to execute this py file 
class L1ICache(Cache):
    size = "256kB"
    #assoc = 1  
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20
    write_buffers = 8
    writeback_clean = True

class L1DCache(Cache):
    size = "256kB"
    #assoc = 1  
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
    system.clk_domain.clock = "4GHz"
    system.clk_domain.voltage_domain = VoltageDomain()
    system.mem_mode = "timing"
    system.mem_ranges = [AddrRange("4GB")]
    system.cpu = TimingSimpleCPU()  

    # Input assoc as parameter
    system.cpu.icache = L1ICache(assoc=assoc)
    
    # Input assoc as parameter
    system.cpu.dcache = L1DCache(assoc=assoc)
    
    system.cpu.icache_port = system.cpu.icache.cpu_side
    system.cpu.dcache_port = system.cpu.dcache.cpu_side

    system.membus = SystemXBar(width=32) # bandwidth = 32
    system.cpu.icache.mem_side = system.membus.cpu_side_ports
    system.cpu.dcache.mem_side = system.membus.cpu_side_ports

    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports
    system.system_port = system.membus.cpu_side_ports

    system.cpu.createInterruptController()

    binary = "/resources/matmult"  # c file path
    system.workload = SEWorkload.init_compatible(binary)

    process = Process()
    process.cmd = [binary]
    system.cpu.workload = process
    system.cpu.createThreads()
    root.system = system
    m5.instantiate()
    return system

# Check if the arguments is sufficient(lloking for 2 arguments)
if len(sys.argv) < 2 or not sys.argv[1].startswith('--assoc='):
    print("Usage: python script.py --assoc=<associativity>")
    sys.exit(1)

# Extract arguments(assoc)
assoc_str = sys.argv[1].split('=')[1]
try:
    assoc = int(assoc_str)
except ValueError:
    print("Invalid associativity value provided:", assoc_str)
    sys.exit(1)

print("Running simulation with associativity:", assoc)

root = Root(full_system=False)
system = run_simulation(assoc)
print("Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
