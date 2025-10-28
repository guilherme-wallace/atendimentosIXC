# public/abrir_atendimento_lote.py 
import requests
import base64
import json
import csv
import logging
from route.dadosDeconexao import urlIXC, tokenIXC

def abrir_atendimentos_csv(arquivo_csv):
    """
    Abre chamados no IXC com base em uma lista de clientes de um arquivo CSV.
    """
    logging.info(f"Iniciando abertura de atendimentos em lote do arquivo: {arquivo_csv}")
    
    try:
        host = urlIXC
        token = tokenIXC
        url = f"{host}/webservice/v1/su_mensagens" 

        headers = {
            'ixcsoft': 'incluir',
            'Authorization': 'Basic {}'.format(base64.b64encode(token).decode('utf-8')),
            'Content-Type': 'application/json'
        }

        mensagem_padrao = "Contrato cancelado por inadimplência, favor verificar se possui equipamentos para serem recolhidos. -> Atendimento gerado via Script. "
        titulo_padrao = "RECOLHER EQUIPAMENTOS"

        with open(arquivo_csv, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            total_clientes = 0
            sucessos = 0
            
            for row in reader:
                total_clientes += 1
                id_cliente = row.get("ID Cliente")
                nome_cliente = row.get("Cliente")

                if not id_cliente:
                    logging.warning(f"Linha {reader.line_num} ignorada: 'ID Cliente' está vazio.")
                    continue

                payload = {
                    "id_cliente": id_cliente.strip(),
                    "assunto_ticket": "16",
                    "id_assunto": "16",
                    "id_wfl_processo": "23",
                    "titulo": titulo_padrao,
                    "origem_endereco": "C", 
                    "status": "OSAB",      
                    "su_status": "EP",                  
                    "id_ticket_setor": "4",             
                    "prioridade": "M",                  
                    "id_responsavel_tecnico": "96",     
                    "id_filial": "1",                   
                    "id_usuarios": "11",
                    "tipo": "C", 
                    "menssagem": mensagem_padrao
                }
                
                try:
                    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)
                    
                    json_data = {}
                    try:
                        json_data = response.json()
                    except ValueError:
                        logging.error(f"Falha ao decodificar JSON para Cliente ID {id_cliente}. Status: {response.status_code}, Resposta: {response.text}")
                        continue

                    if (response.status_code == 200 or response.status_code == 201) and json_data.get("type") != "error":
                        logging.info(f"Sucesso! Ticket aberto para Cliente ID {id_cliente} ({nome_cliente}). Resposta: {response.text}")
                        sucessos += 1
                    else:
                        error_message = json_data.get("message", response.text)
                        logging.error(f"Falha ao abrir ticket para Cliente ID {id_cliente}. Status: {response.status_code}, API Error: {error_message}")
                        logging.error(f"Payload enviado: {json.dumps(payload)}")
                
                except requests.exceptions.RequestException as e:
                    logging.error(f"Erro de conexão ao tentar abrir ticket para Cliente ID {id_cliente}: {e}")

            logging.info(f"Processo de abertura em lote concluído. {sucessos} de {total_clientes} tickets abertos com sucesso.")

    except FileNotFoundError:
        logging.error(f"Erro: O arquivo CSV '{arquivo_csv}' não foi encontrado.")
    except Exception as e:
        logging.error(f"Erro inesperado no script de abertura de atendimentos: {e}")