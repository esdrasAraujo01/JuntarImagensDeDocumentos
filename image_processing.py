import cv2
import numpy as np
from PIL import Image

class ImageProcessor:
    """Classe para encapsular funções de processamento de imagem."""

    @staticmethod
    def order_points(pts):
        """Ordena os 4 pontos em: top-left, top-right, bottom-right, bottom-left.
        Usa a soma e a diferença das coordenadas para ordenar os pontos de forma robusta.
        """
        pts = np.array(pts, dtype="float32")
        s = pts.sum(axis=1)
        ordered = np.zeros((4, 2), dtype="float32")
        ordered[0] = pts[np.argmin(s)]
        ordered[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        ordered[1] = pts[np.argmin(diff)]
        ordered[3] = pts[np.argmax(diff)]
        return ordered

    @staticmethod
    def four_point_transform(image, pts):
        """Aplica uma transformação de perspectiva em uma imagem.
        Recebe uma imagem PIL e 4 pontos (x,y) que definem a região a ser transformada.
        """
        image_np = np.array(image) if isinstance(image, Image.Image) else image
        rect = ImageProcessor.order_points(pts)
        (tl, tr, br, bl) = rect

        # Calcula a largura e altura da nova imagem transformada
        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = int(max(widthA, widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = int(max(heightA, heightB))

        # Define os pontos de destino para a transformação (retângulo)
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        # Calcula a matriz de transformação de perspectiva e aplica-a
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image_np, M, (maxWidth, maxHeight))
        return Image.fromarray(warped)

    @staticmethod
    def enhance_image_readability(image):
        """Melhora a legibilidade da imagem preservando as cores.
        Aplica CLAHE no canal L do espaço de cores LAB para aprimorar o contraste
        e um desfoque Gaussiano para reduzir ruído.
        """
        img_np = np.array(image.convert("RGB"))
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Converte para o espaço de cores LAB
        lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Aplica CLAHE no canal L (luminosidade)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl = clahe.apply(l)

        # Combina os canais de volta e converte para BGR
        limg = cv2.merge((cl, a, b))
        enhanced_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        # Aplica desfoque Gaussiano para remover ruído
        blurred = cv2.GaussianBlur(enhanced_bgr, (7, 7), 0)

        # Converte de volta para imagem PIL
        return Image.fromarray(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))


