#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
sets – The practical way to do set operations on sets of lines in the shell

Copyright © 2012  Mattias Andrée (maandree@kth.se)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys

def print(text = '', end = '\n'):
    sys.stdout.buffer.write((str(text) + end).encode('utf-8'))


class Set():
    def __init__(self):
        self.inv = False
        self.elems = set()
    
    def __and__(x, y):
        if x.inv and y.inv:
            return ~(~x | ~y)
        elif y.inv:
            return x - ~y
        elif x.inv:
            return y - ~x
        else:
            rc = Set()
            for e in x.elems:
                if e in y.elems:
                    rc.elems.add(e)
            return rc
    
    def __or__(x, y):
        if x.inv and y.inv:
            return ~(~x & ~y)
        elif y.inv:
            return x | (U - ~y)
        elif x.inv:
            return y | (U - ~x)
        else:
            rc = Set()
            for e in x.elems:
                rc.elems.add(e)
            for e in y.elems:
                if e not in rc.elems:
                    rc.elems.add(e)
            return rc
    
    def __xor__(x, y):
        return (x | y) - (x & y)
    
    def __sub__(x, y):
        if x.inv and y.inv:
            return ~y - ~x
        elif x.inv:
            return ~(~x | y)
        else:
            rc = Set()
            for e in x.elems:
                if (e in y.elems) == y.inv:
                    rc.elems.add(e)
            return rc
    
    def __invert__(x):
        rc = Set()
        rc.elems = x.elems
        rc.inv = not x.inv
        return rc


sets = [Set()]
next = Set()
U = Set()


try:
    while True:
        e = input()
        if len(e) == 0:
            if len(next.elems) > 0:
                sets.append(next)
                next = Set()
        else:
            if e not in next.elems:
                next.elems.add(e)
            if e not in U.elems:
                U.elems.add(e)
except:
    pass

if len(next.elems) > 0:
    sets.append(next)


formula = sys.argv[1]
formula = formula.replace('\\', '-').replace('*', '&').replace('+', '|')
formula = formula.replace('C', '~').replace('!', '~')

for i in range(0, 10):
    formula = formula.replace('%i' % i, 'sets[%i]' % i)

formula = formula.replace(']sets[', '')

rc = eval(formula)

if rc.inv:
    rc = U - ~rc

for e in rc.elems:
    print(e)

sys.stdout.buffer.flush()

