# gene.py
# Author: John Dickinson

'''
An organism has genes. Each gene controls one aspect
of the organism. Genes are passed on to the next generation
by way of sexual reproduction. Mutation may also occur and
change genes, add genes, or remove genes.
'''

import random

class Organism(object):
    def __init__(self, genes=None):
        if genes is None:
            genes = list()
        self.gene_pairs = genes
    
    def createGamete(self):
        gamete_genes = list()
        for pair in self.gene_pairs:
            gene = random.choice(pair)
            gene = mutate(gene)
            gamete_genes.append(gene)
        
        return gamete_genes
        
def mutate(gene):
    return gene

def mate(org1, org2):
    gamete1 = org1.createGamete()
    gamete2 = org2.createGamete()
    gene_pairs = list((i,j) for i in gamete1 for j in gamete2)
    return Organism(gene_pairs)

if __name__ == '__main__':
    pass
