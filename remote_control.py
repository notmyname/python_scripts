#!/usr/bin/env python

import getpass
import pexpect
import sys
import optparse
sys.path.insert(0, '/home/john/python_scripts/')
import Common

@Common.deferred_fork
def main(script_name, host_list, command, pw):
    username = 'joeuser'
    for hostname in host_list:
        print 'processing %s' % hostname
        child = pexpect.spawn('ssh %s@%s \'%s\'' % (username, hostname, command))
        
        timeout_count = 0
        while True:
            try:
                index = child.expect(['assword:',
                                      '(yes/no)',
                                      'cannot connect to %s'%hostname,
                                      '\[sudo\] password for %s:'%username,
                                      pexpect.TIMEOUT,
                                      pexpect.EOF], timeout=1.0)
            except:
                print child.before.replace(pw, '').strip()
                raise
            if index == 0:
                # password expected
                print 'password expected'
                child.sendline(pw)
            elif index == 1:
                # need to add the fingerprint
                child.sendline('yes')
                print 'added fingerprint for %s' % hostname
            elif index == 2:
                # error connecting
                print 'cannot connect to %s (No route to host)' % hostname
                continue
            elif index == 3:
                print 'sudo password expected'
                child.sendline(pw)
            elif index == 4:
                timeout_count += 1
                if timeout_count > 30:
                    timeout_count = 0
                    print 'still waiting...'
                    output = child.before.replace(pw, '').strip()
                    if not output:
                        print 'nothing has happened, %s is unresponsive. moving on...' % hostname
                        break
                    print output
                    child.before = ''
            elif index == 5:
                print child.before.replace(pw, '').strip()
                break

def usage(script_name):
    return 'Usage: %s [-p] -c <command> host1[ host2[ host3[ ...]]]' % script_name

if __name__ == '__main__':
    script_name = sys.argv[0]
    opt = optparse.OptionParser(usage=usage(script_name))
    opt.add_option('-p', '--pool', action='store_true', default=False)
    opt.add_option('-c', '--command')
    options, host_list = opt.parse_args()
    if host_list and options.command:
        pw = getpass.getpass('Password for tladmin: ')
        pool_size = 5 if options.pool else 1
        pool = []
        pool_slice = len(host_list) / pool_size
        if pool_slice == 0:
            pool_slice = len(host_list)
        for i in xrange(pool_size):
            start = i * pool_slice
            end = start + pool_slice
            pool.append(main(script_name, host_list[start:end], options.command, pw))
            if end > len(host_list):
                pool_size = max(1,i)
                break
        for i in xrange(pool_size):
            pool[i]()
    else:
        print usage(script_name)
