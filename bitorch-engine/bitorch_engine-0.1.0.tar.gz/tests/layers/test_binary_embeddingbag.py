import pytest
import torch
import time
from bitorch.layers.qembedding import QEmbeddingBag as bitorch_qembag
from bitorch.quantizations import Sign
from bitorch_engine.layers.qembedding import QEmbeddingBag as engine_qembag
from tests.layers.util import get_cuda_test_device

if torch.cuda.is_available():
    from bitorch_engine.layers.qembedding.binary.cuda import BCompressedEmbeddingBagCuda

"""
    Test binary EmbeddingBag layers
"""

def to_device(data: torch.Tensor, device: torch.device) -> torch.Tensor:
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device)

TEST_INPUT_DATA = [
    (64, 10),
    (128, 10),
    (1024, 100),
    (5120, 500),
    (10240, 1024),
]

@pytest.mark.parametrize("vocab_size, embedding_size", TEST_INPUT_DATA)
def test_cpu(vocab_size, embedding_size):
    print("vocab size:{}, embedding dim:{}".format(vocab_size, embedding_size))
    num_runs = 1000

    qembeddingbag = bitorch_qembag(num_embeddings=vocab_size, embedding_dim=embedding_size,
                                  weight_quantization=Sign(),
                                  output_quantization=Sign(), sparse=False, mode="mean")

    input = torch.randint(0, vocab_size-1, (vocab_size, ))
    example_offset = torch.tensor((0, ), dtype=int)


    start_time = time.time()
    for i in range(num_runs):
        output_bitorch_qembeddingbag = qembeddingbag(input, example_offset)
    time_engine = time.time() - start_time
    # print(output_bitorch_qembeddingbag)
    print("bitorch binary qEmd run time: %.6f s" % (time_engine/num_runs))
    s_w = qembeddingbag.embedding_weight_quantization(qembeddingbag.weight)

    # QEmbeddingBag of inference engine
    engine_qembeddingbag = engine_qembag(num_embeddings=vocab_size, embedding_dim=embedding_size,
                                         _weight=s_w)
    start_time = time.time()
    for i in range(num_runs):
        output_engine_qembeddingbag = engine_qembeddingbag(input)
    time_engine = time.time() - start_time
    # print(output_engine_qembeddingbag)
    print("bitorch engine binary qEmd run time: %.6f s" % (time_engine / num_runs))
    assert torch.equal(output_bitorch_qembeddingbag, output_engine_qembeddingbag)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("vocab_size, embedding_size", TEST_INPUT_DATA)
def test_gpu(vocab_size, embedding_size):
    print("vocab size:{}, embedding dim:{}".format(vocab_size, embedding_size))
    num_runs = 1000
    input = torch.randint(0, vocab_size - 1, (vocab_size,))
    example_offset = torch.tensor((0,), dtype=int)

    # to gpu
    device = get_cuda_test_device()
    input_cuda = to_device(input, device)
    example_offset_cuda = to_device(example_offset, device)

    qembeddingbag = bitorch_qembag(num_embeddings=vocab_size, embedding_dim=embedding_size,
                                   weight_quantization=Sign(),
                                   output_quantization=Sign(), sparse=False, mode="mean")
    qembeddingbag.to(device)
    start_time = time.time()
    for i in range(num_runs):
        output_bitorch_qembeddingbag = qembeddingbag(input_cuda, example_offset_cuda)
    torch.cuda.synchronize()
    time_engine = time.time() - start_time
    # print(output_bitorch_qembeddingbag)
    print("bitorch binary qEmd CUDA run time: %.6f s" % (time_engine / num_runs))

    # QEmbeddingBag of inference engine
    engine_qembeddingbag = engine_qembag(num_embeddings=vocab_size, embedding_dim=embedding_size,
                                         _weight=qembeddingbag.weight)
    engine_qembeddingbag.to(device)
    start_time = time.time()
    for i in range(num_runs):
        output_engine_qembeddingbag = engine_qembeddingbag(input_cuda)
    torch.cuda.synchronize()
    time_engine = time.time() - start_time
    # print(output_engine_qembeddingbag)
    print("bitorch engine binary qEmd CUDA run time: %.6f s" % (time_engine / num_runs))
    assert torch.equal(output_bitorch_qembeddingbag, output_engine_qembeddingbag)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available, skipping CUDA-related test")
@pytest.mark.parametrize("vocab_size, embedding_size", TEST_INPUT_DATA)
def test_bcompressed_embedding_bag_gpu(vocab_size, embedding_size):
    print("vocab size:{}, embedding dim:{}".format(vocab_size, embedding_size))
    num_runs = 1
    input = torch.randint(0, vocab_size - 1, (vocab_size,))
    example_offset = torch.tensor((0,), dtype=int)

    # to gpu
    device = get_cuda_test_device()
    input_cuda = to_device(input, device)
    example_offset_cuda = to_device(example_offset, device)

    qembeddingbag = bitorch_qembag(num_embeddings=vocab_size, embedding_dim=embedding_size,
                                   weight_quantization=Sign(),
                                   output_quantization=Sign(), sparse=False, mode="mean")
    qembeddingbag.to(device)
    start_time = time.time()
    for i in range(num_runs):
        output_bitorch_qembeddingbag = qembeddingbag(input_cuda, example_offset_cuda)
    torch.cuda.synchronize()
    time_engine = time.time() - start_time
    # print(output_bitorch_qembeddingbag)
    print("bitorch binary qEmd CUDA run time: %.6f s" % (time_engine / num_runs))

    # QEmbeddingBag of inference engine
    input = torch.randint(0, int(vocab_size/32 - 1), (int(vocab_size/32),))
    input_cuda = to_device(input, device)
    engine_qembeddingbag = BCompressedEmbeddingBagCuda(num_embeddings=vocab_size, embedding_dim=embedding_size, device=device)
    engine_qembeddingbag.to(device)
    start_time = time.time()
    for i in range(num_runs):
        output_engine_qembeddingbag = engine_qembeddingbag(input_cuda)
    torch.cuda.synchronize()
    time_engine = time.time() - start_time
    # print(output_engine_qembeddingbag)
    print("bitorch engine binary qEmd CUDA run time: %.6f s" % (time_engine / num_runs))
    # assert torch.equal(output_bitorch_qembeddingbag, output_engine_qembeddingbag)
