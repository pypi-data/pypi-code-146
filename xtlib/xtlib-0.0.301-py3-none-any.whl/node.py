# node.py: implements the node_tree class (from TPX-Transformer repo)
import sys, os

def text_tree_to_node(tokens):
    prev_c = None
    stack = []
    parent = None
    
    for c in tokens:
        if prev_c == '(':
            parent = Node(label=c, children=[])
            stack.append(parent) 
        elif c == ')':
            child = parent 
            stack.pop()
            if len(stack) > 0:
                parent = stack[-1]
                parent.children.append(child)
        elif c != '(':
            parent.children.append(Node(c, children=[]))
        prev_c = c

    return parent
        
class Node:
    def __init__(self, label, children=None, key=None):
        self.label = label
        self.key = key
        self.children = children if children else []
        self.forced_child = False
        self.reconstruct_calls = 0
        self.exceeded_max_reconstruct_calls = False

    def get_draw_rep(self):
        rep = [self.label] + [child.get_draw_rep() if isinstance(child, Node) else child for child in self.children]
        return rep

    def get_max_depth(self):
        max_child_depth = 0

        for child in self.children:
            max_child_depth = max(max_child_depth, child.get_max_depth())

        return 1 + max_child_depth

    def get_max_branching(self):
        max_branching = 1

        if self.children:
            max_branching = len(self.children)

            for child in self.children:
                max_branching = max(max_branching, child.get_max_branching())

        return max_branching

    def get_num_nodes(self):
        node_count = 1

        for child in self.children:
            node_count += child.get_num_nodes()

        return node_count

    def node_at_index(self, index, node_index=0, parent=None):
        '''
        Processing:
            find the node with the specified index, determined by 
            visiting the nodes in depth-first order.
        '''
        if node_index == index:
            return self, parent

        child_index = 1 + node_index

        for i, child in enumerate(self.children):
            node, node_parent = child.node_at_index(index, child_index, self)
            if node is not None:
                return node, node_parent

            child_index += child.get_num_nodes()

        return None, None     # not found

    def draw(self, show_in_browser=False):
        if show_in_browser:
            import svgling

            rep = self.get_draw_rep()       
            value = svgling.draw_tree(rep, leaf_padding=4)
            svg_text = value.get_svg().tostring()
            
            # save to file 
            fn = "test.svg"
            with open(fn, "wt") as outfile:
                outfile.write(svg_text)

            # display in browser (close window when done viewing to continue)
            import os
            os.system(fn)
        else:
            #return svgling.draw_tree(self.rep, leaf_padding=4)
            pass
    
    def __repr__(self, root_format=False, show_key=True, max_len=None, depth=0, add_parens=True):

        label_key = self.label

        if show_key and self.key:
            label_key += ":" + self.key

        if self.children:
            child_rep = ""

            for c, child in enumerate(self.children):

                flat_child = len(child.children) == 0
                child_text = child.__repr__(root_format, depth=depth+1, add_parens=(not flat_child), show_key=show_key)

                if max_len and depth==0 and len(child_text) > max_len:
                    child_text = child_text[0:max_len] + "..."

                if root_format and depth==0:
                    force_flag = "*" if child.forced_child else ""
                    exceed_flag = "#" if child.exceeded_max_reconstruct_calls else ""
                    child_rep += "\n  [{}{}{}]: {}".format(c, force_flag, exceed_flag, child_text)
                else:
                    if c:
                        child_rep += " " + child_text
                    else:
                        child_rep += child_text

            # if flat_children:
            #     child_rep = "( {} )".format(child_rep)

            if root_format and depth==0:
                rep = "root: {}{}".format(label_key, child_rep)
            else:
                rep = "{} {}".format(label_key, child_rep)

        else:
            # simple node without children
            rep = label_key

        if add_parens:
            rep = "( {} )".format(rep)

        return rep
    
    def __str__(self):
        return self.__repr__()

    def str(self, root_format=False, show_key=True, max_len=0):
        return self.__repr__(root_format, show_key, max_len)


def test():
    '''
    NC team text tree conventions:
        ( A ) ==> parent A
        ( A B ) ==> parent A with child B
        ( A B C ) ==> parent A with children B and C
        ( A ( B C) ) ==> parent A with child B (B has child C)
    '''

    def check(node, text):
        assert str(node) == text
        nx = text_tree_to_node(text)
        assert str(nx) == text

    node = Node("A")
    check(node, "( A )")

    node = Node("A", children=[Node("B")])
    check(node, "( A B )")

    node = Node("A", children=[Node("B")])
    check(node, "( A B )")

    node = Node("A", children=[Node("B"), Node("C")])
    check(node, "( A B C )")

    node = Node("A", children=[Node("B"), Node("C", children=[Node("D")])])
    check(node, "( A B ( C D ) )")

    nodeb = Node("B", children=[Node("C")])
    noded = Node("D", children=[Node("E")])
    node = Node("A", children=[nodeb, noded])
    check(node, "( A ( B C ) ( D E ) )")

    tree_text = "( NP ( DET our ) ( AP ( N car ) ) )"
    node = text_tree_to_node(tree_text)
    assert str(node) == tree_text

    tree_text = '( S ( NP ( DET our ) ( AP ( N car ) ) ) ( VP ( V collided ) ( NP ( DET her ) ( AP ( N child ) ) ) ) )'
    node = text_tree_to_node(tree_text)
    assert str(node) == tree_text

    print("Node tests passed")

if __name__ == "__main__":
    test()
