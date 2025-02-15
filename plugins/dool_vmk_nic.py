### Author: Bert de Bruijn <bert+dool$debruijn,be>

### VMware ESX kernel vmknic stats
### Displays VMkernel port statistics on VMware ESX servers

# NOTE TO USERS: command-line plugin configuration is not yet possible, so I've
# "borrowed" the -N argument.
# EXAMPLES:
# # dool --vmknic -N vmk1
# You can even combine the Linux and VMkernel network stats (just don't just "total").
# # dool --vmknic -n -N vmk0,vswif0
# NB Data comes from /proc/vmware/net/tcpip/ifconfig

class dool_plugin(dool):
    def __init__(self):
        self.name = 'vmknic'
        self.nick = ('recv', 'send')
        self.open('/proc/vmware/net/tcpip/ifconfig')
        self.cols = 2

    def check(self):
        try:
            os.listdir('/proc/vmware')
        except:
            raise Exception('Needs VMware ESX')
        info(1, 'The vmknic module is an EXPERIMENTAL module.')

    def discover(self, *list):
        ret = []
        for l in self.fd[0].splitlines(replace=' /', delim='/'):
            if len(l) != 12: continue
            if l[2][:5] == '<Link': continue
            if ','.join(l) == 'Name,Mtu/TSO,Network,Address,Ipkts,Ierrs,Ibytes,Opkts,Oerrs,Obytes,Coll,Time': continue
            if l[0] == 'lo0': continue
            if l[0] == 'Usage:': continue
            ret.append(l[0])
        ret.sort()
        for item in list: ret.append(item)
        return ret

    def vars(self):
        ret = []
        if op.netlist:
            list = op.netlist
        else:
            list = self.discover
            list.sort()
        for name in list:
            if name in self.discover + ['total']:
                ret.append(name)
        return ret

    def name(self):
        return ['net/'+name for name in self.vars]

    def extract(self):
        self.set2['total'] = [0, 0]
        for line in self.fd[0].readlines():
            l = line.replace(' /','/').split()
            if len(l) != 12: continue
            if l[2][:5] == '<Link': continue
            if ','.join(l) == 'Name,Mtu/TSO,Network,Address,Ipkts,Ierrs,Ibytes,Opkts,Oerrs,Obytes,Coll,Time': continue
            if l[0] == 'Usage:': continue
            name = l[0]
            if name in self.vars:
                self.set2[name] = ( int(l[6]), int(l[9]) )
            if name != 'lo0':
                self.set2['total'] = ( self.set2['total'][0] + int(l[6]), self.set2['total'][1] + int(l[9]) )

        if update:
            for name in self.set2:
                self.val[name] = list(map(lambda x, y: (y - x) * 1.0 / elapsed, self.set1[name], self.set2[name]))

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4
