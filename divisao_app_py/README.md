# Programas para Digitalização de Livros Antigos

Este pacote contém dois programas Python com interface gráfica desenvolvidos para auxiliar na digitalização de livros antigos, especialmente aqueles em que o conteúdo do texto passa continuamente de uma página para a outra.

## Programas Incluídos

### 1. Correção de Perspectiva (`correcao_perspectiva.py`)
Programa para corrigir a perspectiva de páginas fotografadas, eliminando distorções trapezoidais e de ângulo.

### 2. Juntar Imagens (`juntar_imagens.py`)
Programa para combinar duas imagens de páginas em uma única imagem, permitindo junção horizontal ou vertical.

## Requisitos do Sistema

### Requisitos de Software
- Python 3.7 ou superior
- Sistema operacional: Windows, macOS ou Linux
- Interface gráfica disponível (não funciona em servidores sem GUI)

### Bibliotecas Python Necessárias
```bash
pip install opencv-python pillow
```

**Nota:** Se você já tem o NumPy instalado, ele será usado automaticamente. Caso contrário, será instalado junto com o OpenCV.

## Instalação

1. **Instalar Python**: Certifique-se de ter Python 3.7+ instalado em seu sistema
2. **Instalar dependências**: Execute o comando acima para instalar as bibliotecas necessárias
3. **Baixar os programas**: Coloque os arquivos `correcao_perspectiva.py` e `juntar_imagens.py` em uma pasta de sua escolha

## Como Usar

### Programa de Correção de Perspectiva

#### Execução
```bash
python correcao_perspectiva.py
```

#### Passo a Passo
1. **Carregar Imagem**: Clique em "Carregar Imagem" e selecione a foto da página que deseja corrigir
2. **Selecionar Pontos**: Clique nos 4 cantos da página na seguinte ordem:
   - Superior esquerdo
   - Superior direito  
   - Inferior direito
   - Inferior esquerdo
3. **Corrigir**: Clique em "Corrigir Perspectiva" para aplicar a transformação
4. **Salvar**: Clique em "Salvar Imagem" para salvar o resultado

#### Dicas Importantes
- Selecione os pontos com precisão para obter melhores resultados
- Os pontos devem formar um quadrilátero que represente a área da página
- Use "Resetar Pontos" se precisar recomeçar a seleção
- A imagem corrigida aparecerá no painel direito

### Programa para Juntar Imagens

#### Execução
```bash
python juntar_imagens.py
```

#### Passo a Passo
1. **Carregar Imagens**: 
   - Clique em "Carregar Imagem 1" para a primeira página
   - Clique em "Carregar Imagem 2" para a segunda página
2. **Configurar Opções**:
   - **Orientação**: Escolha "Horizontal" para páginas lado a lado ou "Vertical" para páginas uma sobre a outra
   - **Alinhamento**: Define como as imagens serão alinhadas (início, centro, fim)
   - **Sobreposição**: Ajuste em pixels se houver conteúdo que se sobrepõe entre as páginas
3. **Combinar**: Clique em "Combinar Imagens" para gerar o resultado
4. **Salvar**: Clique em "Salvar Resultado" para salvar a imagem combinada

#### Opções Avançadas
- **Sobreposição**: Use valores positivos (ex: 50px) quando há conteúdo que se repete entre as páginas
- **Alinhamento**: 
  - "Início" = alinha pela borda superior/esquerda
  - "Centro" = centraliza as imagens
  - "Fim" = alinha pela borda inferior/direita

## Fluxo de Trabalho Recomendado

Para digitalizar um livro antigo com páginas contínuas:

1. **Fotografar**: Tire fotos individuais de cada página do livro
2. **Corrigir Perspectiva**: Use o primeiro programa para corrigir a perspectiva de cada foto
3. **Juntar Páginas**: Use o segundo programa para combinar páginas que formam uma unidade de leitura
4. **Organizar**: Salve os resultados com nomes organizados (ex: pagina_001_002.png)

## Formatos Suportados

### Entrada (Leitura)
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

### Saída (Salvamento)
- PNG (recomendado para melhor qualidade)
- JPEG (menor tamanho de arquivo)
- TIFF (para arquivamento)

## Solução de Problemas

### Erro ao Carregar Imagem
- Verifique se o arquivo não está corrompido
- Certifique-se de que o formato é suportado
- Tente converter a imagem para PNG usando outro software

### Programa Não Abre
- Verifique se Python está instalado corretamente
- Confirme se as dependências foram instaladas: `pip list | grep opencv`
- Em sistemas Linux, pode ser necessário instalar: `sudo apt-get install python3-tk`

### Resultado da Correção Não Satisfatório
- Selecione os pontos com mais precisão
- Certifique-se de que os 4 pontos formam um quadrilátero válido
- Tente selecionar pontos ligeiramente dentro das bordas da página

### Imagens Não Se Alinham Bem na Junção
- Verifique se ambas as imagens têm orientação similar
- Use a opção de sobreposição para ajustar conteúdo repetido
- Experimente diferentes opções de alinhamento

## Limitações

- Os programas requerem interface gráfica (não funcionam via SSH sem X11)
- Imagens muito grandes podem consumir bastante memória
- A correção de perspectiva funciona melhor com distorções moderadas
- Para livros com curvatura acentuada, pode ser necessário pré-processamento adicional

## Suporte

Para problemas técnicos ou sugestões de melhorias, verifique:
1. Se todas as dependências estão instaladas corretamente
2. Se a versão do Python é compatível (3.7+)
3. Se há mensagens de erro específicas no terminal

## Licença

Estes programas são fornecidos como estão, para uso pessoal e educacional. Desenvolvidos pela Manus AI para auxiliar na preservação digital de livros antigos.

