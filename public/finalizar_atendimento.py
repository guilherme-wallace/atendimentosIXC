import requests
import base64
import json
import os
from route.dadosDeconexao import tokenIXC, hostIXC

def finalizar_atendimento(arquivo_entrada_json=None):
    host = hostIXC
    token = tokenIXC
    
    if arquivo_entrada_json is None:
        caminho_pasta = os.path.dirname(os.path.abspath(__file__))
        arquivo_entrada_json = os.path.join(caminho_pasta, 'src', 'tickets_finalizados.json')
    
    headers = {
        'Authorization': 'Basic {}'.format(base64.b64encode(token).decode('utf-8')),
        'Content-Type': 'application/json'
    }

    try:
        with open(arquivo_entrada_json, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
        
        if not tickets:
            print("Nenhum ticket encontrado para finalizar.")
            return
        
        for ticket in tickets:
            ticket_id = ticket.get('id_ticket')
            if not ticket_id:
                continue
                
            url_mensagem = f"https://{host}/webservice/v1/su_mensagens"
            
            payload_mensagem = {
                "id_ticket": str(ticket_id),
                "mensagem": ticket.get("mensagem", "Atendimento finalizado via script"),
                "su_status": ticket.get("su_status", "S")
            }
            
            response = requests.post(
                url_mensagem,
                data=json.dumps(payload_mensagem),
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"Ticket ID {ticket_id} finalizado com sucesso.")
            else:
                print(f"Erro ao finalizar ticket ID {ticket_id}:")
                print(f"Status Code: {response.status_code}")
                print(f"Resposta: {response.text}")
        
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo_entrada_json}")
    except json.JSONDecodeError as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")