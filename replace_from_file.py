import csv
import sys

with open(sys.argv[1]) as f:
    keys = dict(row for row in csv.reader(f, delimiter='\t'))

rdr = csv.reader(sys.stdin, delimiter='\t')

for row in rdr:
    print '\t'.join(keys.get(v, v) for v in row)
