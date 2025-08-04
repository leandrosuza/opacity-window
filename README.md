# 🎛️ Controlador de Transparência

Um aplicativo moderno e intuitivo para controlar a transparência de janelas no Windows, permitindo maximizar sua produtividade com monitor único.

![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Windows](https://img.shields.io/badge/windows-10+-red)
![Licença](https://img.shields.io/badge/licença-MIT-yellow)

## ✨ Características

- 🎨 **Interface Moderna**: Design dark mode com elementos visuais modernos
- 📋 **Detecção Automática**: Lista automaticamente todas as janelas abertas
- 🎚️ **Controle Preciso**: Slider para ajustar transparência de 0% a 100%
- 🔄 **Gerenciamento Inteligente**: Acompanha janelas com transparência aplicada
- ⚡ **Atualização em Tempo Real**: Lista de janelas atualizada automaticamente
- 🎯 **Filtros Inteligentes**: Opção para mostrar apenas processos .exe
- 🛡️ **Seguro**: Não afeta janelas do sistema críticas
- 🎨 **Ícone Personalizado**: Interface visual profissional

## 🚀 Instalação

### Opção 1: Executável (Recomendado)

1. Baixe o arquivo `OpacityWindow.exe` da pasta `dist/`
2. Execute o arquivo diretamente (não requer instalação)
3. Pronto para usar! 🎉

### Opção 2: Código Fonte

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/opacity-window.git
cd opacity-window
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o programa:
```bash
python window_opacity_controller.py
```

## 📋 Requisitos

- **Sistema Operacional**: Windows 10 ou superior
- **Python**: 3.8+ (apenas para execução do código fonte)
- **Dependências**: Ver `requirements.txt`

## 🎮 Como Usar

### Interface Principal

1. **Janelas Disponíveis**: Lista todas as janelas abertas no sistema
2. **Janelas com Transparência**: Mostra janelas que já têm transparência aplicada
3. **Controle de Transparência**: Slider para ajustar o nível (0-100%)
4. **Botões de Ação**: Aplicar, Resetar, Resetar Todas, Atualizar

### Passo a Passo

1. **Selecionar Janela**: Clique em uma janela na lista "Janelas Disponíveis"
2. **Ajustar Transparência**: Use o slider para definir o nível desejado
3. **Aplicar**: Clique em "✅ Aplicar" para aplicar a transparência
4. **Gerenciar**: Use os botões para resetar transparências quando necessário

### Funcionalidades

- **✅ Aplicar**: Aplica transparência à janela selecionada
- **🔄 Resetar**: Remove transparência da janela selecionada
- **🔄 Resetar Todas**: Remove transparência de todas as janelas
- **🔄 Atualizar**: Atualiza a lista de janelas disponíveis

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
opacity-window/
├── window_opacity_controller.py  # Código principal
├── requirements.txt              # Dependências Python
├── window.ico                   # Ícone da aplicação
├── dist/
│   └── OpacityWindow.exe        # Executável final
├── README.md                    # Este arquivo
├── LICENSE                      # Licença MIT
└── .gitignore                   # Arquivos ignorados pelo Git
```

### Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Tkinter**: Interface gráfica
- **win32gui**: Controle de janelas Windows
- **psutil**: Informações de processos
- **PyInstaller**: Criação do executável

### Criando o Executável

Para criar o executável com ícone personalizado:

```bash
pyinstaller --onefile --windowed --icon=window.ico --name=OpacityWindow window_opacity_controller.py
```

## 🔧 Configuração

### Personalização de Cores

O aplicativo usa um tema dark moderno com as seguintes cores:

```python
colors = {
    'bg_dark': '#0f172a',        # Fundo escuro
    'bg_medium': '#1e293b',      # Fundo médio
    'primary': '#6366f1',        # Cor primária
    'success': '#10b981',        # Verde (sucesso)
    'warning': '#f59e0b',        # Amarelo (aviso)
    'danger': '#ef4444',         # Vermelho (perigo)
}
```

### Filtros de Janelas

O aplicativo automaticamente filtra:
- Janelas do próprio aplicativo
- Janelas do sistema críticas
- Janelas sem título

## 🐛 Solução de Problemas

### Problema: Janela não aparece na lista
**Solução**: Verifique se a janela está visível e não é uma janela do sistema

### Problema: Transparência não é aplicada
**Solução**: Certifique-se de que a janela suporta transparência (não é uma janela do sistema)

### Problema: Erro de permissão
**Solução**: Execute o aplicativo como administrador

### Problema: Ícone não aparece
**Solução**: Use o executável da pasta `dist/` que já inclui o ícone

## 📝 Changelog

### v1.0.0 (2025-01-04)
- ✅ Interface moderna com tema dark
- ✅ Detecção automática de janelas
- ✅ Controle de transparência 0-100%
- ✅ Gerenciamento de janelas com transparência
- ✅ Filtros inteligentes
- ✅ Ícone personalizado
- ✅ Executável standalone
- ✅ Atualização em tempo real

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Comunidade Python
- Desenvolvedores do win32gui
- Contribuidores do PyInstaller
- Todos que testaram e deram feedback

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões:

1. Abra uma [Issue](https://github.com/seu-usuario/opacity-window/issues)
2. Descreva o problema detalhadamente
3. Inclua informações do sistema (Windows, versão, etc.)

---

**Desenvolvido com ❤️ para a comunidade Windows** 