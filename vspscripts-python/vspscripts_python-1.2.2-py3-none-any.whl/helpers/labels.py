#!/usr/bin/python
#
# Cityscapes labels
#

from __future__ import print_function, absolute_import, division
from collections import namedtuple


#--------------------------------------------------------------------------------
# Definitions
#--------------------------------------------------------------------------------

# a label and all meta information
Label = namedtuple( 'Label' , [

    'name'        , # The identifier of this label, e.g. 'car', 'person', ... .
                    # We use them to uniquely name a class

    'id'          , # An integer ID that is associated with this label.
                    # The IDs are used to represent the label in ground truth images
                    # An ID of -1 means that this label does not have an ID and thus
                    # is ignored when creating ground truth images (e.g. license plate).
                    # Do not modify these IDs, since exactly these IDs are expected by the
                    # evaluation server.

    'trainId'     , # Feel free to modify these IDs as suitable for your method. Then create
                    # ground truth images with train IDs, using the tools provided in the
                    # 'preparation' folder. However, make sure to validate or submit results
                    # to our evaluation server using the regular IDs above!
                    # For trainIds, multiple labels might have the same ID. Then, these labels
                    # are mapped to the same class in the ground truth images. For the inverse
                    # mapping, we use the label that is defined first in the list below.
                    # For example, mapping all void-type classes to the same ID in training,
                    # might make sense for some approaches.
                    # Max value is 255!

    'category'    , # The name of the category that this label belongs to

    'categoryId'  , # The ID of this category. Used to create ground truth images
                    # on category level.

    'hasInstances', # Whether this label distinguishes between single instances or not

    'ignoreInEval', # Whether pixels having this class as ground truth label are ignored
                    # during evaluations or not

    'color'       , # The color of this label
    ] )


#--------------------------------------------------------------------------------
# A list of all labels
#--------------------------------------------------------------------------------

# Please adapt the train IDs as appropriate for your approach.
# Note that you might want to ignore labels with ID 255 during training.
# Further note that the current train IDs are only a suggestion. You can use whatever you like.
# Make sure to provide your results using the original IDs and not the training IDs.
# Note that many IDs are ignored in evaluation and thus you never need to predict these!

labels = [
    #       name                     id    trainId   category            catId     hasInstances   ignoreInEval   color
    Label(  'unlabeled'            ,  0 ,      255 , 'void'            , 0       , False        , True         , (  0,  0,  0) ),
    Label(  'out of roi'           ,  1 ,      255 , 'void'            , 0       , False        , True         , (  0,  0,  0) ),
    Label(  'background'           ,  2 ,        0 , 'background'      , 0       , False        , True         , (  0,  0,  0) ),
    Label(  'copper'               ,  3 ,        6 , 'copper'          , 1       , True         , False        , (111, 74,  0) ),
    Label(  'drill_break'          ,  4 ,        0 , 'drill'           , 2       , True         , False        , ( 81,  0, 81) ),
    Label(  'drill_nick_in'        ,  5 ,        0 , 'drill'           , 2       , True         , False        , (128, 64,128) ),
    Label(  'drill_nick_out'       ,  6 ,        0 , 'drill'           , 2       , True         , False        , (244, 35,232) ),
    Label(  'drill_protru_out'     ,  7 ,        0 , 'drill'           , 2       , True         , False        , (250,170,160) ),
    Label(  'island'               ,  8 ,        1 , 'island'          , 3       , True         , False        , (230,150,140) ),
    Label(  'nick'                 ,  9 ,        2 , 'nick'            , 4       , True         , False        , ( 70, 70, 70) ),
    Label(  'open'                 , 10 ,        3 , 'open'            , 5       , True         , False        , (102,102,156) ),
    Label(  'pad'                  , 11 ,        0 , 'pad'             , 6       , True         , False        , (190,153,153) ),
    Label(  'pinhole'              , 12 ,        7 , 'pinhole'         , 7       , True         , False        , (180,165,180) ),
    Label(  'protrusion'           , 13 ,        4 , 'protrusion'      , 8       , True         , False        , (150,100,100) ),
    Label(  'short'                , 14 ,        5 , 'short'           , 9       , True         , False        , (150,120, 90) ),
    Label(  'drill_protru_in'      , 15 ,        0 , 'drill'           , 2       , True         , False        , (153,153,153) ),
    Label(  'drill_open'           , 16 ,        0 , 'drill'           , 2       , True         , False        , (250,170, 30) ),
]


#--------------------------------------------------------------------------------
# Create dictionaries for a fast lookup
#--------------------------------------------------------------------------------

# Please refer to the main method below for example usages!

# name to label object
name2label      = { label.name    : label for label in labels           }
# id to label object
id2label        = { label.id      : label for label in labels           }
# trainId to label object
trainId2label   = { label.trainId : label for label in reversed(labels) }
# category to list of label objects
category2labels = {}
for label in labels:
    category = label.category
    if category in category2labels:
        category2labels[category].append(label)
    else:
        category2labels[category] = [label]

#--------------------------------------------------------------------------------
# Assure single instance name
#--------------------------------------------------------------------------------

# returns the label name that describes a single instance (if possible)
# e.g.     input     |   output
#        ----------------------
#          car       |   car
#          cargroup  |   car
#          foo       |   None
#          foogroup  |   None
#          skygroup  |   None
def assureSingleInstanceName( name ):
    # if the name is known, it is not a group
    if name in name2label:
        return name
    # test if the name actually denotes a group
    if not name.endswith("group"):
        return None
    # remove group
    name = name[:-len("group")]
    # test if the new name exists
    if not name in name2label:
        return None
    # test if the new name denotes a label that actually has instances
    if not name2label[name].hasInstances:
        return None
    # all good then
    return name

#--------------------------------------------------------------------------------
# Main for testing
#--------------------------------------------------------------------------------

# just a dummy main
if __name__ == "__main__":
    # Print all the labels
    print("List of vsp labels:")
    print("")
    print("    {:>21} | {:>3} | {:>7} | {:>14} | {:>10} | {:>12} | {:>12}".format( 'name', 'id', 'trainId', 'category', 'categoryId', 'hasInstances', 'ignoreInEval' ))
    print("    " + ('-' * 98))
    for label in labels:
        print("    {:>21} | {:>3} | {:>7} | {:>14} | {:>10} | {:>12} | {:>12}".format( label.name, label.id, label.trainId, label.category, label.categoryId, label.hasInstances, label.ignoreInEval ))
    print("")

    print("Example usages:")

    # Map from name to label
    name = 'short'
    id   = name2label[name].id
    trainId = name2label[name].trainId
    print("ID of label '{name}': {id}".format( name=name, id=id ))
    print("trainId of label '{name}': {trainId}".format( name=name, trainId=trainId ))

    # Map from ID to label
    category = id2label[id].category
    print("Category of label with ID '{id}': {category}".format( id=id, category=category ))

    # Map from trainID to label
    trainId = 0
    name = trainId2label[trainId].name
    print("Name of label with trainID '{id}': {name}".format( id=trainId, name=name ))
