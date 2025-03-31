import requests
import base64
import json
import os
from route.dadosDeconexao import tokenIXC, hostIXC

def obter_dados_OS(arquivo_tickets, arquivo_saida):
    host = hostIXC
    token = tokenIXC
    
    # Caminhos dos arquivos
    caminho_pasta = os.path.dirname(os.path.abspath(__file__))
    caminho_tickets = os.path.join(arquivo_tickets)
    caminho_saida = os.path.join(arquivo_saida)
    
    headers = {
        'ixcsoft': 'listar',
        'Authorization': 'Basic {}'.format(base64.b64encode(token).decode('utf-8')),
        'Content-Type': 'application/json'
    }

    try:
        # 1. Ler os tickets do arquivo JSON
        with open(caminho_tickets, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
        
        if not tickets:
            print("Nenhum ticket encontrado no arquivo.")
            return []
        
        # 2. Para cada ticket, buscar as OS relacionadas
        todas_os = []
        
        for ticket in tickets:
            ticket_id = ticket.get('id_ticket')
            if not ticket_id:
                continue
            
            # Consulta as OS para o ticket específico
            url = f"https://{host}/webservice/v1/su_oss_chamado"
            payload = {
                'qtype': 'su_oss_chamado.id_ticket',
                'query': str(ticket_id),
                'oper': '=',
                'page': '1',
                'rp': '100',
                'grid_param': json.dumps([
                    {
                        "TB": "su_oss_chamado.status",
                        "OP": "!=",
                        "P": "F"  # OS não finalizadas
                    }
                ]),
                'sortname': 'su_oss_chamado.id',
                'sortorder': 'asc'
            }
            
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            
            os_data = response.json()
            
            # Adiciona informações adicionais sobre o ticket relacionado
            for os_item in os_data.get('registros', []):
                os_item['ticket_relacionado'] = {
                    'id_ticket': ticket_id,
                    'mensagem': ticket.get('mensagem', '')
                }
                todas_os.append(os_item)
        
        # 3. Salva as OS encontradas
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            json.dump(todas_os, f, ensure_ascii=False, indent=4)
        
        print(f"OS relacionadas salvas em: {caminho_saida}")
        print(f"Total de OS encontradas: {len(todas_os)}")
        
        return todas_os
        
    except FileNotFoundError:
        print(f"Arquivo de tickets não encontrado: {caminho_tickets}")
    except json.JSONDecodeError as e:
        print(f"Erro ao ler JSON: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {e}")
        if 'response' in locals():
            print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"Erro inesperado: {e}")