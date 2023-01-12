# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


class RowCountsForClassificationRegression:

    ForValidation = 100000
    ForPostFeaturizationSteps = 50000  # used for model-explain, model-test etc
    ForSuggestion = 10000
    ForFakeFitTransform = 20
