from torch import nn

models_folder = "../models/"


def export_params(model: nn.Module, model_name: str):
    with open(f"{models_folder}{model_name}_params.txt", "w") as file:
        state_dict = model.state_dict()
        for name, param in state_dict.items():
            weights = param.numpy()
            dims = weights.shape

            # Converte o numpy array para uma string formatada no estilo C++ sem chaves internas
            if weights.ndim == 1:
                # Vetor 1D
                formatted_weights = "{" + ", ".join(f"{v:.6f}" for v in weights) + "};"
            elif weights.ndim == 2:
                # Matriz 2D
                flattened_weights = (
                    weights.flatten()
                )  # Achata a matriz para uma única dimensão
                formatted_weights = (
                    "{" + ", ".join(f"{v:.6f}" for v in flattened_weights) + "};"
                )
            else:
                raise ValueError("Este script lida apenas com tensores de 1D ou 2D.")

            # Imprime as informações do tensor
            file.write(f"Nome: {name}\n")
            file.write(f"Dimensões: {dims}\n")
            file.write(f"Valores:\n{formatted_weights}\n\n")
