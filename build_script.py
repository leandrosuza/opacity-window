#!/usr/bin/env python3
"""
Script automatizado para criar o executável do Controlador de Transparência
"""

import os
import sys
import subprocess
import shutil

def check_requirements():
    """Verificar se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import win32gui
        print("✅ win32gui encontrado")
    except ImportError:
        print("❌ win32gui não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"])
    
    try:
        import psutil
        print("✅ psutil encontrado")
    except ImportError:
        print("❌ psutil não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "psutil"])

def clean_build_files():
    """Limpar arquivos de build anteriores"""
    print("🧹 Limpando arquivos de build anteriores...")
    
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['OpacityWindow.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removido: {dir_name}/")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ Removido: {file_name}")

def build_executable():
    """Criar o executável"""
    print("🏗️ Criando executável...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=window.ico",
        "--name=OpacityWindow",
        "--add-data=window.ico;.",
        "--hidden-import=win32gui",
        "--hidden-import=win32con",
        "--hidden-import=win32api",
        "--hidden-import=win32process",
        "--hidden-import=psutil",
        "--hidden-import=ctypes",
        "window_opacity_controller.py"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Executável criado com sucesso!")
        return True
    else:
        print("❌ Erro ao criar executável:")
        print(result.stderr)
        return False

def verify_executable():
    """Verificar se o executável foi criado corretamente"""
    exe_path = "dist/OpacityWindow.exe"
    
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"✅ Executável criado: {exe_path}")
        print(f"📏 Tamanho: {size:.1f} MB")
        return True
    else:
        print("❌ Executável não encontrado!")
        return False

def main():
    """Função principal"""
    print("🎛️ Controlador de Transparência - Build Script")
    print("=" * 50)
    
    # Verificar dependências
    check_requirements()
    
    # Limpar arquivos anteriores
    clean_build_files()
    
    # Criar executável
    if build_executable():
        # Verificar resultado
        if verify_executable():
            print("\n🎉 Build concluído com sucesso!")
            print("📁 Executável: dist/OpacityWindow.exe")
            print("🚀 Pronto para distribuição!")
        else:
            print("\n❌ Falha na verificação do executável")
            sys.exit(1)
    else:
        print("\n❌ Falha na criação do executável")
        sys.exit(1)

if __name__ == "__main__":
    main() 