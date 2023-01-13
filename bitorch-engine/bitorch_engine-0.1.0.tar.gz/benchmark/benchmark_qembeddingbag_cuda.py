import torch
from bitorch.layers.qembedding import QEmbeddingBag as bitorch_qembag
from bitorch.quantizations import Sign
from torch.profiler import profile, record_function, ProfilerActivity

import os, sys

from benchmark.util import get_cuda_benchmark_device

sys.path.insert(0, os.getcwd())
from bitorch_engine.layers.qembedding import QEmbeddingBag as engine_qembag


def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)


def qembeddingbag_cuda_benchmarking(vocab_size, embedding_size, input_l):
    # pass if not cuda ready
    if not torch.cuda.is_available(): return
    print("vocab size:{}, embedding dim:{}, input length:{}.".format(vocab_size, embedding_size, input_l))

    num_runs = 1000


    input = torch.randint(0, vocab_size - 1, (vocab_size,))
    example_offset = torch.tensor((0,), dtype=int)

    # to gpu
    device = get_cuda_benchmark_device()
    input_cuda = to_device(input, device)
    example_offset_cuda = to_device(example_offset, device)

    qembeddingbag = bitorch_qembag(num_embeddings=vocab_size, embedding_dim=embedding_size,
                                   weight_quantization=Sign(),
                                   output_quantization=Sign(), sparse=False, mode="mean")
    qembeddingbag.to(device)

    # warm-up
    for i in range(num_runs):
        output_bitorch_qembeddingbag = qembeddingbag(input_cuda, example_offset_cuda)

    # set stream
    stream = torch.cuda.current_stream(device=device)
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    start.record(stream=stream)
    # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    for i in range(num_runs):
        output_bitorch_qembeddingbag = qembeddingbag(input_cuda, example_offset_cuda)
    # print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    end.record(stream=stream)
    torch.cuda.synchronize()
    dot_time = start.elapsed_time(end)/1000/num_runs
    print("bitorch binary qEmd CUDA run time:\t%.6f s" % (dot_time))


    # QEmbeddingBag of inference engine
    engine_qembeddingbag = engine_qembag(num_embeddings=vocab_size, embedding_dim=embedding_size,
                                         _weight=qembeddingbag.weight)
    engine_qembeddingbag.to(device)

    start.record(stream=stream)
    # with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    for i in range(num_runs):
        output_engine_qembeddingbag = engine_qembeddingbag(input_cuda)
    # print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    end.record(stream=stream)
    torch.cuda.synchronize()
    rt = start.elapsed_time(end)/1000/num_runs
    print("bitorch engine binary qEmd CUDA run time:\t{:.6f} s, {:.2f} times speedup".format(rt, dot_time/rt))
        


TEST_DATA = [
    #dict size, emb_dim, input_length
    (10, 10, 10),
    (100, 10, 100),
    (1000, 100, 1000),
    (5000, 500, 5000),
    (10000, 1024, 10000),
    (100000, 128, 100000),
    # BERT
    (30522, 768, 64),
    (30522, 768, 128),
    (30522, 768, 256),
    (30522, 768, 512),
]



if __name__ == '__main__':
    for config in TEST_DATA:
        qembeddingbag_cuda_benchmarking(config[0], config[1], config[2])
