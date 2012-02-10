import mmap
import os
from time import sleep

f=open("sm.mmap", "r+b")
f.write("Hello World 0\n")

smap=mmap.mmap(f.fileno(), 0)

for i in range(0,10):
    smap.seek(0)
    print smap.readline()
    sleep(1)

smap.close()
