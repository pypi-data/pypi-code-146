from label_flatten import Tree
import copy

pth = "labor_theme.json"
labels = ["劳动事件"]


tree_template = Tree(pth)
for label in labels:
    # label
    new_tree = copy.deepcopy(tree_template)
    labeled_tree = new_tree.give_label(label)
    print(labeled_tree)
    sentences = labeled_tree.write(mode="all")
    for sen in sentences:
        print(sen)
    # reduce
    new_tree2 = copy.deepcopy(tree_template)
    labeled_tree = new_tree2.reduce_from_sentences(sentences)
    label = labeled_tree.deepest_label()
    print(label)