import requests
import base64
import json
import os
from datetime import datetime 
from route.dadosDeconexao import tokenIXC, hostIXC

def finalizar_pela_OS(arquivo_entrada_json):
    host = hostIXC
    token = tokenIXC
    
    if arquivo_entrada_json is None:
        caminho_pasta = os.path.dirname(os.path.abspath(__file__))
        arquivo_entrada_json = os.path.join(caminho_pasta, 'src', 'tickets_OS_abertos.json')
    
    headers = {
        'Authorization': 'Basic {}'.format(base64.b64encode(token).decode('utf-8')),
        'Content-Type': 'application/json'
    }

    try:
        with open(arquivo_entrada_json, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
        
        if not tickets:
            print("Nenhuma OS encontrada para finalizar.")
            return
        
        for ticket in tickets:
            # Obtém o ID da OS do campo "id"
            os_id = ticket.get('id')
            if not os_id:
                print(f"OS sem ID encontrada: {ticket}")
                continue
            
            # Formata a data atual no formato DD/MM/YYYY HH:MM:SS
            data_hora_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            
            # Usa a data de abertura como data_inicio se existir
            data_inicio = data_hora_atual  # Valor padrão é agora
            if ticket.get('data_abertura'):
                try:
                    dt_abertura = datetime.strptime(ticket['data_abertura'], '%Y-%m-%d %H:%M:%S')
                    data_inicio = dt_abertura.strftime('%d/%m/%Y %H:%M:%S')
                except ValueError:
                    pass
            
            url = f"https://{host}/webservice/v1/su_oss_chamado_fechar"
            
            # Payload ajustado com o campo que a API espera para ID da OS
            payload = {
                "id_chamado": str(os_id),  # Alterado de "id_ticket" para "id"
                "data_inicio": data_inicio,
                "data_final": data_hora_atual,
                "mensagem": "Atendimento finalizado via script",
                "id_tecnico": "96",
                "id_proxima_tarefa": "425",
                "finaliza_processo_aux": "S",
                "status": "F"
            }
            
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers
            )
            
            resposta_json = response.json()
            if response.status_code == 200 and resposta_json.get('type') != 'error':
                print(f"OS ID {os_id} finalizada com sucesso.")
                print(f"Resposta: {resposta_json}")
            else:
                print(f"Erro ao finalizar OS ID {os_id}:")
                print(f"Status Code: {response.status_code}")
                print(f"Resposta: {resposta_json}")
        
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo_entrada_json}")
    except json.JSONDecodeError as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")