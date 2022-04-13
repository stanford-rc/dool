#!/usr/bin/python

### Example2: simple sub-second monitor (ministat)

### This is a quick example showing how to implement your own *stat utility
### If you're interested in such functionality, contact me at dag@wieers.com
import sys
sys.path.insert(0, '/usr/share/dool/')
import dool, time

### Set default theme
dool.theme = dool.set_theme()

### Allow arguments
try: delay = float(sys.argv[1])
except: delay = 0.2
try: count = int(sys.argv[2])
except: count = 10

### Load stats
stats = []
dool.starttime = time.time()
dool.tick = dool.ticks()
for o in (dool.dool_epoch(), dool.dool_cpu(), dool.dool_mem(), dool.dool_load(), dool.dool_disk(), dool.dool_sys()):
    try: o.check()
    except Exception, e: print e
    else: stats.append(o)

### Make time stats sub-second
stats[0].format = ('t', 14, 0)

### Print headers
title = subtitle = ''
for o in stats:
    title = title + '  ' + o.title()
    subtitle = subtitle + '  ' + o.subtitle()
print '\n' + title + '\n' + subtitle

### Print stats
for dool.update in range(count):
    line = ''
    for o in stats:
        o.extract()
        line = line + '  ' + o.show()
    print line + dool.ansi['reset']
    if dool.update != count-1: time.sleep(delay)
    dool.tick = 1
print dool.ansi['reset']
