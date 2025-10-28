#script desenvolvido por Guilherme Wallace Souza Costa (https://github.com/guilherme-wallace)

import logging
from datetime import datetime
import csv
from public.obter_dados_atendimento import obter_dados_atendimento
from public.obter_dados_OS import obter_dados_OS
from public.finalizar_pela_OS import finalizar_pela_OS
from public.finalizar_pelo_atendimento import finalizar_pelo_atendimento
from public.abrir_atendimento_lote import abrir_atendimentos_csv

caminho = ''

logging.basicConfig(filename=f'{caminho}src/executa_script.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def filtrar_clientes_por_data(arquivo_entrada, arquivo_saida, data_inicio_str, data_fim_str):
    """
    Filtra um arquivo CSV de clientes pela coluna 'Data Cancelamento' 
    e salva o resultado em um novo arquivo.
    """
    logging.info(f"Iniciando filtro de clientes do arquivo '{arquivo_entrada}'...")
    logging.info(f"Período de cancelamento: {data_inicio_str} a {data_fim_str}")
    
    try:
        data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        
        clientes_filtrados = []
        headers = []
        
        with open(arquivo_entrada, mode='r', encoding='utf-8-sig') as f_in:
            reader = csv.DictReader(f_in)
            headers = reader.fieldnames
            
            if "Data Cancelamento" not in headers:
                logging.error(f"Erro no filtro: A coluna 'Data Cancelamento' não foi encontrada no arquivo CSV.")
                return None

            for row in reader:
                data_cancel_str = row.get("Data Cancelamento")
                
                if not data_cancel_str:
                    logging.warning(f"Cliente {row.get('ID Cliente')} ignorado (filtro): 'Data Cancelamento' está vazia.")
                    continue
                    
                try:
                    data_cancel = datetime.strptime(data_cancel_str, '%m/%d/%Y').date()
                except ValueError:
                    logging.error(f"Cliente {row.get('ID Cliente')} ignorado (filtro): Formato de data inválido '{data_cancel_str}'. Esperado MM/DD/YYYY.")
                    continue
                    
                if data_inicio <= data_cancel <= data_fim:
                    clientes_filtrados.append(row)
        
        if not clientes_filtrados:
             logging.warning("Nenhum cliente encontrado para o período de data especificado. Nenhum arquivo de saída foi gerado.")
             return None

        with open(arquivo_saida, mode='w', encoding='utf-8-sig', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=headers)
            writer.writeheader()
            writer.writerows(clientes_filtrados)
            
        logging.info(f"Filtro concluído. {len(clientes_filtrados)} clientes salvos em '{arquivo_saida}'.")
        return arquivo_saida

    except FileNotFoundError:
        logging.error(f"Erro no filtro: Arquivo de entrada '{arquivo_entrada}' não encontrado.")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado durante o filtro de datas: {e}")
        return None


def main():
    try:
        logging.info("Início da execução do script.")
        arquivo_saida_pega = f'{caminho}src/pegaAtendimentosResultado.json'
        tickets_finalizados = f'{caminho}src/tickets_finalizados.json'
        tickets_OS_abertos = f'{caminho}src/tickets_OS_abertos.json'


        # 1. Define o período (formato 'YYYY-MM-DD')
        data_inicio_filtro = "2025-01-01"
        data_fim_filtro = "2025-10-29"

        arquivo_csv_original = f'{caminho}src/IXC_inadimplente_sem_recolhimento.csv'
        arquivo_csv_filtrado = f'{caminho}src/clientes_filtrados_para_abertura.csv'
        arquivo_para_processar = filtrar_clientes_por_data(
            arquivo_csv_original,
            arquivo_csv_filtrado,
            data_inicio_filtro,
            data_fim_filtro
        )
        
        # -----------------------------------------------------------

        #obter_dados_atendimento(arquivo_saida_pega)
        #logging.info(f"Dados do Atendimento obtidos e salvos em {arquivo_saida_pega}.")

        #obter_dados_OS(tickets_finalizados, tickets_OS_abertos)
        #logging.info(f"Dados da OS obtidos e salvos em {tickets_OS_abertos}.")

        #finalizar_pela_OS(tickets_OS_abertos)

        #finalizar_pelo_atendimento(tickets_finalizados)
        
        # 4. Nova função para abrir atendimentos em lote
        if arquivo_para_processar:
            abrir_atendimentos_csv(arquivo_para_processar)
            logging.info(f"Processo de abertura de tickets (filtrado) do arquivo {arquivo_para_processar}.")
        else:
            logging.warning("Abertura de atendimentos não executada: Nenhum cliente foi selecionado pelo filtro de data.")

        logging.info(f"Script finalizado")
    except Exception as e:
        logging.error(f"Erro durante a execução do script: {e}")

    logging.info("Execução do script concluída.")

if __name__ == "__main__":
    main()