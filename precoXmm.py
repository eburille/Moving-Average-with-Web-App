import csv

def mm_media_movel(cotações, period):
    soma = 0
    for cotação in cotações:
        soma += cotação
    media = soma / period

    return media

def mm_stats(cotação, media):
    if cotação > media:
        return 'compra'
    else: return 'venda'

def mm_start(po, status, check_status):
    if po == False and status != check_status and check_status != '':
        return True
    elif po == True:
        return True
    else: return False

def mm_rent(entrada, saida, status, patrimonio):
    if status == 'venda' and entrada != 0:
        rentab = (saida - entrada) / entrada
        return (rentab + 1) 

    elif status == 'compra' and entrada != 0:
        rentab = (-(saida - entrada)) / entrada
        return (rentab + 1)

    else:
        return patrimonio

def mm_ticker_adj(ticker):
    return ticker.upper() + '.SA.csv'

def mm_media_ganhos(retorno_ganho, med_ganho):
    return (retorno_ganho + med_ganho)/2

def mm_media_perdas(retorno_perda, med_perda):
    return (retorno_perda + med_perda)/2

class Retorno():
    drawdown=1
    maior_retorno=0
    media_ganhos=0
    media_perdas=0
    operacoes_ganhas=0
    operacoes_perdas=0
    retorno_total=0
    patrimonio = 1
    numero_operacoes = 0
    status_atual=''
    taxa_acerto = 0
    longonly = 0
    first_data = 0

    def __init__(self, period):
        self.periodo = period

def mm_main(period, ticker):
    ticker_ajustado = mm_ticker_adj(ticker)

    retorno = Retorno(period)
    ultima_cotacao = 0

    try:
        f = open(ticker_ajustado)
        f.close()
    except: 
        return 'erro'
        
    with open(ticker_ajustado) as ativo:
        read = csv.DictReader(ativo)
        cotações_periodo = []

        media = 0

        status = ''
        check_status = ''

        entrada = 0
        saida = 0

        primeira_operação = True
            
        for num, row in enumerate(read):
            if len(cotações_periodo) < retorno.periodo:
                cotações_periodo.append(float(row['Close']))
                if num == 0:
                    retorno.longonly = float(row['Open'])
                    retorno.first_data = row['Date']

            else:
                cotações_periodo.pop(0)
                cotações_periodo.append(float(row['Close']))
                media = mm_media_movel(cotações_periodo, period)

                check_status = status
                status = mm_stats(float(row['Close']), media)

                primeira_operação = mm_start(primeira_operação, status, check_status)
                

                ultima_cotacao = float(row['Close'])

                if primeira_operação == True and check_status != status:
                    entrada = saida
                    saida = float(row['Close'])
                    retorno.numero_operacoes += 1
                    rentab = mm_rent(entrada, saida, status, retorno.patrimonio)
                    retorno.patrimonio = rentab * retorno.patrimonio
                    retorno.status_atual = status

                    #print(row['Date'], status, retorno.patrimonio, row['Close'])

                    if rentab > 1:
                        retorno.operacoes_ganhas += 1
                        retorno.media_ganhos = mm_media_ganhos(rentab, retorno.media_ganhos)
                        if rentab > retorno.maior_retorno:
                            retorno.maior_retorno = rentab
                    
                    elif rentab <= 1:
                        retorno.operacoes_perdas += 1
                        retorno.media_perdas = mm_media_perdas(rentab, retorno.media_perdas)
                        if rentab < retorno.drawdown:
                            retorno.drawdown = rentab


    retorno.media_perdas = round(      (1-retorno.media_perdas)*100,       2)
    retorno.media_ganhos = round(     ((retorno.media_ganhos-1)*100),      2)
    retorno.drawdown = round(         ((1-retorno.drawdown)*100),          2)    
    retorno.maior_retorno = round(    (retorno.maior_retorno-1)*100,       2)
    retorno.patrimonio = round(retorno.patrimonio, 2)
    retorno.retorno_total = round ((retorno.patrimonio - 1) * 100, 2)
    retorno.status_atual = status
    retorno.taxa_acerto = round(   retorno.operacoes_ganhas/retorno.numero_operacoes *100   , 2)
    retorno.longonly = round((ultima_cotacao-retorno.longonly)/retorno.longonly*100, 2)

    return retorno

func = mm_main