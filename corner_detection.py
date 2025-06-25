import cv2
import numpy as np
from PIL import Image
from image_processing import ImageProcessor # Importa ImageProcessor

class CornerDetector:
    """Classe para encapsular a lógica de detecção de cantos de documentos."""

    @staticmethod
    def find_document_corners(image):
        """Tenta detectar automaticamente os 4 cantos de um documento em uma imagem.
        Retorna os 4 pontos ordenados (top-left, top-right, bottom-right, bottom-left)
        ou os cantos da imagem inteira se nenhum documento for encontrado.
        """
        img_np = np.array(image.convert("RGB"))
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Redimensiona para processamento mais rápido, mantendo a proporção
        ratio = image.width / 500.0
        resized = cv2.resize(img_cv, (500, int(image.height / ratio)))

        # Pré-processamento: escala de cinza, desfoque e detecção de bordas Canny
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200) # Parâmetros Canny ajustados

        # Encontra contornos na imagem com bordas
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Ordena os contornos por área em ordem decrescente e pega os 5 maiores
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        screenCnt = None
        # Itera sobre os contornos encontrados
        for c in contours:
            # Calcula o perímetro do contorno
            peri = cv2.arcLength(c, True)
            # Aproxima o contorno por um polígono com menos vértices
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # Verifica se o polígono tem 4 vértices (um retângulo)
            # e se a área é significativa (pelo menos 20% da área da imagem redimensionada)
            area = cv2.contourArea(c)
            if len(approx) == 4 and area > (resized.shape[0] * resized.shape[1] * 0.2):
                # Calcula o aspect ratio do contorno
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w)/h
                # Verifica se o aspect ratio está dentro de uma faixa razoável para documentos
                if 0.5 < aspect_ratio < 2.0: # Ajustado para ser mais flexível
                    screenCnt = approx
                    break # Encontrou o contorno do documento, pode parar

        if screenCnt is not None:
            # Se um contorno de documento foi encontrado, ordena seus pontos e redimensiona de volta
            # para as coordenadas da imagem original
            return ImageProcessor.order_points(screenCnt.reshape(4, 2) * ratio)

        # Se nenhum contorno de documento for encontrado, retorna os cantos da imagem inteira
        h, w = image.height, image.width
        return np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype="float32")


