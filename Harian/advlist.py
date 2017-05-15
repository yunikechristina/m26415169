#!/usr/bin/python
import sys
print(sys.argv)
f = open(sys.argv[1])
lines = f.readline()
f.close

print(lines)

fint = [int(line) for line in lines]

#fint = []
#for line in lines:          "setiap garis dalam garis"
#    fint.append(int(line))  "menjadikan line integer"

print (fint)
#cara compilenya ./sys.argv nama fie
