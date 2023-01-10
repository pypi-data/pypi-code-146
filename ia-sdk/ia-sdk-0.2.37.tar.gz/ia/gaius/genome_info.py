try:
    from cyjupyter import Cytoscape
except:
    class Cytoscape:
        def __init__(*args, **kwargs):
            pass


class Genome:
    def __init__(self, topology: dict):
        """Initialize a genome from a GAIuS agent topology (dict)

        Args:
            topology (dict, required): GAIuS agent topology
        """
        self.topology = topology
        self.agent = self.topology['agent']
        self.description = self.topology['description']
        ## Not everyone will have style information, so wrap this:
        try:
            self.style_obj = self.topology['style']
            self.style_obj[1]['style']['curve-style'] = 'bezier'
        except:
            pass
        #        self.agent_genome = self.topology['elements']['nodes']
        self.primitives = {}
        self.manipulatives = {}
        self.action_ids = []
        self.actions_manifests = {}
        for node in self.topology['elements']['nodes']:
            if node['data']['type'] == 'primitive':
                self.primitives[node['data']['id']] = node['data']
            elif node['data']['type'] == 'manipulative':
                self.manipulatives[node['data']['id']] = node['data']
                if node['data']['name'].startswith("ACTION"):
                    self.action_ids.append(node['data']['id'])
                    if node['data']['primitive'] in self.actions_manifests:
                        self.actions_manifests[node['data']['primitive']].append(node['data'])
                    else:
                        self.actions_manifests[node['data']['primitive']] = [node['data']]
        self.agent_genome = {'primitives': self.primitives, 'manipulatives': self.manipulatives}
        self.primitive_map = {x['name']: _id for _id, x in self.primitives.items()}
        self.manipulative_map = {_id: x['name'] for _id, x in self.manipulatives.items()}
        # print(" %s total primitives" % (len(self.primitives)))
        # print(" %s total manipulatives" % (len(self.manipulatives)))
        # print(" %s total actions" % (len(self.actions_manifests)))
        return

    def get_nodes(self):
        return self.agent_genome['primitives'], self.agent_genome['manipulatives']

    def get_actions(self):
        """Return a list of ACTIONs in the topology

        .. warning::
            .. deprecated:: 12.0 (Kehl)

                ACTIONs are not actively used in GAIuS topology creation
        """
        return self.action_ids

    def get_primitive_map(self):
        """Get a map of the node names to node ids in the GAIuS agent topology

        Example:
            .. code-block:: python
            
                >>> agent = AgentClient(agent_info)
                >>> agent.connect()
                >>> agent.genome.get_primitive_map()
                {'P1': 'p46b6b076c'}
        """
        return self.primitive_map

    def get_manipulative_map(self):
        """Get a map of the manipulatives connected to each primitive node in the GAIuS agent topology

        Returns:
            dict: dictionary of manipulatives mappings in the topology
        """
        return self.manipulative_map

    def change_genes(self, p_id, gene_data):
        """Change the genes of a primitive in the Genome's cache

        Args:
            p_id (str): primitive id of the node to edit
            gene_data (dict): dictionary of genes to update in the Genome's cache
        """
        for key, value in gene_data.items():
            self.agent_genome['primitives'][p_id][key] = value
        return

    def display(self):
        """Display the Genome topology in Cytoscape
        """
        return Cytoscape(data=self.topology, visual_style=self.style_obj, layout={'height': '500px'},
                         background='white')

