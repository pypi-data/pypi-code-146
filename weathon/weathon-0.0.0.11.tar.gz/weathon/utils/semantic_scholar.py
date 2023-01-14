# -*- coding: utf-8 -*-
# @Time    : 2023/1/14 11:15
# @Author  : LiZhen
# @FileName: semantic_scholar.py
# @github  : https://github.com/Lizhen0628
# @Description:


from semanticscholar import SemanticScholar


def overlap_papers(paper_id1, paper_id2):
    ss = SemanticScholar()
    paper1 = ss.paper(paper_id1)
    paper2 = ss.paper(paper_id2)
    co_citations = list(set(x['title'] for x in paper1['citations']) & set(x['title'] for x in paper2['citations']))
    return co_citations


if __name__ == '__main__':
    print(overlap_papers('arXiv:1906.08237', 'arXiv:1907.11692'))
