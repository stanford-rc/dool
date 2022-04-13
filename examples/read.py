#!/usr/bin/python

### Example 1: Direct accessing stats
### This is a quick example showing how you can access dool data
### If you're interested in this functionality, contact me at dag@wieers.com
import sys
sys.path.insert(0, '/usr/share/dool/')
import dool

### Set default theme
dool.theme = dool.set_theme()

clear = dool.ansi['reset']
dool.tick = dool.ticks()

c = dool.dool_cpu()
print c.title() + '\n' + c.subtitle()
c.extract()
print c.show(), clear
print 'Percentage:', c.val['total']
print 'Raw:', c.cn2['total']
print

m = dool.dool_mem()
print m.title() + '\n' + m.subtitle()
m.extract()
print m.show(), clear
print 'Raw:', m.val
print

l = dool.dool_load()
print l.title() + '\n' + l.subtitle()
l.extract()
print l.show(), clear
print 'Raw:', l.val
print

d = dool.dool_disk()
print d.title() + '\n' + d.subtitle()
d.extract()
print d.show(), clear
print 'Raw:', d.val['total']
print
