# 📚 Digitalização de Livros - Interface Web Moderna

Uma interface web moderna e unificada para digitalização de livros antigos, substituindo as aplicações desktop anteriores com uma experiência superior.

## ✨ Funcionalidades

### 🔧 Correção de Perspectiva
- Upload de imagens via drag & drop
- Seleção interativa de pontos de referência
- Visualização com zoom e pan
- Processamento em tempo real
- Download da imagem corrigida

### 🔗 Combinação de Imagens
- Upload de múltiplas imagens
- Orientação horizontal/vertical
- Opções de alinhamento
- Controle de sobreposição
- Preview do resultado

## 🚀 Tecnologias

- **React 18** - Framework frontend
- **Tailwind CSS** - Estilização
- **shadcn/ui** - Componentes UI
- **Lucide React** - Ícones
- **Canvas API** - Processamento de imagens
- **Vite** - Build tool

## 🛠 Instalação e Uso

### Pré-requisitos
- Node.js 18+
- pnpm (recomendado) ou npm

### Desenvolvimento Local
```bash
# Instalar dependências
pnpm install

# Iniciar servidor de desenvolvimento
pnpm run dev

# Abrir http://localhost:5173
```

### Build para Produção
```bash
# Gerar build otimizado
pnpm run build

# Preview do build
pnpm run preview
```

## 📁 Estrutura do Projeto

```
src/
├── components/
│   ├── ui/              # Componentes shadcn/ui
│   ├── ImageUpload.jsx  # Upload de imagens
│   └── ImageViewer.jsx  # Visualizador interativo
├── utils/
│   └── imageProcessing.js # Lógica de processamento
├── App.jsx              # Componente principal
├── App.css              # Estilos globais
└── main.jsx             # Entry point
```

## 🎯 Vantagens sobre a Versão Desktop

- ✅ **Zero instalação** - funciona no navegador
- ✅ **Multiplataforma** - desktop, tablet, mobile
- ✅ **Interface moderna** - design responsivo
- ✅ **Funcionalidades unificadas** - tudo em um lugar
- ✅ **Atualizações automáticas** - sempre a versão mais recente
- ✅ **Compartilhamento fácil** - apenas enviar URL

## 🔧 Como Usar

### Correção de Perspectiva
1. Clique na aba "Correção de Perspectiva"
2. Faça upload da imagem da página
3. Clique nos 4 cantos da página na ordem indicada
4. Clique em "Corrigir Perspectiva"
5. Baixe o resultado

### Combinação de Imagens
1. Clique na aba "Combinar Páginas"
2. Faça upload das duas imagens
3. Configure orientação e alinhamento
4. Clique em "Combinar Imagens"
5. Baixe o resultado

## 🚀 Deploy

A aplicação pode ser deployada em qualquer serviço de hospedagem estática:

- **Netlify**: Arraste a pasta `dist` após o build
- **Vercel**: Conecte o repositório Git
- **GitHub Pages**: Configure GitHub Actions
- **Servidor próprio**: Sirva a pasta `dist`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências estão instaladas
2. Confirme que está usando Node.js 18+
3. Tente limpar o cache: `pnpm run build --force`

---

**Desenvolvido para facilitar a preservação digital de livros antigos** 📖✨

