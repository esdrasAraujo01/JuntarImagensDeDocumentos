#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa para Correção de Perspectiva de Páginas Digitalizadas - Versão com Desfazer
Autor: Manus AI
Descrição: Interface gráfica para corrigir perspectiva, rotacionar, melhorar legibilidade e desfazer alterações
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import copy


class CorrecaoPerspectivaMelhoradaComUndo:
    def __init__(self, root):
        self.root = root
        self.root.title("Correção de Perspectiva com Desfazer - Digitalização de Livros")
        self.root.geometry("1400x900")

        # Variáveis da aplicação
        self.imagem_original = None
        self.imagem_exibida = None
        self.imagem_corrigida = None
        self.imagem_processada = None  # Para armazenar versão com melhorias de legibilidade
        self.pontos_selecionados = []
        self.escala_exibicao = 1.0
        self.rotacao_atual = 0  # Graus de rotação aplicados

        # Sistema de histórico para desfazer
        self.historico_estados = []  # Lista de estados (dicionários com imagens e metadados)
        self.max_historico = 10  # Máximo de estados no histórico

        # Configurar interface
        self.configurar_interface()

    def configurar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame de controles principais
        controles_frame = ttk.Frame(main_frame)
        controles_frame.pack(fill=tk.X, pady=(0, 10))

        # Primeira linha de controles
        linha1_frame = ttk.Frame(controles_frame)
        linha1_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(linha1_frame, text="Carregar Imagem",
                   command=self.carregar_imagem).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(linha1_frame, text="Resetar Pontos",
                   command=self.resetar_pontos).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(linha1_frame, text="Corrigir Perspectiva",
                   command=self.corrigir_perspectiva).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(linha1_frame, text="Salvar Imagem",
                   command=self.salvar_imagem).pack(side=tk.LEFT, padx=(0, 10))

        # Botão Desfazer
        self.btn_desfazer = ttk.Button(linha1_frame, text="↶ Desfazer",
                                       command=self.desfazer, state="disabled")
        self.btn_desfazer.pack(side=tk.LEFT, padx=(10, 0))

        # Segunda linha de controles - Rotação
        linha2_frame = ttk.Frame(controles_frame)
        linha2_frame.pack(fill=tk.X, pady=(5, 5))

        ttk.Label(linha2_frame, text="Rotação:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(linha2_frame, text="↺ 90° Anti-horário",
                   command=self.rotacionar_anti_horario).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(linha2_frame, text="↻ 90° Horário",
                   command=self.rotacionar_horario).pack(side=tk.LEFT, padx=(0, 20))

        # Terceira linha de controles - Melhoria de Legibilidade
        linha3_frame = ttk.Frame(controles_frame)
        linha3_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Label(linha3_frame, text="Legibilidade:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(linha3_frame, text="Melhorar Contraste",
                   command=self.melhorar_contraste).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(linha3_frame, text="Aumentar Nitidez",
                   command=self.aumentar_nitidez).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(linha3_frame, text="Binarizar (P&B)",
                   command=self.binarizar_imagem).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(linha3_frame, text="Remover Ruído",
                   command=self.remover_ruido).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(linha3_frame, text="Resetar Melhorias",
                   command=self.resetar_melhorias).pack(side=tk.LEFT, padx=(0, 10))

        # Label de instruções
        self.label_instrucoes = ttk.Label(main_frame,
                                          text="1. Carregue uma imagem\n2. Use rotação se necessário\n3. Clique nos 4 cantos da página (ordem: superior esquerdo, superior direito, inferior direito, inferior esquerdo)\n4. Clique em 'Corrigir Perspectiva'\n5. Aplique melhorias de legibilidade se desejado\n6. Use 'Desfazer' para reverter a última alteração\n7. Salve o resultado",
                                          font=("Arial", 10))
        self.label_instrucoes.pack(pady=(0, 10))

        # Frame para as imagens
        imagens_frame = ttk.Frame(main_frame)
        imagens_frame.pack(fill=tk.BOTH, expand=True)

        # Frame da imagem original
        original_frame = ttk.LabelFrame(imagens_frame, text="Imagem Original")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Canvas para imagem original
        self.canvas_original = tk.Canvas(original_frame, bg="white")
        self.canvas_original.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas_original.bind("<Button-1>", self.selecionar_ponto)

        # Scrollbars para o canvas original
        scrollbar_v_orig = ttk.Scrollbar(original_frame, orient="vertical", command=self.canvas_original.yview)
        scrollbar_h_orig = ttk.Scrollbar(original_frame, orient="horizontal", command=self.canvas_original.xview)
        self.canvas_original.configure(yscrollcommand=scrollbar_v_orig.set, xscrollcommand=scrollbar_h_orig.set)

        # Frame da imagem corrigida
        corrigida_frame = ttk.LabelFrame(imagens_frame, text="Imagem Corrigida")
        corrigida_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Canvas para imagem corrigida
        self.canvas_corrigida = tk.Canvas(corrigida_frame, bg="white")
        self.canvas_corrigida.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para carregar imagem")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def salvar_estado(self, operacao):
        """Salva o estado atual no histórico para permitir desfazer"""
        estado = {
            'operacao': operacao,
            'imagem_original': self.imagem_original.copy() if self.imagem_original is not None else None,
            'imagem_corrigida': self.imagem_corrigida.copy() if self.imagem_corrigida is not None else None,
            'imagem_processada': self.imagem_processada.copy() if self.imagem_processada is not None else None,
            'pontos_selecionados': copy.deepcopy(self.pontos_selecionados),
            'rotacao_atual': self.rotacao_atual
        }

        # Adicionar ao histórico
        self.historico_estados.append(estado)

        # Limitar tamanho do histórico
        if len(self.historico_estados) > self.max_historico:
            self.historico_estados.pop(0)

        # Habilitar botão desfazer
        self.btn_desfazer.config(state="normal")

    def desfazer(self):
        """Desfaz a última operação"""
        if not self.historico_estados:
            messagebox.showinfo("Info", "Não há operações para desfazer.")
            return

        # Recuperar estado anterior
        estado_anterior = self.historico_estados.pop()

        # Restaurar estado
        self.imagem_original = estado_anterior['imagem_original']
        self.imagem_corrigida = estado_anterior['imagem_corrigida']
        self.imagem_processada = estado_anterior['imagem_processada']
        self.pontos_selecionados = estado_anterior['pontos_selecionados']
        self.rotacao_atual = estado_anterior['rotacao_atual']

        # Atualizar interface
        self.exibir_imagem_original()
        self.exibir_imagem_corrigida()

        # Desabilitar botão se não há mais histórico
        if not self.historico_estados:
            self.btn_desfazer.config(state="disabled")

        self.status_var.set(f"Operação '{estado_anterior['operacao']}' desfeita!")

    def carregar_imagem(self):
        """Carrega uma imagem do disco"""
        tipos_arquivo = [
            ("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("Todos os arquivos", "*.*")
        ]

        caminho_arquivo = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=tipos_arquivo
        )

        if caminho_arquivo:
            try:
                # Salvar estado antes da operação
                if self.imagem_original is not None:
                    self.salvar_estado("Carregar Imagem")

                # Carregar imagem com OpenCV
                self.imagem_original = cv2.imread(caminho_arquivo)
                if self.imagem_original is None:
                    raise ValueError("Não foi possível carregar a imagem")

                # Converter para RGB (OpenCV usa BGR)
                self.imagem_original = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2RGB)

                # Resetar variáveis
                self.pontos_selecionados = []
                self.rotacao_atual = 0
                self.imagem_corrigida = None
                self.imagem_processada = None

                # Limpar histórico (nova imagem = novo início)
                self.historico_estados = []
                self.btn_desfazer.config(state="disabled")

                # Exibir imagem no canvas
                self.exibir_imagem_original()

                self.status_var.set(f"Imagem carregada: {os.path.basename(caminho_arquivo)}")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem: {str(e)}")

    def rotacionar_horario(self):
        """Rotaciona a imagem 90 graus no sentido horário"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return

        # Salvar estado antes da operação
        self.salvar_estado("Rotação Horária")

        # Rotacionar imagem original
        self.imagem_original = cv2.rotate(self.imagem_original, cv2.ROTATE_90_CLOCKWISE)
        self.rotacao_atual = (self.rotacao_atual + 90) % 360

        # Rotacionar imagem corrigida se existir
        if self.imagem_corrigida is not None:
            self.imagem_corrigida = cv2.rotate(self.imagem_corrigida, cv2.ROTATE_90_CLOCKWISE)
            self.exibir_imagem_corrigida()

        # Rotacionar imagem processada se existir
        if self.imagem_processada is not None:
            self.imagem_processada = cv2.rotate(self.imagem_processada, cv2.ROTATE_90_CLOCKWISE)
            self.exibir_imagem_corrigida()

        # Resetar pontos (a rotação invalida a seleção anterior)
        self.pontos_selecionados = []

        # Atualizar exibição
        self.exibir_imagem_original()
        self.status_var.set(f"Imagem rotacionada 90° horário (total: {self.rotacao_atual}°)")

    def rotacionar_anti_horario(self):
        """Rotaciona a imagem 90 graus no sentido anti-horário"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return

        # Salvar estado antes da operação
        self.salvar_estado("Rotação Anti-horária")

        # Rotacionar imagem original
        self.imagem_original = cv2.rotate(self.imagem_original, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.rotacao_atual = (self.rotacao_atual - 90) % 360

        # Rotacionar imagem corrigida se existir
        if self.imagem_corrigida is not None:
            self.imagem_corrigida = cv2.rotate(self.imagem_corrigida, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.exibir_imagem_corrigida()

        # Rotacionar imagem processada se existir
        if self.imagem_processada is not None:
            self.imagem_processada = cv2.rotate(self.imagem_processada, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.exibir_imagem_corrigida()

        # Resetar pontos (a rotação invalida a seleção anterior)
        self.pontos_selecionados = []

        # Atualizar exibição
        self.exibir_imagem_original()
        self.status_var.set(f"Imagem rotacionada 90° anti-horário (total: {self.rotacao_atual}°)")

    def exibir_imagem_original(self):
        """Exibe a imagem original no canvas com os pontos selecionados"""
        if self.imagem_original is None:
            return

        # Calcular escala para caber no canvas
        canvas_width = self.canvas_original.winfo_width()
        canvas_height = self.canvas_original.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas ainda não foi renderizado, tentar novamente depois
            self.root.after(100, self.exibir_imagem_original)
            return

        img_height, img_width = self.imagem_original.shape[:2]

        escala_w = canvas_width / img_width
        escala_h = canvas_height / img_height
        self.escala_exibicao = min(escala_w, escala_h, 1.0)  # Não aumentar além do tamanho original

        # Redimensionar imagem para exibição
        novo_width = int(img_width * self.escala_exibicao)
        novo_height = int(img_height * self.escala_exibicao)

        imagem_redimensionada = cv2.resize(self.imagem_original, (novo_width, novo_height))

        # Desenhar pontos selecionados
        imagem_com_pontos = imagem_redimensionada.copy()
        cores_pontos = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Vermelho, Verde, Azul, Amarelo

        for i, ponto in enumerate(self.pontos_selecionados):
            x_scaled = int(ponto[0] * self.escala_exibicao)
            y_scaled = int(ponto[1] * self.escala_exibicao)
            cor = cores_pontos[i % len(cores_pontos)]
            cv2.circle(imagem_com_pontos, (x_scaled, y_scaled), 8, cor, -1)
            cv2.putText(imagem_com_pontos, str(i + 1), (x_scaled - 5, y_scaled - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)

        # Converter para formato PIL e exibir
        self.imagem_exibida = Image.fromarray(imagem_com_pontos)
        self.photo_original = ImageTk.PhotoImage(self.imagem_exibida)

        # Limpar canvas e adicionar imagem
        self.canvas_original.delete("all")
        self.canvas_original.create_image(0, 0, anchor=tk.NW, image=self.photo_original)
        self.canvas_original.configure(scrollregion=self.canvas_original.bbox("all"))

    def selecionar_ponto(self, event):
        """Seleciona um ponto na imagem original"""
        if self.imagem_original is None:
            return

        if len(self.pontos_selecionados) >= 4:
            messagebox.showwarning("Aviso",
                                   "Já foram selecionados 4 pontos. Use 'Resetar Pontos' para começar novamente.")
            return

        # Converter coordenadas do canvas para coordenadas da imagem original
        x_canvas = self.canvas_original.canvasx(event.x)
        y_canvas = self.canvas_original.canvasy(event.y)

        x_original = x_canvas / self.escala_exibicao
        y_original = y_canvas / self.escala_exibicao

        # Verificar se o ponto está dentro da imagem
        img_height, img_width = self.imagem_original.shape[:2]
        if 0 <= x_original < img_width and 0 <= y_original < img_height:
            self.pontos_selecionados.append((x_original, y_original))
            self.exibir_imagem_original()

            pontos_restantes = 4 - len(self.pontos_selecionados)
            if pontos_restantes > 0:
                self.status_var.set(
                    f"Ponto {len(self.pontos_selecionados)} selecionado. Faltam {pontos_restantes} pontos.")
            else:
                self.status_var.set("Todos os 4 pontos selecionados. Clique em 'Corrigir Perspectiva'.")

    def resetar_pontos(self):
        """Remove todos os pontos selecionados"""
        self.pontos_selecionados = []
        if self.imagem_original is not None:
            self.exibir_imagem_original()
        self.status_var.set("Pontos resetados. Selecione 4 pontos na imagem.")

    def corrigir_perspectiva(self):
        """Aplica a correção de perspectiva"""
        if self.imagem_original is None:
            messagebox.showerror("Erro", "Carregue uma imagem primeiro.")
            return

        if len(self.pontos_selecionados) != 4:
            messagebox.showerror("Erro", "Selecione exatamente 4 pontos na imagem.")
            return

        # Salvar estado antes da operação
        self.salvar_estado("Correção de Perspectiva")

        try:
            # Pontos de origem (selecionados pelo usuário)
            pontos_origem = np.float32(self.pontos_selecionados)

            # Calcular dimensões do retângulo de destino
            # Usar as distâncias entre os pontos para manter proporções
            largura1 = np.linalg.norm(pontos_origem[1] - pontos_origem[0])
            largura2 = np.linalg.norm(pontos_origem[2] - pontos_origem[3])
            largura_max = max(int(largura1), int(largura2))

            altura1 = np.linalg.norm(pontos_origem[3] - pontos_origem[0])
            altura2 = np.linalg.norm(pontos_origem[2] - pontos_origem[1])
            altura_max = max(int(altura1), int(altura2))

            # Pontos de destino (retângulo perfeito)
            pontos_destino = np.float32([
                [0, 0],
                [largura_max - 1, 0],
                [largura_max - 1, altura_max - 1],
                [0, altura_max - 1]
            ])

            # Calcular matriz de transformação
            matriz = cv2.getPerspectiveTransform(pontos_origem, pontos_destino)

            # Aplicar transformação
            self.imagem_corrigida = cv2.warpPerspective(
                self.imagem_original, matriz, (largura_max, altura_max)
            )

            # Resetar melhorias (aplicar na imagem corrigida)
            self.imagem_processada = None

            # Exibir resultado
            self.exibir_imagem_corrigida()

            self.status_var.set("Perspectiva corrigida com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao corrigir perspectiva: {str(e)}")

    def melhorar_contraste(self):
        """Melhora o contraste da imagem corrigida"""
        if self.imagem_corrigida is None:
            messagebox.showwarning("Aviso", "Corrija a perspectiva primeiro.")
            return

        # Salvar estado antes da operação
        self.salvar_estado("Melhorar Contraste")

        try:
            # Usar a imagem processada se existir, senão usar a corrigida
            imagem_base = self.imagem_processada if self.imagem_processada is not None else self.imagem_corrigida

            # Aplicar CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(imagem_base, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)

            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)

            self.imagem_processada = cv2.merge([l, a, b])
            self.imagem_processada = cv2.cvtColor(self.imagem_processada, cv2.COLOR_LAB2RGB)

            self.exibir_imagem_corrigida()
            self.status_var.set("Contraste melhorado!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao melhorar contraste: {str(e)}")

    def aumentar_nitidez(self):
        """Aumenta a nitidez da imagem corrigida"""
        if self.imagem_corrigida is None:
            messagebox.showwarning("Aviso", "Corrija a perspectiva primeiro.")
            return

        # Salvar estado antes da operação
        self.salvar_estado("Aumentar Nitidez")

        try:
            # Usar a imagem processada se existir, senão usar a corrigida
            imagem_base = self.imagem_processada if self.imagem_processada is not None else self.imagem_corrigida

            # Kernel de nitidez
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])

            self.imagem_processada = cv2.filter2D(imagem_base, -1, kernel)

            self.exibir_imagem_corrigida()
            self.status_var.set("Nitidez aumentada!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aumentar nitidez: {str(e)}")

    def binarizar_imagem(self):
        """Converte a imagem para preto e branco (binarização)"""
        if self.imagem_corrigida is None:
            messagebox.showwarning("Aviso", "Corrija a perspectiva primeiro.")
            return

        # Salvar estado antes da operação
        self.salvar_estado("Binarizar Imagem")

        try:
            # Usar a imagem processada se existir, senão usar a corrigida
            imagem_base = self.imagem_processada if self.imagem_processada is not None else self.imagem_corrigida

            # Converter para escala de cinza
            gray = cv2.cvtColor(imagem_base, cv2.COLOR_RGB2GRAY)

            # Aplicar binarização adaptativa
            binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 2)

            # Converter de volta para RGB
            self.imagem_processada = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)

            self.exibir_imagem_corrigida()
            self.status_var.set("Imagem binarizada (P&B)!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao binarizar imagem: {str(e)}")

    def remover_ruido(self):
        """Remove ruído da imagem corrigida"""
        if self.imagem_corrigida is None:
            messagebox.showwarning("Aviso", "Corrija a perspectiva primeiro.")
            return

        # Salvar estado antes da operação
        self.salvar_estado("Remover Ruído")

        try:
            # Usar a imagem processada se existir, senão usar a corrigida
            imagem_base = self.imagem_processada if self.imagem_processada is not None else self.imagem_corrigida

            # Aplicar filtro bilateral para remover ruído preservando bordas
            self.imagem_processada = cv2.bilateralFilter(imagem_base, 9, 75, 75)

            self.exibir_imagem_corrigida()
            self.status_var.set("Ruído removido!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover ruído: {str(e)}")

    def resetar_melhorias(self):
        """Reseta todas as melhorias aplicadas"""
        if self.imagem_corrigida is None:
            messagebox.showwarning("Aviso", "Corrija a perspectiva primeiro.")
            return

        # Salvar estado antes da operação
        self.salvar_estado("Resetar Melhorias")

        self.imagem_processada = None
        self.exibir_imagem_corrigida()
        self.status_var.set("Melhorias resetadas!")

    def exibir_imagem_corrigida(self):
        """Exibe a imagem corrigida no canvas"""
        # Usar imagem processada se existir, senão usar a corrigida
        imagem_para_exibir = self.imagem_processada if self.imagem_processada is not None else self.imagem_corrigida

        if imagem_para_exibir is None:
            return

        # Calcular escala para caber no canvas
        canvas_width = self.canvas_corrigida.winfo_width()
        canvas_height = self.canvas_corrigida.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas ainda não foi renderizado, tentar novamente depois
            self.root.after(100, self.exibir_imagem_corrigida)
            return

        img_height, img_width = imagem_para_exibir.shape[:2]

        escala_w = canvas_width / img_width
        escala_h = canvas_height / img_height
        escala = min(escala_w, escala_h, 1.0)

        # Redimensionar imagem para exibição
        novo_width = int(img_width * escala)
        novo_height = int(img_height * escala)

        imagem_redimensionada = cv2.resize(imagem_para_exibir, (novo_width, novo_height))

        # Converter para formato PIL e exibir
        imagem_pil = Image.fromarray(imagem_redimensionada)
        self.photo_corrigida = ImageTk.PhotoImage(imagem_pil)

        # Limpar canvas e adicionar imagem
        self.canvas_corrigida.delete("all")
        self.canvas_corrigida.create_image(0, 0, anchor=tk.NW, image=self.photo_corrigida)

    def salvar_imagem(self):
        """Salva a imagem corrigida (com melhorias se aplicadas)"""
        # Usar imagem processada se existir, senão usar a corrigida
        imagem_para_salvar = self.imagem_processada if self.imagem_processada is not None else self.imagem_corrigida

        if imagem_para_salvar is None:
            messagebox.showerror("Erro", "Não há imagem corrigida para salvar.")
            return

        tipos_arquivo = [
            ("PNG", "*.png"),
            ("JPEG", "*.jpg"),
            ("TIFF", "*.tiff"),
            ("Todos os arquivos", "*.*")
        ]

        caminho_arquivo = filedialog.asksaveasfilename(
            title="Salvar Imagem Corrigida",
            defaultextension=".png",
            filetypes=tipos_arquivo
        )

        if caminho_arquivo:
            try:
                # Converter de RGB para BGR para salvar com OpenCV
                imagem_bgr = cv2.cvtColor(imagem_para_salvar, cv2.COLOR_RGB2BGR)
                cv2.imwrite(caminho_arquivo, imagem_bgr)

                self.status_var.set(f"Imagem salva: {os.path.basename(caminho_arquivo)}")
                messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar imagem: {str(e)}")


def main():
    root = tk.Tk()
    app = CorrecaoPerspectivaMelhoradaComUndo(root)
    root.mainloop()


if __name__ == "__main__":
    main()

