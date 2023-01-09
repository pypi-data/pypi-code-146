import spacy


def filter_irrelevant(context: str) -> str:
    # Load the NLP model
    nlp = spacy.load("en_core_web_sm")
    # Process the context
    doc = nlp(context)
    # Extract the named entities from the context
    named_entities = [entity.text for entity in doc.ents]
    # Convert the list of named entities into a single string
    named_entities_str = " ".join(named_entities)
    return str(named_entities_str)
