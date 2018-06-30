import random
import networkx


def propose_random_flip(partition):
    """Proposes a random boundary flip from the partition.

    :partition: The current partition to propose a flip from.
    :returns: a dictionary with the flipped node mapped to its new assignment

    """
    edge = random.choice(tuple(partition['cut_edges']))
    index = random.choice((0, 1))

    flipped_node, other_node = edge[index], edge[1 - index]

    flip = {flipped_node: partition.assignment[other_node]}

    # self loop
    numEdges = 2.0 * len(partition['cut_edges'])
    if random.random() < 1.0 - (numEdges * 1.0 / partition.max_edge_cuts):
        flip = dict()

    # checks for a frozen nodes field and self loops if the value has
    # been set to 1
    if bool(networkx.get_node_attributes(partition.graph, 'Frozen')) and bool(flip.keys()):
        if bool(partition.graph.node[str(list(flip.keys())[0])]['Frozen']):
            flip = dict()
    return flip


def propose_several_random_flips(partition):
    """Proposes between 2 and 7 random boundary flips from the partition.
       Calls the propose_random_flip() method from this file.

    :partition: The current partition to propose a flip from.
    :returns: a dictionary with the flipped nodes mapped to their new assignments

    """
    number_of_flips = random.randint(2, 7)

    proposal = dict()

    for i in range(number_of_flips):
        proposal.update(propose_random_flip(partition))

    return proposal


def propose_flip_every_district(partition):
    """Proposes a random boundary flip for each district in the partition.

    :partition: The current partition to propose a flip from.
    :returns: a dictionary with the flipped nodes mapped to their new assignments

    """
    proposal = dict()

    for dist_edges in partition['cut_edges_by_part'].values():
        edge = random.choice(list(dist_edges))

        index = random.choice((0, 1))
        flipped_node, other_node = edge[index], edge[1 - index]
        flip = {flipped_node: partition.assignment[other_node]}

        proposal.update(flip)

    return proposal


def propose_chunk_flip(partition):
    """Chooses a random boundary node and proposes to flip it and all of its neighbors

    :partition: The current partition to propose a flip from.
    :returns: a dictionary with the flipped nodes mapped to their new assignments

    """
    proposal = dict()

    edge = random.choice(tuple(partition['cut_edges']))
    index = random.choice((0, 1))

    flipped_node = edge[index]

    valid_flips = [nbr for nbr in partition.graph.neighbors(
        flipped_node) if partition.assignment[nbr] != partition.assignment[flipped_node]]

    for flipped_neighbor in valid_flips:
        proposal.update({flipped_neighbor: partition.assignment[flipped_node]})

    return proposal


def propose_flip_every_edge_of_district(partition):
    """Chooses a random district to manipulate. Each edge on the boundary is
       incident to a node in this district and a node outside of it. For each
       edge, toss a fair coin. If tails, do nothing. If heads, toss a second
       fair coin. If heads, add the node outside of this district to it. If
       tails, add the node inside of this district to the other one.

    :partition: The current partition to propose a flip from.
    :returns: a dictionary with the flipped nodes mapped to their new assignments

    """
    proposal = dict()

    edges = random.choice(list(partition['cut_edges_by_part'].values()))

    for edge in edges:
        if(random.random() > .5):
            index = random.choice((0, 1))
            flipped_node, other_node = edge[index], edge[1 - index]
            proposal.update({flipped_node: partition.assignment[other_node]})

    return proposal


def propose_single_or_chunk(partition):
    """With probability .9, chooses a random boundary node and proposes to flip it.
       With probability .1, chooses a random boundary node and proposes to flip it
       and all of its neighbors.
       Calls the propose_random_flip() and propose_chunk_flip()
       methods from this file.


    :partition: The current partition to propose a flip from.
    :returns: a dictionary with the flipped nodes mapped to their new assignments

    """
    if(random.random() > .1):
        return propose_random_flip(partition)
    else:
        return propose_chunk_flip(partition)


def number_of_flips(partition, dict_of_flips, prev_partition):
    flips = partition.flips
    if flips is None or flips is prev_partition:
        return dict_of_flips, prev_partition
    else:
        prev_partition = flips
        dict_of_flips[next(iter(flips))] = dict_of_flips.get(next(iter(flips)), 0) + 1
        return dict_of_flips, prev_partition
