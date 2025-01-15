
import argparse
import subprocess
import sys
from scanner.utils.logger import logger

def check_and_install_dependencies():
    """
    Verifica e instala dependências automaticamente.
    """
    required_packages = ["requests", "pdfkit", "pyyaml", "tqdm", "beautifulsoup4"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            logger.info(f"[Setup] Instalando dependência: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    # Garantir que dependências estão instaladas
    check_and_install_dependencies()

    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description="Scanner de Vulnerabilidades Web com Instalação Automática")
    parser.add_argument("-u", "--url", required=True, help="URL alvo. Ex: http://example.com")
    parser.add_argument("-m", "--modulos", nargs="*", help="Lista de módulos (sqli, xss, auth). Se vazio, executa todos.")
    parser.add_argument("-o", "--output", help="Nome do arquivo de relatório (PDF ou HTML). Ex: report.pdf ou report.html")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Número de threads (padrão: 5).")
    parser.add_argument("-c", "--config", default="scanner/config/default.yaml", help="Arquivo de configuração YAML.")

    args = parser.parse_args()

    # Log básico para exibir argumentos recebidos
    logger.info(f"[Main] URL Alvo: {args.url}")
    logger.info(f"[Main] Módulos: {args.modulos or 'Todos'}")
    logger.info(f"[Main] Threads: {args.threads}")
    logger.info(f"[Main] Configuração: {args.config}")
    
    # TODO: Adicionar lógica principal do scanner aqui (chamar módulos core)

if __name__ == "__main__":
    main()
