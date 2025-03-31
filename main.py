#script desenvolvido por Guilherme Wallace Souza Costa (https://github.com/guilherme-wallace)

import logging
from datetime import datetime
from public.obter_dados_atendimento import obter_dados_atendimento
from public.obter_dados_OS import obter_dados_OS
from public.finalizar_pela_OS import finalizar_pela_OS
from public.finalizar_pelo_atendimento import finalizar_pelo_atendimento

caminho = ''

logging.basicConfig(filename=f'{caminho}src/executa_script.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Início da execução do script.")
        arquivo_saida_pega = f'{caminho}src/pegaAtendimentosResultado.json'
        tickets_finalizados = f'{caminho}src/tickets_finalizados.json'
        tickets_OS_abertos = f'{caminho}src/tickets_OS_abertos.json'

        obter_dados_atendimento(arquivo_saida_pega)
        logging.info(f"Dados do Atendimento obtidos e salvos em {arquivo_saida_pega}.")

        obter_dados_OS(tickets_finalizados, tickets_OS_abertos)
        logging.info(f"Dados da OS obtidos e salvos em {tickets_OS_abertos}.")

        #finalizar_pela_OS(tickets_OS_abertos)

        finalizar_pelo_atendimento(tickets_finalizados)
        logging.info(f"Script finalizado")
    except Exception as e:
        logging.error(f"Erro durante a execução do script: {e}")

    logging.info("Execução do script concluída.")

if __name__ == "__main__":
    main()
