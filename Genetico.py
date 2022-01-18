import math
import numpy as np
import matplotlib.pyplot as plt
import random
import Calculos as calc
import Principal as views
from numpy.random import rand


#Formula: z(x , y) = x cos (y) + y sin (x) 
class Gnetico():
    def __init__(self , bits , n_selection , verbose , mutation_rate , n_individuals ,
        n_generations , n_maximo , min_x , max_x , min_y , max_y , error_x ):

        self.bits = bits
        self.n_selection = n_selection
        self.verbose = verbose
        self.mutation_rate = float(mutation_rate)
        self.n_individuals = int(n_individuals) 
        self.n_generations = int(n_generations)  
        self.n_maximo = int(n_maximo)
        self.min_x = int(min_x) 
        self.max_x = int(max_x)
        self.min_y = int(min_y) 
        self.max_y = int(max_y) 
        self.error_x = float(error_x)

        self.Mejores_fitness = []
        self.Peores_fitness = []
        self.promedio_mejor = []
        self.promedio_peor = []
        self.Promedios = []
        self.Delta_X = 0
        self.Delta_Y = 0


    def create_individual(self):
        ind_x = ''
        ind_y = ''
        for i in range(self.bits):
            ind_x += str(np.random.randint(0 ,2))
            ind_y += str(np.random.randint(0 ,2))
            
        individual = [ind_x, ind_y]
        print("Individuo: " , individual)
        return individual

    def create_population(self):
        population = [self.create_individual() for i in range(self.n_individuals)]
        return population

    def fitness(self, individual):
        #Formula: z(x , y) = x cos (y) + y sin (x) 
        fitness = 0
        cor_x = 0
        cor_y = 0   

        #Se obtienen las coordenadas de X y Y
        cor_x = (self.min_x + individual[0]) * self.Delta_X
        cor_y = (self.min_y + individual[1]) * self.Delta_Y

        part1 = cor_x * (math.cos(cor_y))
        part2 = cor_y * (math.sin(cor_x))

        fitness = part1 + part2

        return fitness


    def selection(self , population):
        bests_fitness = []
        scores = [(self.fitness(i) , i) for i in population]

        for i in sorted(scores , reverse=False):
            bests_fitness.append(i[1])

        selected = bests_fitness[:self.n_selection]
        print("Seleccionados: " , selected)
        return selected
        

    def reproduction(self, population, selected):
        #Metodo de cruza de un punto
        for x in range(len(selected)):
            pos = 0
            father = random.sample(selected, 1)                     #Aleatorio cual padre se cruzará de los seleccionados
            for y in range(2):
                point = np.random.randint(1 , self.bits-1)          #Crea un punto random entre 1 y el total de bits
                posicion = random.randint(1 , len(population)-1)    #Individuo random que mutará
                part1 = father[0][pos]
                select = population[posicion][y]

                child_1 = select[:point] + part1[point:]
                child_2 = select[point:] + part1[:point]
                new = [ child_1 , child_2 ]
                population.append(new)
        return population


    def mutation(self, population):
        #Mutación por probabilidad
        new_gen = ' ' 
        iter = random.randint(1 , len(population)-1)                #Numero de individuos que mutaran
        print("Individuos a mutar: ", iter)
        for _ in range(iter):
            if random.random() <= self.mutation_rate:               #probabilidad de que mute el indiv
                posicion = random.randint(1 , len(population)-1)    #Individuo random que mutará
                for x in range(2):
                    vector = population[posicion][x]
                    for inside in range(self.bits):
                            if vector[inside] == '1':
                                new_gen += '0'
                            elif vector[inside] == '0':
                                new_gen += '1'

                    population[posicion][x] = new_gen
                    new_gen = ' '
        return population
     

    def poda(self , population):
        poda, menores , coordenada, cord_max = calc.Calculos.operation_poda(self, population ,self.min_x, self.min_y , self.Delta_X , self.Delta_Y)
        self.Mejores_fitness.append(min(menores))
        self.Peores_fitness.append(max(menores))

        prom_min = sum(self.Mejores_fitness)/len(self.Mejores_fitness)
        prom_max = sum(self.Peores_fitness)/len(self.Peores_fitness)
        self.promedio_mejor.append(prom_min)
        self.promedio_peor.append(prom_max)
        
        self.graphics_evo_mejores(coordenada , cord_max)        #grafica las coordenadas obtenidas

        if len(population) > self.n_maximo:
            population = poda
            return population
        else:
            return population


    def imprimir_fitness(self):
        for i in range(len(self.Mejores_fitness)):
            print("Fitness gen ", i+1 , ": " , self.Mejores_fitness[i])


    def graphics_evo_mejores(self , coordenadas , cord_max):
        cord_x = []
        cord_y = []
        print("Cordenada del mejor: ", cord_max)
        for i in range(len(coordenadas)):
            cor_x = (self.min_x + coordenadas[i][0]) * self.Delta_X
            cor_y = (self.min_y + coordenadas[i][1]) * self.Delta_Y

            cord_x.append(cor_x)
            cord_y.append(cor_y)

        x = (self.min_x + cord_max[0]) * self.Delta_X
        y = (self.min_y + cord_max[1]) * self.Delta_Y

        plt.style.use('seaborn')
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.grid()

        plt.ion()
        plt.scatter(cord_x , cord_y, label='Normal', marker='o')
        plt.scatter( x, y, label='Mejor' ,marker='x')
        plt.legend(loc='upper left')
        plt.pause(0.7)
        plt.cla()
    

    def graphics_results_promedios(self):
        plt.style.use('seaborn')
        plt.title("Promedio por generacion")
        plt.ylabel('Promedio')
        plt.xlabel('Iteraciones')
        plt.plot(self.promedio_mejor, label = "Mejores promedios")
        plt.plot(self.promedio_peor, label = "Peores promedios")
        plt.legend(loc="center right") 
        plt.show()
    

    def graphics_results(self):
        mejor_fitness = max(self.Mejores_fitness)
        plt.style.use('seaborn')
        plt.title("Evolución del Fitness")
        plt.title(mejor_fitness)
        plt.ylabel('Fitness')
        plt.xlabel('Iteraciones')
        plt.plot(self.Mejores_fitness, label = "Mejores Fitness")
        plt.plot(self.Peores_fitness, label = "Peores Fitness")
        plt.legend(loc="center right") 
        plt.show()
    

    def genetic_run(self):

        self.bits , self.Delta_X  , self.Delta_Y = calc.Calculos.getBits(self.min_x , self.max_x , self.min_y , self.max_y , self.error_x)
        print("Bits a utilizar: " , self.bits)

        population = self.create_population()
        population = calc.Calculos.convert_decimal(population)

        for i in range(self.n_generations):
            if self.verbose:
                print('______________')
                print("GENERATION: ", i)
                print("POPULATION: " , population)

            selected = self.selection(population)
            population = calc.Calculos.convert_binary(population , self.bits)
            population = self.reproduction(population, selected)
            population = self.mutation(population)
            population = calc.Calculos.convert_decimal(population)
            population = self.poda(population)
    
        self.graphics_results_promedios()
        self.graphics_results()
        self.imprimir_fitness()


def main(prob_muta, pob_inicial , n_iter , pob_max , minx , maxx , miny , maxy , errx):
    model = Gnetico(bits = 0, n_selection=5 , verbose=True , 
    mutation_rate = prob_muta, n_individuals=pob_inicial ,n_generations=n_iter , 
    n_maximo = pob_max ,min_x = minx , max_x =maxx ,min_y =miny ,max_y = maxy , error_x=errx)
    
    model.genetic_run()


# CREDITS
__author__ = "Alexis Roque"
__copyright__ = "Copyright (C) 2021 Author Alexis Roque"
__program__ = "Algoritmo Genetico (IA)"
__date__ = "May 17. 16:20 hrs."
__version__ = "Final 1.0"