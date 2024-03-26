import m5
from m5.objects import Cache

# Add the common scripts to our path
m5.util.addToPath("../../")

from common import SimpleOpts

class L1Cache(Cache):
    """Simple L1 Cache with default values"""

    def __init__(self, size: "512MB", assoc: int = 1, tag_latency: int = 10, data_latency: int = 10, response_latency: int = 1, mshrs: int = 20, tgts_per_mshr: int = 12, writeback_clean: boolean = False): 
        super().__init__()
        self.size = size
        self.assoc = assoc  # Direct-mapped
        # self.cache_line_size = 32  # 32-byte blocks
        self.tag_latency = tag_latency # Hit time of 1 cycle
        self.data_latency = data_latency
        self.response_latency = response_latency
        self.mshrs = mshrs
        self.tgts_per_mshr = tgts_per_mshr
        self.writeback_clean = writeback_clean
        self.cache_line_size = 32  # Set cache line (block) size to 32 bytes

    def connectBus(self, bus):
        """Connect this cache to a memory-side bus"""
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU-side port
        This must be defined in a subclass"""
        raise NotImplementedError


class L1ICache(L1Cache):
    def __init__(self, size, assoc):
        super().__init__(size, assoc)

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU icache port"""
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    def __init__(self, size, assoc):
        super().__init__(size, assoc)

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU dcache port"""
        self.cpu_side = cpu.dcache_port


class L2Cache(Cache):
    def __init__(self, size, assoc):
        super().__init__(size, assoc)

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
