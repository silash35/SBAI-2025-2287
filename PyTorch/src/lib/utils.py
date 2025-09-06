import time

import torch
from notifypy import Notify


def mean_square(x):
    return torch.mean(x**2)


def prepare_sequences(
    input_sequences, target_sequences, history_size: int, overlap=True
):
    step = 1 if overlap else history_size

    # Create input sequences (X_true) using unfold to generate sliding windows
    input_sequences = [
        seq.unfold(0, history_size, step)[:-1] for seq in input_sequences
    ]

    # Stack and permute dimensions to get final input tensor
    X_true = torch.stack(input_sequences).permute(1, 2, 0)

    # Create target sequences (Y_true) by taking the last value of each target sequence window
    target_seqs = [
        seq.unfold(0, history_size, step)[1:, -1] for seq in target_sequences
    ]

    # Stack and permute dimensions to get final target tensor
    Y_true = torch.stack(target_seqs).permute(1, 0)

    return X_true, Y_true


def notify_training_end():
    notification = Notify()
    notification.application_name = "PyTorch"
    notification.title = "Your neural network has finished training!"
    notification.message = "Check the results now."
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
