import numpy as np
from numpy import pi
from utils.coordinates import RotationMatrices

def world_translation(x: float, y: float, z: float ) -> np.ndarray:
    """
    Calculate translation matrix for world coordinates
    Args:
        x (float): translation in x-axis
        y (float): translation in y-axis
        z (float): translation in z-axis
    Returns:
        np.ndarray: translation matrix
    """

    translate_matrix = np.eye(4)
    translate_matrix[0, -1] = x
    translate_matrix[1, -1] = y
    translate_matrix[2, -1] = z

    return translate_matrix


def world_rotation(eixo: str, theta: float | int) -> np.ndarray:
    """
    Calculate rotation matrix for world coordinates
    Args:
        eixo (str): axis of rotation
        theta (float): angle of rotation
    Returns:
        np.ndarray: rotation matrix
    """
    rotation_matrices = RotationMatrices.from_theta(theta)
    rotation_matrix = getattr(rotation_matrices, eixo, None)
    
    if rotation_matrix is None:
        print('Eixo inexistente ou incorreto.')
        return np.array([])
    
    print(f"Matriz de rotação {eixo}:\n{rotation_matrix}")
    return rotation_matrix
