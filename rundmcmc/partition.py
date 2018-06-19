import random


def propose_random_flip(partition):
    """Proposes a random boundary flip from the partition.

    :partition: The current partition to propose a flip from.
    :returns: a dictionary of with the flipped node mapped to its new assignment

    """
    edge = random.choice(tuple(partition['cut_edges']))
    index = random.choice((0, 1))

    flipped_node, other_node = edge[index], edge[1 - index]
    flip = {flipped_node: partition.assignment[other_node]}

    return flip


class Partition:
    """
    Partition represents a partition of the nodes of the graph. It will perform
    the first layer of computations at each step in the Markov chain - basic
    aggregations and calculations that we want to optimize.

    """

    def __init__(self, graph, assignment, updaters=None, fields=None):
        """
        :graph: NetworkX graph.
        :assignment: Dictionary mapping node ids to their partition cell.

        """
        self.graph = graph
        self.assignment = assignment

        if not updaters:
            updaters = dict()
        self.updaters = updaters

        if not fields:
            fields = {key: updater(self) for key, updater in self.updaters.items()}
        self.fields = fields

    def __str__(self):
        fields_str = "\n".join(
            f"{key}: " + ", ".join(str(value) for value in self.fields[key]) for key in self.fields)
        return f"Partition\n{fields_str}"

    def merge(self, flips):
        """
        Takes a dictionary of new assignments and returns the Partition
        obtained by applying these new assignments to this instance (self) of
        Partition.

        :flips: a dictionary of nodes mapped to their new assignments
        :returns: a new Partition instance

        """
        new_assignment = {**self.assignment, **flips}

        new_fields = {key: updater(self, new_assignment, flips)
                      for key, updater in self.updaters.items()}

        return Partition(self.graph, assignment=new_assignment,
                         updaters=self.updaters, fields=new_fields)

    def __getitem__(self, key):
        """Allows keying on a Partition instance.
        :key: Property to access.
        """
        return self.fields[key]

    def keys(self):
        """Implementation of the Python dict's keys() method."""
        return self.fields.keys()

    def items(self):
        """Implementation of the Python dict's items() method."""
        return self.fields.items()
