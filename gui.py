import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from image_processing import ImageProcessor
from corner_detection import CornerDetector
import os
import cv2
import numpy as np

class ImageCanvas(tk.Canvas):
    """Widget de Canvas para exibir e manipular imagens, incluindo pontos de controle."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.img = None
        self.tk_img = None
        self.relative_points = None  # Pontos relativos (0 a 1) para a imagem
        self.active_point = None
        self.enhance_on_load = False

        # Binds de eventos do mouse
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Configure>", self._on_configure) # Redesenha ao redimensionar
        
    #salva caminho da imagem selecionada
    def load_image(self, path): 
        try:
            self.img = Image.open(path)
            self.image_path = path # Armazena o caminho da imagem
            if self.enhance_on_load:
                self.img = ImageProcessor.enhance_image_readability(self.img)
            # Inicializa os pontos para cobrir a imagem inteira
            self.relative_points = [(0, 0), (1, 0), (1, 1), (0, 1)]
            self.redraw()
        except Exception as e:
            messagebox.showerror("Erro ao carregar imagem", f"Não foi possível carregar a imagem: {e}")

    def rotate_image(self, angle):
        """Rotaciona a imagem pelo ângulo especificado."""
        if self.img:
            self.img = self.img.rotate(angle, expand=True)
            self.relative_points = [(0, 0), (1, 0), (1, 1), (0, 1)] # Reinicia pontos após rotação
            self.redraw()

    def redraw(self):
        """Redesenha a imagem e os pontos de controle no canvas."""
        self.delete("all")
        if self.img is None: return

        cw, ch = self.winfo_width(), self.winfo_height()
        if cw < 1 or ch < 1: return

        iw, ih = self.img.size
        scale = min(cw/iw, ch/ih)
        new_size = (int(iw*scale), int(ih*scale))
        
        resized = self.img.resize(new_size, Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized)

        x_offset = (cw - new_size[0]) // 2
        y_offset = (ch - new_size[1]) // 2
        self.create_image(x_offset, y_offset, anchor=tk.NW, image=self.tk_img)

        if self.relative_points:
            points_display = []
            for rx, ry in self.relative_points:
                x = x_offset + rx * new_size[0]
                y = y_offset + ry * new_size[1]
                points_display.append((x, y))
                self.create_oval(x-5, y-5, x+5, y+5, fill="red", outline="white", width=1) # Desenha pontos
            if len(points_display) == 4:
                self.create_polygon(points_display, outline="red", width=2, fill="", tags="selection_polygon") # Desenha polígono

    def get_absolute_points(self):
        """Converte pontos relativos para coordenadas absolutas na imagem original.""" 
        if self.img is None or self.relative_points is None: return None
        iw, ih = self.img.size
        return [(rx * iw, ry * ih) for rx, ry in self.relative_points]

    def _on_click(self, event):
        """Manipula o clique do mouse para selecionar um ponto de controle."""
        if self.img is None or self.relative_points is None: return
        cw, ch = self.winfo_width(), self.winfo_height()
        iw, ih = self.img.size
        scale = min(cw/iw, ch/ih)
        new_size = (int(iw*scale), int(ih*scale))
        x_offset = (cw - new_size[0]) // 2
        y_offset = (ch - new_size[1]) // 2

        min_dist_sq = float("inf")
        closest_point_idx = -1
        for idx, (rx, ry) in enumerate(self.relative_points):
            x = x_offset + rx * new_size[0]
            y = y_offset + ry * new_size[1]
            dist_sq = (event.x - x) ** 2 + (event.y - y) ** 2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_point_idx = idx
        
        if min_dist_sq < 100: # Raio de 10 pixels
            self.active_point = closest_point_idx

    def _on_drag(self, event):
        """Manipula o arrastar do mouse para mover um ponto de controle."""
        if self.active_point is None or self.img is None: return
        cw, ch = self.winfo_width(), self.winfo_height()
        iw, ih = self.img.size
        scale = min(cw/iw, ch/ih)
        new_size = (int(iw*scale), int(ih*scale))
        x_offset = (cw - new_size[0]) // 2
        y_offset = (ch - new_size[1]) // 2

        rx = (event.x - x_offset) / new_size[0]
        ry = (event.y - y_offset) / new_size[1]
        rx = max(0.0, min(rx, 1.0))
        ry = max(0.0, min(ry, 1.0))
        
        self.relative_points[self.active_point] = (rx, ry)
        self.redraw()

    def _on_release(self, event):
        """Manipula a liberação do mouse."""
        self.active_point = None

    def get_corrected_image(self):
        """Retorna a imagem com a perspectiva corrigida com base nos pontos de controle."""
        if self.img is None or self.relative_points is None or len(self.relative_points) != 4:
            return self.img
        abs_pts = self.get_absolute_points()
        try:
            return ImageProcessor.four_point_transform(self.img, abs_pts)
        except Exception as e:
            messagebox.showerror("Erro na transformação", f"Erro na transformação de perspectiva: {e}")
            return self.img

    def _on_configure(self, event):
        """Redesenha o canvas quando seu tamanho é alterado."""
        if self.winfo_width() > 1 and self.winfo_height() > 1:
            self.redraw()

    def auto_detect_corners(self):
        """Tenta detectar e definir automaticamente os cantos do documento."""
        if self.img is None:
            messagebox.showwarning("Detecção Automática", "Carregue uma imagem primeiro para usar a detecção automática.")
            return
        try:
            detected_corners = CornerDetector.find_document_corners(self.img)
            iw, ih = self.img.size
            self.relative_points = [
                (p[0] / iw, p[1] / ih) for p in detected_corners
            ]
            self.redraw()
        except Exception as e:
            messagebox.showerror("Erro na Detecção Automática", f"Não foi possível detectar os cantos automaticamente: {e}")

class ImageMergerApp:
    """Classe principal da aplicação Tkinter para juntar e corrigir imagens."""
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar e Corrigir Imagens")

        # Configuração da interface
        self._setup_ui()

    def _setup_ui(self):
        """Configura os elementos da interface do usuário."""
        self.canvas_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas1 = ImageCanvas(self.canvas_frame, bg="lightgray")
        self.canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.canvas2 = ImageCanvas(self.canvas_frame, bg="lightgray")
        self.canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.controls = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        self.controls.pack(pady=10, padx=5, fill=tk.X)

        # Botões e controles para Imagem 1
        tk.Label(self.controls, text="Imagem 1").grid(row=0, column=0, columnspan=3, pady=5)
        tk.Button(self.controls, text="Selecionar", command=self._load_image1).grid(row=1, column=0, padx=5, pady=2)
        tk.Button(self.controls, text="Rot. Esquerda", command=lambda: self.canvas1.rotate_image(90)).grid(row=1, column=1, padx=5, pady=2)
        tk.Button(self.controls, text="Rot. Direita", command=lambda: self.canvas1.rotate_image(-90)).grid(row=1, column=2, padx=5, pady=2)
        tk.Button(self.controls, text="Detectar Cantos", command=lambda: self.canvas1.auto_detect_corners()).grid(row=2, column=0, columnspan=3, pady=5)

        # Botões e controles para Imagem 2
        tk.Label(self.controls, text="Imagem 2").grid(row=0, column=3, columnspan=3, pady=5)
        tk.Button(self.controls, text="Selecionar", command=self._load_image2).grid(row=1, column=3, padx=5, pady=2)
        tk.Button(self.controls, text="Rot. Esquerda", command=lambda: self.canvas2.rotate_image(90)).grid(row=1, column=4, padx=5, pady=2)
        tk.Button(self.controls, text="Rot. Direita", command=lambda: self.canvas2.rotate_image(-90)).grid(row=1, column=5, padx=5, pady=2)
        tk.Button(self.controls, text="Detectar Cantos", command=lambda: self.canvas2.auto_detect_corners()).grid(row=2, column=3, columnspan=3, pady=5)

        # Botão de Juntar Imagens
        tk.Button(self.controls, text="Juntar Imagens", command=self.merge_images, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=6, pady=10)

        # Checkbox para melhoria de imagem
        self.enhance_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.controls, text="Melhorar Legibilidade ao Carregar", variable=self.enhance_var, command=self._toggle_image_enhancement).grid(row=4, column=0, columnspan=6, pady=5)

        # Configurações de coluna para centralizar os botões
        for i in range(6):
            self.controls.grid_columnconfigure(i, weight=1)

    def _toggle_image_enhancement(self):
        """Ativa/desativa a melhoria de legibilidade ao carregar imagens."""
        state = self.enhance_var.get()
        self.canvas1.enhance_on_load = state
        self.canvas2.enhance_on_load = state

    def _load_image1(self):
        """Carrega a primeira imagem selecionada pelo usuário."""
        path = filedialog.askopenfilename(filetypes=[
            ("Imagens", "*.png *.jpg *.jpeg *.JPG *.JPEG *.bmp *.gif"),
            ("Todos os arquivos", "*.*")
        ])
        if path:
            self.canvas1.load_image(path)

    def _load_image2(self):
        """Carrega a segunda imagem selecionada pelo usuário."""
        path = filedialog.askopenfilename(filetypes=[
            ("Imagens", "*.png *.jpg *.jpeg *.JPG *.JPEG *.bmp *.gif"),
            ("Todos os arquivos", "*.*")
        ])
        if path:
            self.canvas2.load_image(path)

      #Atualização pasta/caminho
    def merge_images(self):
        if self.canvas1.img is None or self.canvas2.img is None:
            messagebox.showwarning("Erro", "Selecione e carregue ambas as imagens antes de juntar!")
            return

        try:
            corrected1 = self.canvas1.get_corrected_image()
            corrected2 = self.canvas2.get_corrected_image()

            # Redimensiona a segunda imagem para a altura da primeira
            if corrected1.height != corrected2.height:
                corrected2 = corrected2.resize((int(corrected2.width * corrected1.height / corrected2.height), corrected1.height), Image.Resampling.LANCZOS)

            # Cria uma nova imagem para a fusão
            merged_width = corrected1.width + corrected2.width
            merged_height = corrected1.height
            merged_image = Image.new("RGB", (merged_width, merged_height))

            # Cola as imagens
            merged_image.paste(corrected1, (0, 0))
            merged_image.paste(corrected2, (corrected1.width, 0))

            # Define o diretório base de salvamento como 'resultado' na pasta do script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_output_dir = os.path.join(script_dir, "resultado")
            os.makedirs(base_output_dir, exist_ok=True)

            # Obtém o diretório da primeira imagem carregada
            # Assume que self.canvas1.image_path armazena o caminho completo da imagem
            if hasattr(self.canvas1, 'image_path') and self.canvas1.image_path:
                # Extrai o nome do diretório pai da imagem (ex: 'Teste' de 'Teste/batata.png')
                image_source_dir_name = os.path.basename(os.path.dirname(self.canvas1.image_path))
                output_dir = os.path.join(base_output_dir, image_source_dir_name)
            else:
                # Se o caminho da imagem não estiver disponível, salva diretamente em 'resultado'
                output_dir = base_output_dir
            
            os.makedirs(output_dir, exist_ok=True)

            # Pergunta ao usuário apenas o nome e tipo do arquivo, com o diretório inicial correto
            save_name = filedialog.asksaveasfilename(initialdir=output_dir, defaultextension=".jpg", filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("Todos os arquivos", "*.*")
            ])
            
            if save_name:
                merged_image.save(save_name)
                messagebox.showinfo("Sucesso", f"Imagem salva em {save_name}")

        except Exception as e:
            messagebox.showerror("Erro ao juntar imagens", f"Ocorreu um erro ao juntar as imagens: {e}")

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
        ratio = image.width / 800.0 
        resized = cv2.resize(img_cv, (800, int(image.height / ratio)))

        # Converter para LAB e aplicar CLAHE para realce de contraste
        lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        merged = cv2.merge((cl, a, b))
        contrast_enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

        # Converter para escala de cinza
        gray = cv2.cvtColor(contrast_enhanced, cv2.COLOR_BGR2GRAY)

        # Aplicar desfoque leve
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detecção de bordas
                # Detecção de bordas
        # Detecção de bordas
                # Detecção de bordas
        edged = cv2.Canny(blurred, 75, 200)

        # --- Adição para fechar brechas nas bordas ---
        kernel = np.ones((5,5),np.uint8)
        closed_edges = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        # --------------------------------------------------

        # --- Adição para salvar a imagem intermediária (closed_edges) ---
        debug_dir = "./debug_images"
        os.makedirs(debug_dir, exist_ok=True)
        debug_image_path_closed = os.path.join(debug_dir, "closed_edges_image.jpg")
        cv2.imwrite(debug_image_path_closed, closed_edges)
        print(f"Imagem de bordas fechadas salva em: {debug_image_path_closed}")
        # --------------------------------------------------

        # Encontra contornos na imagem com bordas fechadas
        contours, _ = cv2.findContours(closed_edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Ordena os contornos por área em ordem decrescente e pega os 10 maiores
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        screenCnt = None
        # Itera sobre os contornos encontrados
        for c in contours:
            # Calcula o perímetro do contorno
            peri = cv2.arcLength(c, True)
            # Aproxima o contorno por um polígono com menos vértices
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # Verifica se o polígono tem 4 vértices (um retângulo)
            # e se a área é significativa (pelo menos 10% da área da imagem redimensionada)
            area = cv2.contourArea(c)
            if len(approx) == 4 and area > (resized.shape[0] * resized.shape[1] * 0.1):
                # Calcula o aspect ratio do contorno
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w)/h
                # Verifica se o aspect ratio está dentro de uma faixa razoável para documentos
                if 0.4 < aspect_ratio < 2.5: 
                    screenCnt = approx
                    break # Encontrou o contorno do documento, pode parar

        if screenCnt is not None:
            # Se um contorno de documento foi encontrado, ordena seus pontos e redimensiona de volta
            # para as coordenadas da imagem original
            return ImageProcessor.order_points(screenCnt.reshape(4, 2) * ratio)

        # Se nenhum contorno de documento for encontrado, retorna os cantos da imagem inteira
        h, w = image.height, image.width
        return np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype="float32")


root = tk.Tk()
app = ImageMergerApp(root)
root.mainloop()


