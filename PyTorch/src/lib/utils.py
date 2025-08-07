import time

import torch
from notifypy import Notify


def dydx(x, y):
    return torch.autograd.grad(
        y, x, grad_outputs=torch.ones_like(y), create_graph=True
    )[0]


def safe_sqrt(x):
    return torch.sqrt(torch.clamp(x, min=0))


def mean_square(x):
    return torch.mean(x**2)


def mean_abs(x):
    return torch.mean(torch.abs(x))


def prepare_sequences(
    input_sequences, target_sequences, history_size: int, overlap=True
):
    step = 1 if overlap else history_size

    # Crie as entradas (X_true) a partir das sequências usando unfold
    input_sequences = [
        seq.unfold(0, history_size, step)[:-1] for seq in input_sequences
    ]

    # Empilhe e permute as dimensões para obter o tensor final de entradas
    X_true = torch.stack(input_sequences).permute(1, 2, 0)

    # Crie os alvos (Y_true) pegando o último valor de cada sequência
    target_seqs = [
        seq.unfold(0, history_size, step)[1:, -1] for seq in target_sequences
    ]

    # Empilhe e permute as dimensões para obter o tensor final de alvos
    Y_true = torch.stack(target_seqs).permute(1, 0)

    return X_true, Y_true


def notify_training_end():
    notification = Notify()
    notification.application_name = "PyTorch"
    notification.title = "Sua rede neural finalizou o treinamento!"
    notification.message = "Confira já os resultados."
    notification.send(block=False)


def enable_optimizations():
    torch.jit.enable_onednn_fusion(True)
    torch.autograd.set_detect_anomaly(False, False)
    torch.autograd.profiler.emit_nvtx(enabled=False)
    torch.autograd.profiler.profile(enabled=False)
    torch.backends.cudnn.benchmark = True


def timer(func, *args):
    start_time = time.monotonic()
    result = func(*args)
    elapsed_time = time.monotonic() - start_time
    return result, elapsed_time
