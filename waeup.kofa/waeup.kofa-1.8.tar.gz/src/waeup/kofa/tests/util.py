## $Id: util.py 7193 2011-11-25 07:21:29Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
import random

def get_randstring(length):
    result = ''
    for i in range(1, length):
        result += random.choice('abcdefghijklmnopqrstuvwxyz')
    return result

def get_randname():
    result = ''
    n1 = get_randstring(random.randint(4, 15))
    n2 = get_randstring(random.randint(4, 15))
    n3 = get_randstring(random.randint(4, 15))
    #n1[0] = n1[0].upper()
    #n2[0] = n2[0].upper()
    #n3[0] = n3[0].upper()
    return '"%s %s %s"' % (n1, n2, n3) 

def get_namelist(num):
    return [get_randname() for x in range(0, num)]

random.seed()
fd = open('namelist.txt', 'w')
for name in get_namelist(70000):
    fd.write(name + '\n')
fd.close()
