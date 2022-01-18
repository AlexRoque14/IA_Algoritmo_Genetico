import Genetico as gnetic
import math 

class Calculos():
    
    def __init__(self): 
        self.min_x = 0 
        self.min_y = 0 
        self.dx  = 0 
        self.dy = 0

    #Convierte numeros a binarios
    def convert_binary(cromosomas , bit):
        aux = 0
        bits = '0' + str(bit) + 'b'
        for iter in range(len(cromosomas)):
            for inside in range(2):
                aux = cromosomas[iter][inside]
                cromosomas[iter][inside] = format(int(aux), bits)
        return cromosomas

    #Convierte de binario a decimal
    def convert_decimal(cromosomas):
        aux = 0
        for iter in range(len(cromosomas)):
            for inside in range(2):
                aux = cromosomas[iter][inside]
                cromosomas[iter][inside] = int(str(aux), 2)
        return cromosomas
        
    #Realiza la poda
    def operation_poda(self, population , min_x , min_y , dx , dy):
        self.min_x = min_x
        self.min_y = min_y
        self.dx = dx
        self.dy = dy

        menor_fitness = []
        coordenadas = []
        Ind_poda = len(population)//2
        bests_fitness = []
        
        scores = [(self.fitness(i) , i) for i in population]
        for i in sorted(scores , reverse=False):
            coordenadas.append(i)
            menor_fitness.append(i[0])
            bests_fitness.append(i[1])
        
        selected = bests_fitness[:Ind_poda]
        cord_max = min(coordenadas) 
        print("Seleccionados: " , selected)

        return selected , menor_fitness, bests_fitness , cord_max[1]
 
    def fitness(self, individual):
        #Formula: z(x , y) = x cos (y) + y sin (x) 
        fitness = 0
        cor_x = 0
        cor_y = 0   

        #Se obtienen las coordenadas de X y Y
        cor_x = self.min_x + ( individual[0] * self.dx)
        cor_y = self.min_y + (individual[1] * self.dy )

        part1 = cor_x * math.cos(cor_y)
        part2 = cor_y * math.sin(cor_x)
        fitness = part1 + part2
        return fitness
    

    def getBits(a, b, c, d, e):
        #Se calcula para Y
        rango_x = d - c
        delta = 2 * e
        saltos_y = int( rango_x/ delta)
        aux_y = format(saltos_y, "b")
        bits_y = len(aux_y)
        Dy =  rango_x / math.pow(2, bits_y)
        print('Y usara ', bits_y, ' bits\nDy: ', Dy)

        #Se calcula para X
        rango = b - a
        delta = 2 * e
        
        saltos_x = int(rango / delta)
        aux_x = format(saltos_x, "b")
        bits_x = len(aux_x)
        Dx = rango / math.pow(2, bits_x)
        print('X usara ', bits_x, ' bits\nDx: ', Dx)

        if bits_x > bits_y:
            print('Se usaran ', bits_x, ' bits')
            return bits_x , Dx , Dy
        else:
            print('Se usaran ', bits_y, ' bits')
            return bits_y , Dx , Dy
