#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

opt_fns = []
opt_keys = []
opt_vals = {}
opt_users = {}
opt_routes = []

syscfg="/opt/config/system.cfg"
inscfg="/opt/config/install.cfg"

cfgs = [ syscfg, inscfg ]
