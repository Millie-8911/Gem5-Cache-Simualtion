import m5
import sys
from m5.objects import *

# Define unified cache
class L1Cache(Cache):
    size = "256kB"
    assoc = 2 
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 20
    tgts_per_mshr = 20
    write_buffers = 8
    writeback_clean = True

def run_simulation():
    system = System()
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "4GHz"
    system.clk_domain.voltage_domain = VoltageDomain()
    system.mem_mode = "timing"
    system.mem_ranges = [AddrRange("4GB")]
    system.cpu = TimingSimpleCPU()  

    # Build a shared L1 Cache
    system.cpu.icache = L1Cache()
    system.cpu.dcache = L1Cache()

    system.cpu.icache.cpu_side = system.cpu.icache_port
    system.cpu.dcache.cpu_side = system.cpu.dcache_port

    system.membus = SystemXBar(width=32)
    system.cpu.icache.mem_side = system.membus.cpu_side_ports
    system.cpu.dcache.mem_side = system.membus.cpu_side_ports

    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports
    system.system_port = system.membus.cpu_side_ports

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

print("Running simulation with shared L1 cache.")
root = Root(full_system=False)
system = run_simulation()
print("Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")