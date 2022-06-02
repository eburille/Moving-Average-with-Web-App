import pandas_datareader.data as web
import yfinance as yf
from precoXmm_teste import func

yf.pdr_override()

def ticker_adj(ticker):
    return ticker.upper() + '.SA'


def melhor_result(ticker):
    
    ticker_ajustado = ticker_adj(ticker)

    cot = web.get_data_yahoo(ticker_ajustado)

    if 'Empty DataFrame' in str(cot):
        return 'Erro'

    melhor_retorno = 0
    retorno = 0

    for periodo in range(2, 50):
        del retorno
        retorno = func(periodo, cot)
        if retorno.patrimonio > melhor_retorno:
            melhor_retorno = retorno.patrimonio
            result = retorno

    return result

def result(ticker, periodo):
    ticker_ajustado = ticker_adj(ticker)

    cot = web.get_data_yahoo(ticker_ajustado)

    retorno = func(periodo, cot)

    return retorno


otimizador = melhor_result

res = result