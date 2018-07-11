#Imports for I/O processing

import json
import geopandas as gp
import networkx.readwrite
import os
import matplotlib.pyplot as plt
import functools


#Imports for RunDMCMC components
#You can look at the list of available functions in each
#corresponding .py file.

from rundmcmc.accept import (always_accept,cut_edge_accept,
                             metagraph_accept)

from rundmcmc.chain import MarkovChain

from rundmcmc.make_graph import (add_data_to_graph, construct_graph,
                                 get_assignment_dict)

from rundmcmc.partition import Partition

from rundmcmc.proposals import (propose_random_flip, propose_random_flip_no_loops,
                                propose_random_flip_metagraph, propose_several_random_flips)

from rundmcmc.updaters import (Tally, boundary_nodes, county_splits, cut_edges,
                               cut_edges_by_part, exterior_boundaries,
                               perimeters, polsby_popper,
                               votes_updaters,
                               interior_boundaries,MetagraphDegree)

from rundmcmc.validity import (L_minus_1_polsby_popper,L1_reciprocal_polsby_popper,
                               UpperBound,no_worse_L_minus_1_polsby_popper,
                               no_worse_L1_reciprocal_polsby_popper,
                               Validator, no_vanishing_districts,
                               refuse_new_splits, single_flip_contiguous,
                               within_percent_of_ideal_population,
                               fast_connected)

from rundmcmc.scores import (efficiency_gap, mean_median,
                             mean_thirdian)

from rundmcmc.run import (pipe_to_table,
                          handle_scores_separately)

from rundmcmc.output import p_value_report

from vis_output import (hist_of_table_scores, trace_of_table_scores)



#Input the path to the graph (either JSON or shapefile) and the label column 
graph_path = "./testData/PA_graph_with_data.json"
unique_label = "wes_id"


#Names of graph columns go here
pop_col = "POP100"
area_col = "ALAND10"
district_col = "CD"


#This builds a graph
graph = construct_graph(graph_path)
assignment = dict(zip(graph.nodes(), [graph.node[x][district_col] for x in graph.nodes()]))

#Write graph to file

#Input the shapefile with vote data here
vote_path = "./testData/wes_merged_data.shp"


#This inputs a shapefile with columns you want to add
df = gp.read_file(vote_path)


#Names of shapefile data columns go here
vote_col1 = "voteA"
vote_col2 = "voteB"

#This adds the data to the graph
data_list=[vote_col1, vote_col2]

add_data_to_graph(df, graph, data_list, id_col=unique_label)



#Desired proposal method
proposal_method = propose_random_flip_no_loops


#Desired proposal method
acceptance_method = always_accept#cut_edge_accept


#Number of steps to run
steps=1000

print("loaded data")


#Necessary updaters go here
updaters = {
            **votes_updaters([vote_col1, vote_col2]),
            'population': Tally(pop_col, alias='population'),
            'perimeters': perimeters,
            'exterior_boundaries': exterior_boundaries,
            'interior_boundaries': interior_boundaries,
            'boundary_nodes': boundary_nodes,
            'cut_edges': cut_edges,
            'areas': Tally(area_col, alias='areas'),
            'polsby_popper': polsby_popper,
            'cut_edges_by_part': cut_edges_by_part,
            }

#This builds the partition object
initial_partition = Partition(graph, assignment, updaters)


#Desired validators go here
pop_limit =.01
population_constraint = within_percent_of_ideal_population(initial_partition, pop_limit)

compactness_limit = 1.01 * L1_reciprocal_polsby_popper(initial_partition)
compactness_constraint = UpperBound(L1_reciprocal_polsby_popper, compactness_limit)



validator = Validator([refuse_new_splits, no_vanishing_districts,
                       single_flip_contiguous, population_constraint,
                       compactness_constraint])


#Add cyclic updaters :(
#updaters['metagraph_degree'] = MetagraphDegree(validator, "metagraph_degree")

#This builds the partition object (again) :(
#initial_partition = Partition(graph, assignment, updaters)


print("setup chain")

#This builds the chain object for us to iterate over
chain = MarkovChain(proposal_method, validator, acceptance_method,
                  initial_partition, total_steps=steps)

print("ran chain")

#Post processing commands go below:

scores = {
        'Mean-Median': functools.partial(mean_median, proportion_column_name=vote_col1+"%"),
        'Mean-Thirdian': functools.partial(mean_thirdian, proportion_column_name=vote_col1+"%"),
        'Efficiency Gap': functools.partial(efficiency_gap, col1=vote_col1, col2=vote_col2),
        'L1 Reciprocal Polsby-Popper': L1_reciprocal_polsby_popper
    }

initial_scores = {key: score(initial_partition) for key, score in scores.items()}

table = pipe_to_table(chain, scores, display = True, display_frequency = 10,
                      bin_frequency = 1)


#Histogram Plotting
hist_path = "chain_histogram.png"

hist_of_table_scores(table, scores, outputFile = hist_path, num_bins = 50)

print("plotted histograms")


#Trace Plotting
trace_path = "chain_traces.png"

trace_of_table_scores(table, scores, outputFile = trace_path)

print("plotted traces")

#P-value reports
pv_dict={key: p_value_report(key, table[key], initial_scores[key]) for key in scores}
print(pv_dict)
with open('pvals_report.json', 'w') as fp:
    json.dump(pv_dict, fp)

print("computed p-values")


#Write flips to file

with open('chain_flips.json', 'w') as fp:
    json.dump(initial_partition.flips, fp)


print("wrote flips")

