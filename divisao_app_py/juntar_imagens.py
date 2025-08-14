#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa para Juntar Imagens de Páginas Digitalizadas
Autor: Manus AI
Descrição: Interface gráfica para combinar duas imagens de páginas em uma única imagem
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

class JuntarImagens:
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar Imagens - Digitalização de Livros")
        self.root.geometry("1400x900")
        
        # Variáveis da aplicação
        self.imagem1 = None
        self.imagem2 = None
        self.imagem_combinada = None
        self.orientacao = tk.StringVar(value="horizontal")
        self.alinhamento = tk.StringVar(value="centro")
        self.sobreposicao = tk.IntVar(value=0)
        
        # Configurar interface
        self.configurar_interface()
        
    def configurar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de controles
        controles_frame = ttk.Frame(main_frame)
        controles_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Primeira linha de controles
        linha1_frame = ttk.Frame(controles_frame)
        linha1_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(linha1_frame, text="Carregar Imagem 1", 
                  command=lambda: self.carregar_imagem(1)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(linha1_frame, text="Carregar Imagem 2", 
                  command=lambda: self.carregar_imagem(2)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(linha1_frame, text="Combinar Imagens", 
                  command=self.combinar_imagens).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(linha1_frame, text="Salvar Resultado", 
                  command=self.salvar_imagem).pack(side=tk.LEFT, padx=(0, 10))
        
        # Segunda linha de controles - Opções
        linha2_frame = ttk.Frame(controles_frame)
        linha2_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Orientação
        ttk.Label(linha2_frame, text="Orientação:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(linha2_frame, text="Horizontal", variable=self.orientacao, 
                       value="horizontal").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(linha2_frame, text="Vertical", variable=self.orientacao, 
                       value="vertical").pack(side=tk.LEFT, padx=(0, 20))
        
        # Alinhamento
        ttk.Label(linha2_frame, text="Alinhamento:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(linha2_frame, text="Início", variable=self.alinhamento, 
                       value="inicio").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(linha2_frame, text="Centro", variable=self.alinhamento, 
                       value="centro").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(linha2_frame, text="Fim", variable=self.alinhamento, 
                       value="fim").pack(side=tk.LEFT, padx=(0, 20))
        
        # Sobreposição
        ttk.Label(linha2_frame, text="Sobreposição (px):").pack(side=tk.LEFT, padx=(0, 5))
        sobreposicao_spinbox = ttk.Spinbox(linha2_frame, from_=0, to=500, width=10, 
                                          textvariable=self.sobreposicao)
        sobreposicao_spinbox.pack(side=tk.LEFT, padx=(0, 10))
        
        # Label de instruções
        self.label_instrucoes = ttk.Label(main_frame, 
            text="1. Carregue as duas imagens que deseja combinar\n2. Escolha a orientação (horizontal para páginas lado a lado, vertical para páginas uma sobre a outra)\n3. Defina o alinhamento e sobreposição se necessário\n4. Clique em 'Combinar Imagens' e depois 'Salvar Resultado'",
            font=("Arial", 10))
        self.label_instrucoes.pack(pady=(0, 10))
        
        # Frame para as imagens
        imagens_frame = ttk.Frame(main_frame)
        imagens_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame das imagens originais
        originais_frame = ttk.Frame(imagens_frame)
        originais_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame da imagem 1
        img1_frame = ttk.LabelFrame(originais_frame, text="Imagem 1")
        img1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.canvas1 = tk.Canvas(img1_frame, bg="white")
        self.canvas1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame da imagem 2
        img2_frame = ttk.LabelFrame(originais_frame, text="Imagem 2")
        img2_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.canvas2 = tk.Canvas(img2_frame, bg="white")
        self.canvas2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame da imagem combinada
        combinada_frame = ttk.LabelFrame(imagens_frame, text="Imagem Combinada")
        combinada_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_combinada = tk.Canvas(combinada_frame, bg="white")
        self.canvas_combinada.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para carregar imagens")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def carregar_imagem(self, numero):
        """Carrega uma imagem do disco"""
        tipos_arquivo = [
            ("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("Todos os arquivos", "*.*")
        ]
        
        caminho_arquivo = filedialog.askopenfilename(
            title=f"Selecionar Imagem {numero}",
            filetypes=tipos_arquivo
        )
        
        if caminho_arquivo:
            try:
                # Carregar imagem com OpenCV
                imagem = cv2.imread(caminho_arquivo)
                if imagem is None:
                    raise ValueError("Não foi possível carregar a imagem")
                
                # Converter para RGB (OpenCV usa BGR)
                imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
                
                if numero == 1:
                    self.imagem1 = imagem
                    self.exibir_imagem(self.canvas1, imagem)
                    self.status_var.set(f"Imagem 1 carregada: {os.path.basename(caminho_arquivo)}")
                else:
                    self.imagem2 = imagem
                    self.exibir_imagem(self.canvas2, imagem)
                    self.status_var.set(f"Imagem 2 carregada: {os.path.basename(caminho_arquivo)}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem {numero}: {str(e)}")
                
    def exibir_imagem(self, canvas, imagem):
        """Exibe uma imagem no canvas especificado"""
        if imagem is None:
            return
            
        # Calcular escala para caber no canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas ainda não foi renderizado, tentar novamente depois
            self.root.after(100, lambda: self.exibir_imagem(canvas, imagem))
            return
            
        img_height, img_width = imagem.shape[:2]
        
        escala_w = canvas_width / img_width
        escala_h = canvas_height / img_height
        escala = min(escala_w, escala_h, 1.0)
        
        # Redimensionar imagem para exibição
        novo_width = int(img_width * escala)
        novo_height = int(img_height * escala)
        
        imagem_redimensionada = cv2.resize(imagem, (novo_width, novo_height))
        
        # Converter para formato PIL e exibir
        imagem_pil = Image.fromarray(imagem_redimensionada)
        photo = ImageTk.PhotoImage(imagem_pil)
        
        # Limpar canvas e adicionar imagem
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, anchor=tk.CENTER, image=photo)
        
        # Manter referência da imagem para evitar garbage collection
        canvas.image = photo
        
    def combinar_imagens(self):
        """Combina as duas imagens carregadas"""
        if self.imagem1 is None or self.imagem2 is None:
            messagebox.showerror("Erro", "Carregue ambas as imagens primeiro.")
            return
            
        try:
            img1 = self.imagem1.copy()
            img2 = self.imagem2.copy()
            
            h1, w1 = img1.shape[:2]
            h2, w2 = img2.shape[:2]
            
            sobreposicao = self.sobreposicao.get()
            
            if self.orientacao.get() == "horizontal":
                # Combinar horizontalmente
                altura_final = max(h1, h2)
                largura_final = w1 + w2 - sobreposicao
                
                # Redimensionar imagens se necessário para ter a mesma altura
                if h1 != h2:
                    if h1 > h2:
                        # Redimensionar img2 para ter a mesma altura de img1
                        novo_w2 = int(w2 * h1 / h2)
                        img2 = cv2.resize(img2, (novo_w2, h1))
                        w2 = novo_w2
                        h2 = h1
                    else:
                        # Redimensionar img1 para ter a mesma altura de img2
                        novo_w1 = int(w1 * h2 / h1)
                        img1 = cv2.resize(img1, (novo_w1, h2))
                        w1 = novo_w1
                        h1 = h2
                
                altura_final = h1  # Agora ambas têm a mesma altura
                largura_final = w1 + w2 - sobreposicao
                
                # Criar imagem combinada
                self.imagem_combinada = np.zeros((altura_final, largura_final, 3), dtype=np.uint8)
                
                # Posicionar primeira imagem
                self.imagem_combinada[0:h1, 0:w1] = img1
                
                # Posicionar segunda imagem
                inicio_x = w1 - sobreposicao
                if sobreposicao > 0:
                    # Aplicar blend na área de sobreposição
                    for x in range(sobreposicao):
                        alpha = x / sobreposicao  # Gradiente de 0 a 1
                        x_img1 = w1 - sobreposicao + x
                        x_img2 = x
                        x_final = inicio_x + x
                        
                        if x_final < largura_final and x_img1 < w1 and x_img2 < w2:
                            self.imagem_combinada[0:h2, x_final] = (
                                (1 - alpha) * img1[0:h1, x_img1] + 
                                alpha * img2[0:h2, x_img2]
                            ).astype(np.uint8)
                    
                    # Adicionar o resto da segunda imagem
                    resto_inicio = inicio_x + sobreposicao
                    resto_img2 = img2[:, sobreposicao:]
                    if resto_inicio < largura_final:
                        fim_x = min(largura_final, resto_inicio + resto_img2.shape[1])
                        self.imagem_combinada[0:h2, resto_inicio:fim_x] = resto_img2[:, :fim_x-resto_inicio]
                else:
                    # Sem sobreposição
                    self.imagem_combinada[0:h2, inicio_x:inicio_x+w2] = img2
                    
            else:
                # Combinar verticalmente
                largura_final = max(w1, w2)
                altura_final = h1 + h2 - sobreposicao
                
                # Redimensionar imagens se necessário para ter a mesma largura
                if w1 != w2:
                    if w1 > w2:
                        # Redimensionar img2 para ter a mesma largura de img1
                        novo_h2 = int(h2 * w1 / w2)
                        img2 = cv2.resize(img2, (w1, novo_h2))
                        h2 = novo_h2
                        w2 = w1
                    else:
                        # Redimensionar img1 para ter a mesma largura de img2
                        novo_h1 = int(h1 * w2 / w1)
                        img1 = cv2.resize(img1, (w2, novo_h1))
                        h1 = novo_h1
                        w1 = w2
                
                largura_final = w1  # Agora ambas têm a mesma largura
                altura_final = h1 + h2 - sobreposicao
                
                # Criar imagem combinada
                self.imagem_combinada = np.zeros((altura_final, largura_final, 3), dtype=np.uint8)
                
                # Posicionar primeira imagem
                self.imagem_combinada[0:h1, 0:w1] = img1
                
                # Posicionar segunda imagem
                inicio_y = h1 - sobreposicao
                if sobreposicao > 0:
                    # Aplicar blend na área de sobreposição
                    for y in range(sobreposicao):
                        alpha = y / sobreposicao  # Gradiente de 0 a 1
                        y_img1 = h1 - sobreposicao + y
                        y_img2 = y
                        y_final = inicio_y + y
                        
                        if y_final < altura_final and y_img1 < h1 and y_img2 < h2:
                            self.imagem_combinada[y_final, 0:w2] = (
                                (1 - alpha) * img1[y_img1, 0:w1] + 
                                alpha * img2[y_img2, 0:w2]
                            ).astype(np.uint8)
                    
                    # Adicionar o resto da segunda imagem
                    resto_inicio = inicio_y + sobreposicao
                    resto_img2 = img2[sobreposicao:, :]
                    if resto_inicio < altura_final:
                        fim_y = min(altura_final, resto_inicio + resto_img2.shape[0])
                        self.imagem_combinada[resto_inicio:fim_y, 0:w2] = resto_img2[:fim_y-resto_inicio, :]
                else:
                    # Sem sobreposição
                    self.imagem_combinada[inicio_y:inicio_y+h2, 0:w2] = img2
            
            # Exibir resultado
            self.exibir_imagem(self.canvas_combinada, self.imagem_combinada)
            
            self.status_var.set("Imagens combinadas com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao combinar imagens: {str(e)}")
            
    def salvar_imagem(self):
        """Salva a imagem combinada"""
        if self.imagem_combinada is None:
            messagebox.showerror("Erro", "Não há imagem combinada para salvar.")
            return
            
        tipos_arquivo = [
            ("PNG", "*.png"),
            ("JPEG", "*.jpg"),
            ("TIFF", "*.tiff"),
            ("Todos os arquivos", "*.*")
        ]
        
        caminho_arquivo = filedialog.asksaveasfilename(
            title="Salvar Imagem Combinada",
            defaultextension=".png",
            filetypes=tipos_arquivo
        )
        
        if caminho_arquivo:
            try:
                # Converter de RGB para BGR para salvar com OpenCV
                imagem_bgr = cv2.cvtColor(self.imagem_combinada, cv2.COLOR_RGB2BGR)
                cv2.imwrite(caminho_arquivo, imagem_bgr)
                
                self.status_var.set(f"Imagem salva: {os.path.basename(caminho_arquivo)}")
                messagebox.showinfo("Sucesso", "Imagem combinada salva com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar imagem: {str(e)}")

def main():
    root = tk.Tk()
    app = JuntarImagens(root)
    root.mainloop()

if __name__ == "__main__":
    main()

