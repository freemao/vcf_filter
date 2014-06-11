#/usr/lib/python
#-*- coding:utf-8 -*-

def FBfilter(qual, depth, vcfnamelist, type='snp'):
    for fn in vcfnamelist:
        filteredname = '.'.join(fn.split('.')[0:-1])+'.filtered.vcf'
        f0 = open(fn, 'r')
        f1 = open(filteredname, 'w')
        for i in f0:
            if i.startswith('#'):
                f1.write(i)
            else:
                j = i.split()
                if (float(j[5]) > qual and j[7].split(';')[-2].split('=')[-1] == type
                    and int(j[9].split(':')[1]) > depth) :
                    f1.write(i)
        f0.close()
        f1.close()

def GATKfilter(qual, depth, vcfnamelist):
    for fn in vcfnamelist:
        filteredname = '.'.join(fn.split('.')[0:-1])+'.filtered.vcf'
        f0 = open(fn, 'r')
        f1 = open(filteredname, 'w')
        for i in f0:
            if i.startswith('#'):
                f1.write(i)
            else:
                j = i.split()
                ref = j[3]
                alt = j[4]
                info = j[8].split(':')
                if (float(j[5]) > qual and len(ref) ==1 and len(alt) == 1
                    and len(info) == 5 and int(j[9].split(':')[2]) > depth):
                    f1.write(i)
        f0.close()
        f1.close()

def SBfilter(qual, depth, vcfnamelist):
    for fn in vcfnamelist:
        filteredname = '.'.join(fn.split('.')[0:-1])+'.filtered.vcf'
        f0 = open(fn, 'r')
        f1 = open(filteredname, 'w')
        for i in f0:
            if i.startswith('#'):
                f1.write(i)
            else:
                j = i.split()
                ref = j[3]
                alt = j[4]
                info = j[8].split(':')
                if (float(j[5]) > qual and len(ref) ==1 and len(alt) == 1
                    and int(j[9].split(':')[2]) > depth):
                    f1.write(i)
        f0.close()
        f1.close()

if __name__ == '__main__':
    import sys
    vcfnamelist = sys.argv[4:]
    q = float(sys.argv[2])
    d = float(sys.argv[3])
    print 'tool: '+sys.argv[1]
    print q
    print d
    print vcfnamelist
    if sys.argv[1]=='FB':
        FBfilter(q, d, vcfnamelist)
    elif sys.argv[1]=='GATK':
        GATKfilter(q, d, vcfnamelist)
    elif sys.argv[1]=='SB':
        SBfilter(q, d, vcfnamelist )
    else:
        print 'please choose the tool when you called snp used.'




