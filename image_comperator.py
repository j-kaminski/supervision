import cv2
import numpy as np
from skimage.metrics import structural_similarity
from sklearn.metrics.pairwise import cosine_similarity


def image_comperator(legit_img, scam_img, threshold=0.9):
    scam = scam_img
    legit = legit_img

    blue_legit = cv2.calcHist([legit], [0], None, [256], [0, 256])
    red_legit = cv2.calcHist([legit], [1], None, [256], [0, 256])
    green_legit = cv2.calcHist([legit], [2], None, [256], [0, 256])

    blue_scam = cv2.calcHist([scam], [0], None, [256], [0, 256])
    red_scam = cv2.calcHist([scam], [1], None, [256], [0, 256])
    green_scam = cv2.calcHist([scam], [2], None, [256], [0, 256])

    blue_similarity = cosine_similarity([blue_legit.flatten()],
                                        [blue_scam.flatten()])
    red_similarity = cosine_similarity([red_legit.flatten()],
                                       [red_scam.flatten()])
    green_similarity = cosine_similarity([green_legit.flatten()],
                                         [green_scam.flatten()])

    return np.mean([blue_similarity, red_similarity, green_similarity])
