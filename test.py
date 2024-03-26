import subprocess

### Run through the assoc value list 
### Extract needed info from stats.txt
associativities = [1, 2, 4, 8, 16, 32]

for assoc in associativities:
    # Insert assoc to the command
    command = f"/gem5/build/ARM/gem5.opt /gem5/configs/learning_gem5/part1/WriteBackCache.py --assoc={assoc}"
    process = subprocess.Popen(command, shell=True)
    # Wait until the command is executed
    process.wait()
    # Extract hits, misses from stats.txt
    command2 ="cat /resources/project2/m5out/Stats.txt | grep -E \"simSeconds|overallMisses::total|overallHits::total\""
    process2 = subprocess.Popen(command2, shell=True)
    # Wait until the command is executed
    process2.wait()
