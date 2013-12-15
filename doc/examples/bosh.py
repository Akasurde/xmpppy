#!/usr/bin/env python
"""
Simple BOSH Bot Example
"""
import sys
import xmpp
from xmpp.transports import Bosh
from urllib2 import urlparse

def showhelp(*args):
    tpl = """
 Simple BOSH Bot Example

   bosh.py username passowrd endpoint [Options] -r|--resource <rsc>

 Required Arguments:

   username    A Username to authenticate with.

               Current: {0}

   password    A passowd to authenticate with.

               Current: {1}

   endpoint    The BOSH endpoint Url.

               Current: {2}

 Options:

  -r|--resource    Set the resource name <rsc> that will be used

                   Current: {3}

  -h|--help Show Help

"""
    print tpl.format(*args)

def connect(username, password, resource,  server='', port='', bosh='', use_srv=False):
    transport = None
    url = urlparse.urlparse(bosh)
    if bosh:
        transport = Bosh(bosh, use_srv)
    server = server or url.hostname
    port = port or 5522
    con = xmpp.Client(server, port)
    con.connect(transport=transport)
    print username, password, resource
    con.auth(username, password, resource)
    return con

def message(con, stanze):
    print stanze
    return stanze

def step(conn):
    try:
        i = conn.Process(1)
        if not i:
            return 1
    except KeyboardInterrupt:
        return 0
    return 1

def main(conn):
    while step(conn): pass

    print tpl.format(*args)

if __name__ == '__main__':
    args = sys.argv[1:]
    resource = 'simplebot'
    pos = []
    help = False
    username = ''
    password = ''
    endpoint = ''
    while args:
        arg = args.pop(0)
        if arg in ['-r', '--resource']:
            resource = args.pop(0)
            continue
        if arg in ['-h', '--help']:
            help = True
            continue
        if not arg.startswith('-'):
            if len(pos) == 0:
                username = arg
            elif len(pos) == 1:
                password = arg
            elif len(pos) == 2:
                endpoint = arg
            pos.push(arg)
            continue
    if help:
        showhelp(username, password, endpoint, resource)
        sys.exit(0)
    assert username and passowrd and endpoint, \
        'username, password, and endpoint required'
    username, password, endpoint = pos
    c = connect(username, password, resource, server, port, 'http://xmpp.h4.cx/xmpp')
    c.RegisterHandler('message', message)
    c.sendInitPresence()
    main(c)
