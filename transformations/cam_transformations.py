import numpy as np
from numpy import pi
from transformations.world_transformations import (world_rotation,
                                                   world_translation)


def cam_translation(M_cam: np.ndarray, x: float, y: float, z: float) -> np.ndarray:
    """Calculate translation in relation to the camera
    Args:
        M_cam (np.ndarray): Camera matrix
        x (float): Translation in x
        y (float): Translation in y
        z (float): Translation in z
    Returns:
        np.ndarray: Translation matrix
    """
    print("Perfoming cam translation")
    M_inv = np.linalg.inv(M_cam)
    T = world_translation(x, y, z)
    translate_matrix = M_cam @ T @ M_inv

    return translate_matrix


def cam_rotation(M_cam: np.ndarray, eixo: str, theta: float) -> np.ndarray:
    """Calculate rotation in relation to the camera
    Args:
        M_cam (np.ndarray): Camera matrix
        eixo (str): Axis to rotate
        theta (float): Angle in degrees
    Returns:
        np.ndarray: Rotation matrix
    """
    print("Perfoming cam rotation")
    theta = theta*pi/180
    M_inv = np.linalg.inv(M_cam)
    R = world_rotation(eixo, theta)
    rotation_matrix = M_cam @ R @ M_inv
    
    return rotation_matrix
