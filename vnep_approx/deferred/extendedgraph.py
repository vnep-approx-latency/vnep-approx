# MIT License
#
# Copyright (c) 2016-2018 Matthias Rost, Elias Doehne, Tom Koch, Alexander Elvers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import logging

from alib import datamodel


class ExtendedGraph(datamodel.Graph):
    """ Initial extended graph construction for chain requests. Deferred. It serves no real purpose anymore.
    """

    def get_node_name(self, u, ve):
        vtail, vhead = ve
        return (u, vtail, vhead)

    def get_edge_name(self, se, ve):
        stail, shead = se
        vtail, vhead = ve
        return (stail, shead, vtail, vhead)

    def __init__(self, request, substrate):
        logger = logging.getLogger(__name__)
        logger.debug('init extended graph with substrate %s', substrate)

        super(ExtendedGraph, self).__init__(request.name)

        self.super_source = "supersource_{}".format(request.name)
        self.super_sink = "supersink_{}".format(request.name)

        # source and sink
        self.add_node(self.super_source, origin=None, layer_index=0)
        self.add_node(self.super_sink, origin=None, layer_index=len(request.edges) + 1)
        self.nodes_of_ve = {}
        # for each edges ve in request generate unique duplicate of substrate
        # graph
        for index, req_node in enumerate(request.sequence):
            nodelist = []
            if req_node == request.sequence[-1]:
                break
            if len(request.out_edges[req_node]) != 1:
                raise ValueError("Too many or too few edges")
            ve = request.out_edges[req_node][0]
            for u in substrate.nodes:
                node_name = self.get_node_name(u, ve)
                self.add_node(node_name, origin=u, layer_index=index + 1)
                nodelist.append(node_name)

            for se in substrate.edges:
                self.add_intra_edge(self.get_node_name(se[0], ve), self.get_node_name(se[1], ve), origin=(se, ve))
            self.nodes_of_ve[ve] = nodelist

        # function mapping : 1. supersource 2. internal functions 3. supersink
        # 1. supersource
        start = request.sequence[0]
        start_type = request.get_type(start)
        for u in substrate.get_nodes_by_type(start_type):
            start_allowed_nodes = request.get_allowed_nodes(start)
            if start_allowed_nodes is None or u in start_allowed_nodes:
                self.add_inter_edge(self.super_source,
                                    self.get_node_name(u, request.get_out_edge(start)),
                                    origin=(start_type, u, start))

        # 2. between nodes
        if len(request.sequence) > 2:
            for req_index in range(0, len(request.sequence) - 2):
                current = request.sequence[req_index]
                nextnode = request.sequence[req_index + 1]
                nextnode_type = request.get_type(nextnode)
                for u in substrate.get_nodes_by_type(nextnode_type):
                    nextnode_allowed_nodes = request.get_allowed_nodes(nextnode)
                    if nextnode_allowed_nodes is None or u in nextnode_allowed_nodes:
                        self.add_inter_edge(self.get_node_name(u, request.get_out_edge(current)),
                                            self.get_node_name(u, request.get_out_edge(nextnode)),
                                            origin=(nextnode_type, u, nextnode))
        # 3. supersink
        end = request.sequence[len(request.sequence) - 1]
        before_end = request.sequence[len(request.sequence) - 2]
        end_type = request.get_type(end)
        for u in substrate.get_nodes_by_type(end_type):
            end_allowed_nodes = request.get_allowed_nodes(end)
            if end_allowed_nodes is None or u in end_allowed_nodes:
                self.add_inter_edge(self.get_node_name(u, request.get_out_edge(before_end)),
                                    self.super_sink,
                                    origin=(end_type, u, end))

    def add_node(self, u, origin, layer_index):
        super(ExtendedGraph, self).add_node(u, origin=origin, layer_index=layer_index)

    def add_intra_edge(self, tail, head, origin):
        super(self.__class__, self).add_edge(tail, head, edge_origin=origin)

    def add_inter_edge(self, tail, head, origin):
        super(self.__class__, self).add_edge(tail, head, node_origin=origin)

    def __str__(self):
        return super(ExtendedGraph, self).__str__()
