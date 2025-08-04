# 🏗️ Como Criar o Executável

## Pré-requisitos

1. **Python 3.8+** instalado
2. **Dependências** instaladas:
   ```bash
   pip install -r requirements.txt
   ```
3. **PyInstaller** instalado:
   ```bash
   pip install pyinstaller
   ```

## 🚀 Criando o Executável

### Método 1: Comando Direto

```bash
pyinstaller --onefile --windowed --icon=window.ico --name=OpacityWindow window_opacity_controller.py
```

### Método 2: Script Automatizado

1. Execute o script de build:
   ```bash
   python build_script.py
   ```

2. O executável será criado em `dist/OpacityWindow.exe`

## 📁 Arquivos Gerados

- `dist/OpacityWindow.exe` - Executável final
- `build/` - Arquivos temporários (pode ser deletado)
- `OpacityWindow.spec` - Arquivo de configuração (pode ser deletado)

## 🎨 Incluindo o Ícone

O ícone `window.ico` é automaticamente incluído no executável usando o parâmetro `--icon=window.ico`.

## 🔧 Opções Avançadas

### Executável com Console (para debug)
```bash
pyinstaller --onefile --icon=window.ico --name=OpacityWindow window_opacity_controller.py
```

### Executável Otimizado
```bash
pyinstaller --onefile --windowed --icon=window.ico --name=OpacityWindow --optimize=2 window_opacity_controller.py
```

## ✅ Verificação

Após criar o executável:

1. Teste o arquivo `dist/OpacityWindow.exe`
2. Verifique se o ícone aparece corretamente
3. Confirme que todas as funcionalidades estão funcionando

## 🧹 Limpeza

Para limpar arquivos temporários:

```bash
# Windows
rmdir /s /q build
del OpacityWindow.spec

# Linux/Mac
rm -rf build
rm OpacityWindow.spec
```

---

**Nota**: O executável final está pronto para distribuição e não requer Python instalado no sistema de destino. 