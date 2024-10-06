#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
sets – The practical way to do set operations on sets of lines in the shell

Copyright © 2012, 2013  Mattias Andrée (m@maandree.se)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys


def print(text = '', end = '\n'):
    sys.stdout.buffer.write((str(text) + end).encode('utf-8'))


if len(sys.argv) != 2:
    sys.argv.append('--help')
if sys.argv[1].startswith('-'):
    if sys.argv[1] in ('-c', '--copying', '--copyright'):
        print()
        print()
        print('sets – The practical way to do set operations on sets of lines in the shell')
        print()
        print('Copyright © 2012, 2013  Mattias Andrée (m@maandree.se)')
        print()
        print('This program is free software: you can redistribute it and/or modify')
        print('it under the terms of the GNU Affero General Public License as published by')
        print('the Free Software Foundation, either version 3 of the License, or')
        print('(at your option) any later version.')
        print()
        print('This program is distributed in the hope that it will be useful,')
        print('but WITHOUT ANY WARRANTY; without even the implied warranty of')
        print('MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the')
        print('GNU Affero General Public License for more details.')
        print()
        print('You should have received a copy of the GNU Affero General Public License')
        print('along with this program.  If not, see <http://www.gnu.org/licenses/>.')
        print()
        print()
    elif sys.argv[1] in ('-w', '--warranty'):
        print()
        print()
        print('This program is distributed in the hope that it will be useful,')
        print('but WITHOUT ANY WARRANTY; without even the implied warranty of')
        print('MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the')
        print('GNU Affero General Public License for more details.')
        print()
        print()
    else:
        print()
        print()
        print('sets – The practical way to do set operations on sets of lines in the shell')
        print()
        print('USAGE: sets (-c | -w | FORMULA)')
        print()
        print('OPTIONS:')
        print()
        print('    -c')
        print('    --copying')
        print('    --copyright    Display copyright information')
        print()
        print('    -w')
        print('    --warranty     Display warranty disclaimer')
        print()
        print('FORMULA:')
        print()
        print('    Symbols:      Function: (corresponding logical function)')
        print()
        print( '    ~ C ∁ ! ¬     Complement (not)')
        print( '    ^ ⊕ ∆ ⊗ ⊻     Symmetrical difference (parity/xor)')
        print( '    & * ∧ ⋀ ∩ ⋂   Intersection (and)')
        print( '    | + ∨ ⋁ ∪ ⋃   Union (or)')
        print('    - − \\ ↛       Difference (material nonimplication/abjunction)')
        print( '    0 ∅           Empty set (false)')
        print( '    U Ω Ω 𝓤       Universe (true)')
        print()
        print('    Round brackets are recognised for evaluation order grouping.')
        print()
        print('    Sets are from stdin are numbers from 1 and up in decimal.')
        print()
        print('INPUT:')
        print()
        print('    In stdin you send sets of sets of lines, a set of line contains')
        print('    no empty lines, and sets of lines are seperated by a blank line.')
        print()
        print('    So if you want the sets 1 = {a, b, c}, 2 = {b}, 3 = {a, c}, your')
        print('    message in standard input should be:')
        print('        a')
        print('        b')
        print('        c')
        print()
        print('        b')
        print()
        print('        a')
        print('        c')
        print()
        print()
        print('Copyright © 2012, 2013  Mattias Andrée (m@maandree.se)')
        print()
        print('This program is free software: you can redistribute it and/or modify')
        print('it under the terms of the GNU Affero General Public License as published by')
        print('the Free Software Foundation, either version 3 of the License, or')
        print('(at your option) any later version.')
        print()
        print()
    sys.stdout.buffer.flush()
    exit(0)
    

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
formula = formula.replace('C', '~').replace('!', '~').replace('¬', '~')
formula = formula.replace('∁', '~').replace('∅', '0').replace('∆', '^')
formula = formula.replace('∧', '&').replace('∨', '|').replace('∩', '&')
formula = formula.replace('∪', '|').replace('⊗', '^').replace('⊻', '^')
formula = formula.replace('⋀', '&').replace('⋁', '|').replace('⋂', '&')
formula = formula.replace('⋃', '|').replace('Ω', 'U').replace('Ω', 'U')
formula = formula.replace('⊕', '^').replace('𝓤', 'U').replace('↛', '-')
formula = formula.replace('−', '-')


for i in range(0, 10):
    formula = formula.replace('%i' % i, 'sets[%i]' % i)

formula = formula.replace(']sets[', '')

rc = eval(formula)

if rc.inv:
    rc = U - ~rc

for e in rc.elems:
    print(e)

sys.stdout.buffer.flush()

