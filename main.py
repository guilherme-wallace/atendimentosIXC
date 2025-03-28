#script desenvolvido por Guilherme Wallace Souza Costa (https://github.com/guilherme-wallace)

import logging
from datetime import datetime
from public.obter_dados_atendimento import obter_dados_atendimento
from public.finalizar_atendimento import finalizar_atendimento

caminho = ''

logging.basicConfig(filename=f'{caminho}src/executa_script.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Início da execução do script.")

        arquivo_saida_pega = f'{caminho}src/pegaAtendimentosResultado.json'
        obter_dados_atendimento(arquivo_saida_pega)
        logging.info(f"Dados obtidos e salvos em {arquivo_saida_pega}.")

        arquivo_entrada_json_finalizar = f'{caminho}src/tickets_finalizados.json'
        finalizar_atendimento(arquivo_entrada_json_finalizar)
        logging.info(f"Script finalizado")
    except Exception as e:
        logging.error(f"Erro durante a execução do script: {e}")

    logging.info("Execução do script concluída.")

if __name__ == "__main__":
    main()
