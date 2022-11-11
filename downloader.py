import pandas_datareader.data as web
import yfinance as yf
from precoXmm import func

yf.pdr_override()

def ticker_adj(ticker):
    return ticker.upper() + '.SA'

def melhor_result(ticker):
    
    ticker_ajustado = ticker

    cot = web.get_data_yahoo(ticker_ajustado,'2010-01-01')

    if 'Empty DataFrame' in str(cot):
        return 'Erro'

    melhor_retorno = 0
    retorno = 0

    for periodo in range(2, 100):

        retorno = func(periodo, cot, ticker)
        if retorno.patrimonio > melhor_retorno:
            melhor_retorno = retorno.patrimonio
            result = retorno

    return result

def result(ticker, periodo):
    ticker_ajustado = ticker

    cot = web.get_data_yahoo(ticker_ajustado)

    retorno = func(periodo, cot, ticker=ticker)

    return retorno

otimizador = melhor_result

res = result
