import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

log = open('perf_java_20.txt')
time_mmap = []
len_mmap = []
time_munmap = []
len_munmap = []
time_page_fa = []
len_page_fa = []
for line in log:
    line = line.strip()
    if "page-faults" in line:
        time = line.split(':')[0].split()[2]
        time_page_fa.append(int(time.split('.')[0]) * (10 ** 6) + int(time.split('.')[1]))
        len_page_fa.append(int(line.split(':')[1].split('p')[0].strip()))
    else:
        parts = re.search(r'.*\] ([^:]*).*len:([^,]*)', line)
        time = int(parts.group(1).split('.')[0]) * (10 ** 6) + int(parts.group(1).split('.')[1])
        len = int(parts.group(2), 16)
        if "syscalls:sys_enter_mmap" in line:
            time_mmap.append(time)
            len_mmap.append(len)
        else:
            time_munmap.append(time)
            len_munmap.append(len)


time0 = min(time_mmap[0],time_munmap[0],time_page_fa[0])
time_mmap[:] = [x - time0 for x in time_mmap]
time_munmap[:]= [x - time0 for x in time_munmap]
time_page_fa[:] = [x - time0 for x in time_page_fa]
plt.plot(time_mmap,len_mmap,'ro', label = "mmap")
plt.plot(time_munmap, len_munmap, 'bs', label = "munmap")
plt.plot(time_page_fa, len_page_fa, 'g^', label = "page faults")
plt.xlabel('Time')
plt.ylabel('Length')
plt.legend()
plt.show()