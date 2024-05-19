import numpy as np
from typing import List

from packing_tools import Point, Polygon

'''
    Returns length of bounding box of polygons in a certain arrangement
    Serves as a metric to evaluate the efficiency of a certain arrangement
'''
def get_packing_length(polygons: List[Polygon], history_index_list, history_length_list, width, **kw) -> int:

    polygons = PolyListProcessor.getPolyVertices(polygons)
    index_list = PolyListProcessor.getPolyIndex(poly_list)
    check_index = PolyListProcessor.getIndex(index_list, history_index_list)

    if check_index >= 0:
        return history_length_list[check_index]

    try: # no idea what this does
        if 'NFPAssistant' in kw:
            blf = BottomLeftFill(width, polygons, NFPAssistant = kw['NFPAssistant'])
        else:
            blf = BottomLeftFill(width, polygons)
    
    except: # self intersection (??)
        length = 99999
    
    history_index_list.append(index_list)
    history_length_list.append(length)
    return length

class GeneticAlgorithm:

    def __init__(self, width, polygons: List[np.array], nfp_assistant=None, generations = 10, population_size = 20): # not sure what nfp asst is, why no height
        self.width = width
        self.minimal_rotation = 360 # what does this mean

        self.elite_size = 10 # number of 'elite' inviduals
        self.mutate_rate = .1 # see what this actually means
        self.generations = generations
        self.population_size = population_size

        self.nfp_assitant = nfp_assistant if nfp_assistant is not None else NFPAssitant(PolyListProcessor.getPolyVertices(poly_list), get_all_nfp = True) # not sure what this default assistant does

        self.genetic_algorithm()
        self.plot_record()

    def geneticAlgorithm(self):
        self.population = []
        self.length_record = []
        self.lowest_length_record = []
        self.global_best_sequence = []
        self.global_lowest_length = None

        for _ in range(0, self.generations):
            self.getLengthRanked() # not sure what 'length' actually refers to
            self.getNextGeneration()

            self.length_record.append(self.fitness_ranked[0][1]) # most fit ??
            
            if self.fitness_ranked[0][1] < self.global_lowest_length: # best (not sure why min)
                self.global_lowest_length = self.fitness_ranked[0][1]
                self.global_best_sequence = self.pop[self.fitness_ranked[0][0]]
            self.lowest_length_record.append(self.global_lowest_length)

            blf = BottomLeftFill(self.width, PolyListProcessor.getPolysVertices(self.global_best_sequence), NFPAssitant = self.NFPAssistant)
            blf.showAll() # i'm assuming this is the sorting / optimization function

        
    
