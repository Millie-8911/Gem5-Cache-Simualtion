import m5
import sys
from m5.objects import *

class L1ICache(Cache):
    size = "16kB"
    assoc = 1  # Set default assoc = 1, changed after getting assoc value in command 
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20
    write_buffers = 8
    writeback_clean = True

class L1DCache(Cache):
    size = "16kB"
    assoc = 1  # Set default assoc = 1, changed after getting assoc value in command 
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20
    write_buffers = 8
    writeback_clean = True

class L2Cache(Cache):
    size = "8kB"
    assoc = 1  # Set default assoc = 1, changed after getting assoc value in command 
    tag_latency = 10
    data_latency = 10
    response_latency = 100
    mshrs = 4
    tgts_per_mshr = 20
    write_buffers = 8
    writeback_clean = True

def run_simulation(assoc1, assoc2):
    system = System()
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "4GHz"
    system.clk_domain.voltage_domain = VoltageDomain()
    system.mem_mode = "timing"
    system.mem_ranges = [AddrRange("512MB")]
    system.cpu = TimingSimpleCPU()  # 使用 TimingSimpleCPU 简化

    # L1 cache
    system.cpu.icache = L1ICache(assoc=assoc1)
    system.cpu.dcache = L1DCache(assoc=assoc1)

    # L2 cache
    system.l2cache = L2Cache(assoc=assoc2)

   # bandwidth = 32
    system.membus = SystemXBar(width=32) 
    system.l2bus = L2XBar(width=32)
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]

    # Connect L1I and L1D to CPU ports
    system.cpu.icache_port = system.cpu.icache.cpu_side
    system.cpu.dcache_port = system.cpu.dcache.cpu_side

    # Connect L1I and L1D to L2 cache CPU side
    system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
    system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

    # Connect L2 CPU side to the memory side
    system.l2cache.cpu_side = system.l2bus.mem_side_ports

    # Connect L2 memory side to the CPU side ports
    system.l2cache.mem_side = system.membus.cpu_side_ports

    # Connect the memory controller to the bus
    system.mem_ctrl.port = system.membus.mem_side_ports

    # create the interrupt controller for the CPU
    system.cpu.createInterruptController()



    binary = "/resources/matmult"  
    system.workload = SEWorkload.init_compatible(binary)

    process = Process()
    process.cmd = [binary]
    system.cpu.workload = process
    system.cpu.createThreads()
    root.system = system
    m5.instantiate()
    return system

# Check if the arguments are sufficient(2 needed)
if len(sys.argv) < 3 or not sys.argv[1].startswith('--L1assoc=') or not sys.argv[2].startswith('--L2assoc='):
    print("Usage: python script.py --L1assoc=<L1 associativity> --L2assoc=<L2 associativity>")
    sys.exit(1)

# Extract assoc values from command
L1_assoc = int(sys.argv[1].split('=')[1])
L2_assoc = int(sys.argv[2].split('=')[1])

print("Running simulation with associativity:", L1_assoc, L2_assoc)

root = Root(full_system=False)
system = run_simulation(L1_assoc, L2_assoc)
print("Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
