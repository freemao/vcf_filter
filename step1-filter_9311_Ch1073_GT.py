import vcf

def judgeGT(P1GTlist, P2GTlist):
    P1GTset = set([i for i in P1GTlist if i])
    P2GTset = set([i for i in P2GTlist if i])
    if ((P1GTset == set(['0/0']) and P2GTset == set(['1/1']))
       or (P1GTset == set(['1/1']) and P2GTset == set(['0/0']))):
        return True
    else:
        return False

def filterHomo(input_vcffil, output_vcffile, P1, P2):
    '''e.g. P1=[L14-1, L14-2, L14-3]
    P2 = [L17-1, L17-2, L17-3]'''
    inputvcf = open(input_vcffil, 'r')
    outputvcf = open(output_vcffile, 'w')
    invcf = vcf.Reader(inputvcf)
    outvcf = vcf.Writer(outputvcf, invcf)
    for i in invcf:
        P1GT, P2GT = [], []
        for m,n in zip(P1, P2):
            P1GT.append(i.genotype(m)['GT'])
            P2GT.append(i.genotype(n)['GT'])
        if judgeGT(P1GT, P2GT):
            outvcf.write_record(i)
    inputvcf.close()
    outputvcf.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 9:
        p1list = [sys.argv[3], sys.argv[4], sys.argv[5]]
        p2list = [sys.argv[6], sys.argv[7], sys.argv[8]]
        filterHomo(sys.argv[1],sys.argv[2], p1list, p2list)
    else:
        print 'Usage:\npython filter_9311_Ch1073.py input_vcffile output_vcffile P1-1 P1-2 P1-3 P2-1 P2-2 P2-3'



