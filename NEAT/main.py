"""
2-input XOR example -- this is most likely the simplest possible example.
"""

from __future__ import print_function

import os

import neat

import simulator
import visualize
import my_statistics

# 2-input XOR inputs and expected outputs.
# xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
# xor_outputs = [   (0.0,),     (1.0,),     (1.0,),     (0.0,)]
world = simulator.World('circuit.txt')

max_iterations_without_getting_goal = 50
points_per_goal = 100
threshold = .9
generations_to_run=300


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0.0
        iterations_without_getting_goal = 0.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        world.reset_car_position()
        sensors=world.get_sensors()
        sensors=tuple(sensors)
        w=net.activate(sensors)
        res=world.next_step(w)
        while res>=0 and iterations_without_getting_goal<max_iterations_without_getting_goal:
            if res>0:
                genome.fitness += points_per_goal-iterations_without_getting_goal
                iterations_without_getting_goal = 0
            else:
                iterations_without_getting_goal+=1
            sensors=world.get_sensors()
            sensors=tuple(sensors)
            w=net.activate(sensors)
            res=world.next_step(w)


def save_simulation(genome,config,file):
    f = open(file)
    iterations_without_getting_goal = 0.0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    world.reset_car_position()
    sensors = world.get_sensors()
    sensors = tuple(sensors)
    w = net.activate(sensors)
    res = world.next_step(w)
    while res >= 0 and iterations_without_getting_goal < max_iterations_without_getting_goal:
        if res > 0:
            iterations_without_getting_goal = 0
        else:
            iterations_without_getting_goal += 1
        sensors = world.get_sensors()
        sensors = tuple(sensors)
        w = net.activate(sensors)
        res = world.next_step(w)
        pos=world.car.get_pos()
        a=world.car.get_ang()
        f.write('%s %s %s\n' % (pos[0],pos[1],a))

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    config.fitness_threshold = world.get_num_goals()*points_per_goal*threshold


    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    stats = my_statistics.MyStatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, generations_to_run)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    baseFolder='../PathContainer/'
    most_fit_5_genomes=stats.get_most_fit_5_genomes()
    for i in range(len(most_fit_5_genomes)):
        generationFolder=baseFolder+'Generation%s/' % (i+1)
        for j in range(len(most_fit_5_genomes[i])):
            genomeFile=generationFolder+'Path%s.txt' % (j+1)
            save_simulation(most_fit_5_genomes[i][j],config,genomeFile)

    # Show output of the most fit genome against training data.
    # print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    # visualize.draw_net(config, winner, True, node_names=node_names) no em funciona
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)



if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)

