# 🚀 Guia Rápido - Digitalização de Livros

## ⚡ Início Rápido

### 1️⃣ Primeira Vez
```bash
# Instalar dependências automaticamente
python instalar_dependencias.py

# OU instalar manualmente
pip install opencv-python pillow
```

### 2️⃣ Executar Programas
```bash
# Corrigir perspectiva de páginas
python correcao_perspectiva.py

# Juntar duas páginas
python juntar_imagens.py
```

## 📋 Fluxo de Trabalho

### Para Livros com Páginas Contínuas

1. **📸 Fotografe** cada página individualmente
2. **🔧 Corrija** a perspectiva de cada foto
3. **🔗 Junte** as páginas que formam uma unidade
4. **💾 Salve** com nomes organizados

### Exemplo Prático
```
Foto original: IMG_001.jpg (página esquerda)
Foto original: IMG_002.jpg (página direita)
    ↓ Corrigir perspectiva
Corrigida: pagina_001_corrigida.png
Corrigida: pagina_002_corrigida.png
    ↓ Juntar horizontalmente
Resultado: paginas_001_002_completa.png
```

## 🎯 Dicas Importantes

### ✅ Correção de Perspectiva
- Clique nos **4 cantos** da página na ordem: ↖️ ↗️ ↘️ ↙️
- Seja **preciso** na seleção dos pontos
- Use **"Resetar Pontos"** se errar

### ✅ Juntar Imagens
- **Horizontal**: páginas lado a lado (mais comum)
- **Vertical**: páginas uma sobre a outra
- **Sobreposição**: use se há texto repetido entre páginas

## 🆘 Problemas Comuns

| Problema | Solução |
|----------|---------|
| Programa não abre | Instale: `pip install opencv-python pillow` |
| Erro ao carregar imagem | Verifique se é JPG, PNG, BMP ou TIFF |
| Perspectiva ruim | Selecione pontos mais precisos |
| Imagens desalinhadas | Ajuste alinhamento e sobreposição |

## 📁 Formatos Recomendados

- **Entrada**: JPG (fotos), PNG (qualidade)
- **Saída**: PNG (melhor qualidade), JPG (menor tamanho)

## 🔧 Requisitos Mínimos

- Python 3.7+
- 4GB RAM (para imagens grandes)
- Interface gráfica (Windows/Mac/Linux Desktop)

---
💡 **Dica**: Mantenha as fotos originais como backup!

