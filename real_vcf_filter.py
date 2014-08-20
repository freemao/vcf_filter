#!/usr/lib/python
#-*- coding:utf-8 -*-
import vcf
from optparse import OptionParser

msg_usage = '''usage: %prog [-I] input [-f1] 12-0/1-10-0.05 [-p1] ...
[-p2] ... [-O] output'''
descr = '''the raw vcf file must contain 3 samples(p1,p2,f1).
        filter each sample by genotype, depth, ratio(small/big).
        each items should concatenate by the dash.
        '''
optparser = OptionParser(usage = msg_usage, description = descr)
optparser.add_option('-I', '--input', dest = 'input',
                     help = 'input the name of your raw vcf file' )
optparser.add_option('-C', '--f1', dest = 'f1',
                     help = 'designate gt,dp,ratio of f1')
optparser.add_option('-A', '--p1', dest = 'p1',
                     help = 'designate gt,dp,ratio of p1')
optparser.add_option('-B', '--p2', dest = 'p2',
                     help = 'designate gt,dp,ratio of p2')
optparser.add_option('-O', '--output', dest = 'output',
                     help = 'the depth cutoff')
options, args = optparser.parse_args()


def asefilter(inputvcffile, f1_name, f1_genotype, f1_dp, f1_ratio, \
p1_name, p1_genotype, p1_dp, p1_ratio, \
p2_name, p2_genotype, p2_dp, p2_ratio, outputfile):
    '''each dp should be int and each ratio(small/big) should be float'''
    myvcf = vcf.Reader(open(inputvcffile, 'r'))
    rf = open(outputfile, 'w')
    rf_w = vcf.Writer(rf, myvcf)
    for i in myvcf:
        if i.is_snp:
            print i.POS
            f1gt = i.genotype(f1_name)['GT']
            f1dp = i.genotype(f1_name)['DP']
            f1ro = i.genotype(f1_name)['RO']
            f1ao = i.genotype(f1_name)['AO']
            if f1gt and type(f1ao) is int and f1ao+f1ro != 0:
                f1ratio = min(f1ro, f1ao)/float(f1ao+f1ro)
# return str, int, int, int, float

            p1gt = i.genotype(p1_name)['GT']
            p1dp = i.genotype(p1_name)['DP']
            p1ro = i.genotype(p1_name)['RO']
            p1ao = i.genotype(p1_name)['AO']
            if p1gt and type(p1ao) is int and p1ao+p1ro != 0:
                p1ratio = min(p1ro, p1ao)/float(p1ao+p1ro)
# if type is ins,ins will return a list [int, int] not int
            p2gt = i.genotype(p2_name)['GT']
            p2dp = i.genotype(p2_name)['DP']
            p2ro = i.genotype(p2_name)['RO']
            p2ao = i.genotype(p2_name)['AO']
            if p2gt and type(p2ao) is int and p2ao+p2ro != 0:
                p2ratio = min(p2ro, p2ao)/float(p2ao+p2ro)

            if (f1gt and type(f1ao) is int and f1ao+f1ro != 0
               and p1gt and type(p1ao) is int and p1ao+p1ro != 0
               and p2gt and type(p2ao) is int and p2ao+p2ro != 0
               and f1gt == f1_genotype and f1dp >= f1_dp and f1ratio > f1_ratio
               and p1gt == p1_genotype and p1dp >= p1_dp and p1ratio < p1_ratio
               and p2gt == p2_genotype and p2dp >= p2_dp and p2ratio < p2_ratio):
                rf_w.write_record(i)
    rf.close()

if __name__ == '__main__':
    infile = options.input
    outfile = options.output

    f1info = options.f1
    f1sm = f1info.split('-')[0]
    f1geno = f1info.split('-')[1]
    f1dp = int(f1info.split('-')[2])
    f1ration = float(f1info.split('-')[3])

    p1info = options.p1
    p1sm = p1info.split('-')[0]
    p1geno = p1info.split('-')[1]
    p1dp = int(p1info.split('-')[2])
    p1ration = float(p1info.split('-')[3])

    p2info = options.p2
    p2sm = p2info.split('-')[0]
    p2geno = p2info.split('-')[1]
    p2dp = int(p2info.split('-')[2])
    p2ration = float(p2info.split('-')[3])

    asefilter(infile, f1sm, f1geno, f1dp, f1ration, p1sm, p1geno, p1dp, p1ration, \
p2sm, p2geno, p2dp, p2ration, outfile)
