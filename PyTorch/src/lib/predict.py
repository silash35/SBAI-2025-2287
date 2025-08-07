import numpy as np
import torch


@torch.inference_mode()
def predict_torch(h1, h2, q, model, history_size):
    # Aloca os tensores que vão ser utilizados
    predicted_h1 = torch.zeros_like(h1)
    predicted_h2 = torch.zeros_like(h2)
    input = torch.zeros((1, history_size, 3))

    # Normalizar e preencher com os valores iniciais
    predicted_h1[:history_size] = model.normalize(
        h1[:history_size], model.in_min[0], model.in_max[0]
    )
    predicted_h2[:history_size] = model.normalize(
        h2[:history_size], model.in_min[1], model.in_max[1]
    )
    q = model.normalize(q, model.in_min[2], model.in_max[2])

    for i in range(history_size, len(h1)):
        # (batch_size, seq_len, input_size)
        input[0, :, 0] = predicted_h1[i - history_size : i]
        input[0, :, 1] = predicted_h2[i - history_size : i]
        input[0, :, 2] = q[i - history_size : i]

        Y_prev = model(input, True)

        predicted_h1[i] = Y_prev[0][0]
        predicted_h2[i] = Y_prev[0][1]

    # Denormalize
    predicted_h1 = model.denormalize(
        predicted_h1,
        model.out_min[0],
        model.out_max[0],
    )
    predicted_h2 = model.denormalize(
        predicted_h2,
        model.out_min[1],
        model.out_max[1],
    )
    return predicted_h1, predicted_h2


def predict_onnx(h1, h2, q, pytorch_model, onnx_model, history_size):
    # Aloca os tensores que vão ser utilizados
    predicted_h1 = np.zeros_like(h1, dtype=np.float32)
    predicted_h2 = np.zeros_like(h2, dtype=np.float32)
    input = np.zeros((1, history_size, 3), dtype=np.float32)

    # Normalizar e preencher com os valores iniciais
    predicted_h1[:history_size] = pytorch_model.normalize(
        h1[:history_size], pytorch_model.in_min[0], pytorch_model.in_max[0]
    )
    predicted_h2[:history_size] = pytorch_model.normalize(
        h2[:history_size], pytorch_model.in_min[1], pytorch_model.in_max[1]
    )
    q = pytorch_model.normalize(q, pytorch_model.in_min[2], pytorch_model.in_max[2])

    for i in range(history_size, len(h1)):
        # (batch_size, seq_len, input_size)
        input[0, :, 0] = predicted_h1[i - history_size : i]
        input[0, :, 1] = predicted_h2[i - history_size : i]
        input[0, :, 2] = q[i - history_size : i]

        Y_prev = onnx_model.run(None, {"input": input})

        predicted_h1[i] = Y_prev[0][0][0]
        predicted_h2[i] = Y_prev[0][0][1]

    # Denormalize
    predicted_h1 = pytorch_model.denormalize(
        torch.from_numpy(predicted_h1),
        pytorch_model.out_min[0],
        pytorch_model.out_max[0],
    )
    predicted_h2 = pytorch_model.denormalize(
        torch.from_numpy(predicted_h2),
        pytorch_model.out_min[1],
        pytorch_model.out_max[1],
    )
    return predicted_h1, predicted_h2
