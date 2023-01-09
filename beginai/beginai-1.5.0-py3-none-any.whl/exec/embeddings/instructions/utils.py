def sequence_encoder(categories_list):
    """
    get a numerical code for each category.
    """
    categories_list = sorted(categories_list)
    return list(range(1, len(categories_list) + 1))


def sort_instructions(data) -> dict:
    if len(data) == 0:
        return {}

    sorted_dictionary = {}
    instructions = data.get("instructions", {})
    embedding_template = data.get("embedding_template", {})

    for object_key, object_instructions in instructions.items():
        sorted_dictionary[object_key] = []

        # Check if it has an entry in the embedding template
        if object_key in embedding_template:
            # Loop through the embedding template entries
            for object_instruction_key in embedding_template[object_key]:
                # Extract chained as a single instruction
                if object_instruction_key.startswith("chain_instruction"):
                    object_instruction_key = object_instruction_key.split("__")[
                        3]

                    instruction = list(
                        filter(lambda x: x["f_id"] == object_instruction_key and x.get("_chains"), object_instructions))[0]
                else:
                    instruction = list(filter(lambda x: x["f_id"] == object_instruction_key and not x.get(
                        "_chains", None), object_instructions))[0]

                if instruction not in sorted_dictionary[object_key]:
                    sorted_dictionary[object_key].append(
                        instruction)
        elif object_key == "interactions":
            sorted_dictionary[object_key] = object_instructions
    return sorted_dictionary
