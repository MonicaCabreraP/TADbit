"""
23 abr 2015

This script generates a false genome for testing purposes
"""
from random import random
import re

# RANDOM GENOME
num_crms = 4
mean_crm_size = 10000000

nts = ('ATGC' * 100) +'N'

genome = {}
for crm in xrange(1, num_crms + 1):
    crm_len = int(mean_crm_size / 2 + mean_crm_size * random())
    genome['chr' + str(crm)] = ''.join([nts[int(401 * random())]
                                        for _ in xrange(crm_len)])

out = open('test.fa', 'w')
for crm in xrange(1, num_crms + 1):
    out.write('>chr%d\n' % crm)
    crm = 'chr' + str(crm)
    for p in xrange(0, len(genome[crm]), 60):
        out.write(genome[crm][p:p+60] + '\n')
out.close()

from pytadbit.parsers.genome_parser import parse_fasta

genome_bis = parse_fasta('test.fa')

if genome_bis == genome:
    genome = genome_bis
else:
    raise Exception('problem with genome parser')

# RE FRAGMENTS
frags = {}
for crm in genome:
    frags[crm] = {}
    beg = 0
    for pos in re.finditer('GATC', genome[crm]):
        end = pos.start()
        if beg == end:
            continue
        frags[crm][beg] = [beg, end]
        beg = end
    if beg != end:
        frags[crm][beg] = [beg, len(genome[crm])]

# RANDOM READS
sam_crm = '@SQ\tSN:%s\tLN:%d\n'
sam_head = """@HD\tVN:1.3
%s@RG\tID:0\tPG:GEM\tPL:ILLUMINA\tSM:0
@PG\tID:GEM\tPN:gem-2-sam\tVN:1.847
"""
crm_heads = ''
for crm in genome:
    crm_heads += sam_crm % (crm, len(genome[crm]))

sam_head = sam_head % crm_heads

read_str = '{id}\t{flag}\t{crm}\t{pos}\t254\t3M\t*\t0\t0\tAAA\tHHH\tRG:Z:0\tNH:i:1\tNM:i:0\tXT:A:U\tmd:Z:3\n'

# dangling ends
out1 = open('test_read1.sam', 'w')
out1.write(sam_head)
out2 = open('test_read2.sam', 'w')
out2.write(sam_head)
flags = [66, 82]
for i in xrange(1000):
    # pick one fragment
    crm  = genome.keys()    [int(random() * len(genome))]
    frag = frags[crm].keys()[int(random() * len(frags[crm]))]
    pos1 = int(random() * (frags[crm][frag][1] - frags[crm][frag][0])
               + frags[crm][frag][0])
    pos2 = int(random() * (frags[crm][frag][1] - frags[crm][frag][0])
               + frags[crm][frag][0])
    if pos2 > pos1:
        sd1 = 66
        sd2 = 82
    else:
        sd1 = 82
        sd2 = 66
    read1 = {'crm': crm, 'pos': pos1, 'flag': sd1, 'id': 'lala.%012d' % (i)}
    read2 = {'crm': crm, 'pos': pos2, 'flag': sd2, 'id': 'lala.%012d' % (i)}
    out1.write(read_str.format(**read1))
    out2.write(read_str.format(**read2))
    
out1.close()
out2.close()


# PARSE SAM
from pytadbit.parsers.sam_parser import parse_sam

parse_sam(['test_read1.sam'], ['test_read2.sam'],
          'lala1', 'lala2', genome, re_name='DPNII')

# GET INTERSECTION
from pytadbit.mapping.mapper import get_intersection

get_intersection('lala1', 'lala2', 'lala')

# FILTER
from pytadbit.mapping.filter import filter_reads

masked = filter_reads('lala')




