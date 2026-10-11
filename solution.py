from datetime import datetime, timedelta
import requests

# PROFESSOR, VI QUE ERA PRA UTILIZAR SOMENTE AS BIBLIOTECAS ACIMA, PORÉM TIVE PROBLEMAS
# AO RODAR O LOOP VARIAS VEZES SEM UMA PEQUENA PAUSA (A API BARRA AS REQUISIÇÕES), ENTÃO USEI O TIME
import time


def cotar():
    # Pegando a data da execução da função
    data_hoje = datetime.today()
    # Transformando para o formato correto aceitado pela api
    data_atual = data_hoje.strftime("%m-%d-%Y")

    # forzinho para os 365 dias
    for i in range(365):
        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?%40dataCotacao='{data_atual}'&%24format=json"

        # try e except para tratamento de algum erro inesperado
        try:
            res = requests.get(url).json()

            # Tratamento para caso algum valor apareça em vazio, geralmente fim de semana/feriado
            if not res["value"]:
                print(
                    f"[{i+1}/365] Dia {data_atual}: Sem cotação (Fim de semana/Feriado)"
                )
            else:
                valor_compra = res["value"][0]["cotacaoCompra"]
                print(f"[{i+1}/365] Dia {data_atual}: R$ {valor_compra}")

        except Exception as e:
            print(f"Erro ao acessar o dia {data_atual}: {e}")

        # Atualizando a data para o dia anterior antes de ir para a próxima volta do loop
        data_atual = (datetime.strptime(data_atual, "%m-%d-%Y") - timedelta(1)).strftime("%m-%d-%Y")

        # Pequena pausa para evitar bloqueio do servidor do Banco Central
        time.sleep(0.1)
# chamando a função
cotar()
