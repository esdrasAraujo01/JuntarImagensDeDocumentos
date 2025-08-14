#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação - Programas de Digitalização de Livros
Autor: Manus AI
Descrição: Instala automaticamente as dependências necessárias
"""

import subprocess
import sys
import os

def verificar_python():
    """Verifica se a versão do Python é compatível"""
    versao = sys.version_info
    if versao.major < 3 or (versao.major == 3 and versao.minor < 7):
        print("❌ ERRO: Python 3.7 ou superior é necessário.")
        print(f"   Versão atual: {versao.major}.{versao.minor}.{versao.micro}")
        print("   Por favor, atualize o Python e tente novamente.")
        return False
    else:
        print(f"✅ Python {versao.major}.{versao.minor}.{versao.micro} - Compatível")
        return True

def instalar_pacote(pacote):
    """Instala um pacote Python usando pip"""
    try:
        print(f"📦 Instalando {pacote}...")
        resultado = subprocess.run([sys.executable, "-m", "pip", "install", pacote], 
                                 capture_output=True, text=True, check=True)
        print(f"✅ {pacote} instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {pacote}:")
        print(f"   {e.stderr}")
        return False

def verificar_pacote(pacote):
    """Verifica se um pacote está instalado"""
    try:
        __import__(pacote)
        return True
    except ImportError:
        return False

def main():
    print("=" * 60)
    print("🔧 INSTALADOR - Programas de Digitalização de Livros")
    print("=" * 60)
    print()
    
    # Verificar Python
    if not verificar_python():
        input("Pressione Enter para sair...")
        return
    
    print()
    
    # Lista de dependências
    dependencias = [
        ("opencv-python", "cv2"),
        ("pillow", "PIL")
    ]
    
    print("🔍 Verificando dependências...")
    print()
    
    instalar_lista = []
    
    for pacote_pip, pacote_import in dependencias:
        if verificar_pacote(pacote_import):
            print(f"✅ {pacote_pip} - Já instalado")
        else:
            print(f"❌ {pacote_pip} - Não encontrado")
            instalar_lista.append(pacote_pip)
    
    print()
    
    if not instalar_lista:
        print("🎉 Todas as dependências já estão instaladas!")
        print()
        print("Você pode executar os programas:")
        print("  • python correcao_perspectiva.py")
        print("  • python juntar_imagens.py")
    else:
        print(f"📋 Pacotes a instalar: {', '.join(instalar_lista)}")
        print()
        
        resposta = input("Deseja instalar as dependências agora? (s/n): ").lower().strip()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            print()
            print("🚀 Iniciando instalação...")
            print()
            
            sucesso = True
            for pacote in instalar_lista:
                if not instalar_pacote(pacote):
                    sucesso = False
            
            print()
            if sucesso:
                print("🎉 Instalação concluída com sucesso!")
                print()
                print("Você pode agora executar os programas:")
                print("  • python correcao_perspectiva.py")
                print("  • python juntar_imagens.py")
            else:
                print("❌ Houve problemas na instalação.")
                print("   Tente instalar manualmente com:")
                print("   pip install opencv-python pillow")
        else:
            print("⏭️  Instalação cancelada.")
            print("   Para instalar manualmente:")
            print("   pip install opencv-python pillow")
    
    print()
    print("=" * 60)
    print("📖 Para mais informações, consulte o arquivo README.md")
    print("=" * 60)
    
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()

