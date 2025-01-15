
import pdfkit
from scanner.utils.logger import logger

def gerar_relatorio_pdf(resultados, nome_arquivo):
    """
    Generate a PDF containing a summary of vulnerabilities with recommendations.
    """
    logger.info("[Relatório] Gerando PDF com recomendações...")
    html = '''<html><head><meta charset="utf-8">
    <title>Relatório de Vulnerabilidades</title></head><body>
    <h1>Relatório de Vulnerabilidades</h1><hr><ul>'''
    
    for r in resultados:
        vuln_name = r.get("vuln", "N/A")
        url = r.get("url", "")
        payload = r.get("payload", "")
        fragment = r.get("response_fragment", "").replace("<", "&lt;").replace(">", "&gt;")
        recommendation = "N/A"

        # Add recommendations for specific vulnerabilities
        if vuln_name == "SQL Injection":
            recommendation = "Utilize consultas parametrizadas (prepared statements) para evitar SQL Injection."
        elif vuln_name == "XSS Refletido":
            recommendation = "Sanitize todas as entradas de usuários e escape caracteres HTML na saída."
        elif vuln_name == "Credenciais padrão aceitas":
            recommendation = "Desative ou altere as credenciais padrão e implemente autenticação forte."
        
        html += f'''
        <li>
            <strong>Vulnerabilidade:</strong> {vuln_name}<br>
            <strong>URL:</strong> {url}<br>
            <strong>Payload:</strong> {payload}<br>
            <strong>Resposta (trecho):</strong> <pre>{fragment}</pre><br>
            <strong>Recomendação:</strong> {recommendation}
        </li>
        <hr>
        '''
    html += "</ul></body></html>"

    pdfkit.from_string(html, nome_arquivo)
