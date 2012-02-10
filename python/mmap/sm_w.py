import mmap
import os
from time import sleep

f=open("sm.mmap", "r+")
f.write("Hello World 0\n")

smap=mmap.mmap(f.fileno(), 0)

for i in range(0,10):
    smap.seek(12)    
    smap.write(str(i))
    sleep(1)
smap.close()
