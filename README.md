The entire program achieved the following steps.

1. Write-back Cache Class
Develop a gem5 system with x86 or ARM CPU, 4 GB memory, and 256 KB L1 write-back cache (shared instruction and data) components. Make the cache direct-mapped with 32-byte blocks and the memory write-through. Set a hit time of 1 cycle and a miss penalty of 20 cycles. Use the matrix multiplication program to demonstrate that it is working. Then, change the cache model to have separate L1 instruction and L1 data caches, each 256 KB with the same hit time and miss penalty. Again, run the matrix multiplication program to demonstrate that it is working.
2. Write-back Instruction and Data Caches
Change the cache model to have separate L1 instruction and data caches, each with 256 KB, the same hit time, and miss penalty. Again, run the matrix multiplication program to demonstrate that it is working.
3. Write-back Instruction and Data Caches
Conduct a study with the gem5 system above (with both cache models), varying the set associativity: 1, 2, 4, 8, 16, and 32. Produce at least one plot of the results and discuss any insights from the experiments.
4. Write-back Instruction and Data Caches
Develop a gem5 system with x86 or ARM CPU, 4 GB memory, x KB L1-I cache, y KB L1-D cache (each 2-way set-associative), and y MB L2 shared cache (4-way set-associative). Initially, set x=64 KB, y=128 KB, and 2 MB. Set an L1 hit time of 1 cycle, an L2 hit time of 10 cycles, and an L2 miss penalty of 100 cycles. Run the matrix multiplication benchmark to demonstrate that it is working. Make a few variations on x, y, and z (minimum 8) and show the results. Produce at least one plot of the results and discuss any insights from the experiments.
5. Final Report
Elaborate knowledge I observed from each steps.
