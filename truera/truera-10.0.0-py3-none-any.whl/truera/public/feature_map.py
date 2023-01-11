def init_default_feature_map(pre_columns, post_data):
    feature_map = {}
    if (post_data is None):
        for i, column in enumerate(pre_columns):
            feature_map[column] = [i]
    else:
        post_columns = list(post_data.columns)
        post_columns_set = set(post_columns)
        for c in pre_columns:
            if c in post_columns_set:
                feature_map[c] = [post_columns.index(c)]
            else:
                feature_map[c] = [
                    post_columns.index(s)
                    for s in post_columns
                    if s.startswith(c)
                ]
    return feature_map


def verify_feature_map(feature_map, pre_columns, post_columns):
    post_idxs_set = set()
    for c in pre_columns:
        feature_map_c = feature_map[c]
        if len(feature_map_c) > 0:
            min_feature = min(feature_map_c)
            max_feature = max(feature_map_c)
            if len(feature_map_c) != max_feature - min_feature + 1:
                # TODO: Is contiguity necessary anymore?
                raise ValueError(
                    "Feature map for {} ({}) is not contiguous".format(
                        c, feature_map_c
                    )
                )
            for f_idx in feature_map_c:
                if f_idx in post_idxs_set:
                    raise ValueError(
                        "Feature {} inferred to be mapped to {}, but is already mapped to another feature"
                        .format(f_idx, c)
                    )
                post_idxs_set.add(f_idx)
    if len(post_idxs_set) != len(post_columns):
        raise ValueError(
            "Feature map values: {} has length {} but there are {} post transform columns {}."
            .format(
                post_idxs_set, len(post_idxs_set), len(post_columns),
                post_columns
            )
        )
