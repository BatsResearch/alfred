from typing import List
from ..query import Query


def batch_multimodal(queries: List[Query], mode: str, batch_size=64):
    """
    Batch RankedQueries with Multimodal Payloads

    :param queries: A list of multimodal queries
    :type queries: List[Query]
    :param mode: The mode of the multimodal query ("autoregressive", "contrastive")
    :type mode: str
    :param batch_size: The batch size
    :type batch_size: int
    :return: A list of batches of multimodal ranked queries
    :rtype: List[List[Query]]
    """
    if mode == "contrastive":
        candidates = queries[0].candidates
        batches = []
        batch = []
        for query in queries:
            if len(batch) == batch_size:
                batches.append((batch, candidates))
                batch = []
            batch.append(query.prompt)
        if len(batch) > 0:
            batches.append((batch, candidates))
    elif mode == "autoregressive":
        batches = []
        batch = []
        for query in queries:
            if len(batch) == batch_size:
                batches.append(batch)
                batch = []
            if isinstance(query, Query):
                batch.append(query.prompt)
            else:
                batch.append(query)
        if len(batch) > 0:
            batches.append(batch)
    else:
        raise ValueError(f"Unknown multimodal mode {mode}")
    return batches
