import random

#define the problem
num_courses = 5
num_halls = 2
num_time_slots = 3
hall_max_hours = 6
conflicts = {
    (1, 2): 10,
    (1, 4): 5,
    (2, 5): 7,
    (3, 4): 12,
    (4, 5): 8
}

#define the representation for a solution
def create_random_solution():
    solution = []
    for i in range(1, num_courses+1):
        course = i
        time_slot = random.randint(1, num_time_slots)
        hall = random.randint(1, num_halls)
        solution.append((course, time_slot, hall))
    return solution

#define the fitness function
def calculate_fitness(solution):
    score = 0
    
    #check for conflicting exams
    for pair, value in conflicts.items():
        if pair in [(x[0], y[0]) for i, x in enumerate(solution) for j, y in enumerate(solution) if i < j]:
            score += value
            
    #check for hall usage time
    for hall in range(1, num_halls+1):
        hall_time = 0
        for exam in solution:
            if exam[2] == hall:
                hall_time += 1
        if hall_time > hall_max_hours:
            score += (hall_time - hall_max_hours) * 10
    return score

#define the genetic algorithm
def genetic_algorithm(pop_size, num_generations, tourney_size, crossover_prob, mutation_prob):
    
    #initialize the population
    population = [create_random_solution() for i in range(pop_size)]
    for i in range(num_generations):
        
        #select parents for crossover
        parents = []
        for j in range(pop_size):
            tournament = random.sample(population, tourney_size)
            parent = min(tournament, key=calculate_fitness)
            parents.append(parent)
            
        #perform crossover
        offspring = []
        for j in range(pop_size):
            if random.random() < crossover_prob:
                parent1, parent2 = random.sample(parents, 2)
                crossover_point = random.randint(1, num_courses-1)
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
                offspring.append(child1)
                offspring.append(child2)
            else:
                offspring.append(parents[j])
                
        #perform mutation
        for j in range(pop_size):
            if random.random() < mutation_prob:
                index1, index2 = random.sample(range(num_courses), 2)
                offspring[j][index1], offspring[j][index2] = offspring[j][index2], offspring[j][index1]
                
        #evaluate fitness of offspring
        fitnesses = [calculate_fitness(solution) for solution in offspring]
        
        #select new population
        population = [offspring[i] for i in sorted(range(pop_size), key=lambda k: fitnesses[k])[:pop_size]]
        
    #return best solution
    best_solution = min(population, key=calculate_fitness)
    return best_solution, calculate_fitness(best_solution)

#run the genetic algorithm
best_solution, best_fitness = genetic_algorithm(100, 100, 5, 0.8, 0.1)
print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
