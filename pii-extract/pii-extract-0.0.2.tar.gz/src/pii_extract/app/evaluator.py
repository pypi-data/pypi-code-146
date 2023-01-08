"""
 * get a folder (in the future, maybe also a Web folder, or a Dataset)
 * get a Ground Truth JSON, with a mapping
      {"language": ["filename": {[<list of PII for that file>]}]}
 * for each language
     - for each filename
           for each configured/available PII:
             - run a PiiManager for the language and with *only* that PII active
             - collect metrics
                 precision
                 recall
                 by-token accuracy
https://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/
cf. SemEval
 * build an evaluation JSON file
"""
