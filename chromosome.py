import random
from utils import binary_to_real

class Chromosome:
    MIN_VAL = -5
    MAX_VAL = 5
    BITS_PER_VAR = 16
    LENGTH = BITS_PER_VAR * 2

    def __init__(self, genes=None):
        self.genes = genes or ''.join(random.choice('01') for _ in range(self.LENGTH))

    def decode(self):
        x_bin = self.genes[:self.BITS_PER_VAR]
        y_bin = self.genes[self.BITS_PER_VAR:]
        x = binary_to_real(x_bin, self.MIN_VAL, self.MAX_VAL, self.BITS_PER_VAR)
        y = binary_to_real(y_bin, self.MIN_VAL, self.MAX_VAL, self.BITS_PER_VAR)
        return x, y

    def fitness(self, func):
        x, y = self.decode()
        return func.evaluate(x, y)

    def mutate(self, rate=0.01, method="one_point"):
        chrom_list = list(self.genes)
        if method == "one_point":
            for i in range(len(chrom_list)):
                if random.random() < rate:
                    chrom_list[i] = '1' if chrom_list[i] == '0' else '0'
        self.genes = ''.join(chrom_list)

    def inversion(self):
        chrom_list = list(self.genes)
        start = random.randint(0, len(chrom_list) - 2)
        end = random.randint(start + 1, len(chrom_list) - 1)
        chrom_list[start:end + 1] = chrom_list[start:end + 1][::-1]
        self.genes = ''.join(chrom_list)
