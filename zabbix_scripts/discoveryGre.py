#!/usr/bin/env python
# -*- coding: utf-8 -*-
# discovery GRENAME:IP

import json

d = {}
i = {}
d["data"] = []
with open('/etc/myshell/tunnels.list', 'r') as f:
    for line in f.readlines():
	grename = line.split(":")[0]
	dstip = line.split(":")[2]
	i["{#GRENAME}"] = grename
	i["{#DSTIP}"] = dstip
	d["data"].append(dict(i))

print json.dumps(d)
