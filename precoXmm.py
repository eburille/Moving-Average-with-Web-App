import pandas_datareader.data as web

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
    first_data = 0
    longonly = 0
    

    def __init__(self, period):
        self.periodo = period

class MM():
    cotacoes = []
    primeira_cot = 0

    entrada = 0
    saida = 0

    def atual(self):
        def media(cotacoes):
            soma = 0
            for cotacao in cotacoes:
                soma += cotacao     
            try: media = soma / len(cotacoes)
            except: media = 0
            return media

        self.media = media(self.cotacoes)

def mm_main(period, cot):

    retorno = Retorno(period)
    mm = MM()

    mm.cotacoes = []

    status = ''
    check_status = ''

    primeira_operação = True
        
    for indice, row in cot.iterrows():

        if len(mm.cotacoes) < retorno.periodo:
            mm.cotacoes.append(float(row['Close']))
            retorno.first_data = str(indice)[:10]
            mm.primeira_cot = float(row['Adj Close'])

        else:
            mm.atual()

            check_status = status
            status = mm_stats(float(row['Close']), mm.media)

            primeira_operação = mm_start(primeira_operação, status, check_status)
                
            ultima_cotacao = float(row['Adj Close'])
                
            if primeira_operação == True and check_status != status:
                    
                mm.entrada = mm.saida
                mm.saida = float(row['Close'])
                retorno.numero_operacoes += 1
                rentab = mm_rent(mm.entrada, mm.saida, status, retorno.patrimonio)
                retorno.patrimonio = rentab * retorno.patrimonio                    
                retorno.status_atual = status

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
                    
            mm.cotacoes.pop(0)
            mm.cotacoes.append(float(row['Close']))


    retorno.media_perdas = round(      (1-retorno.media_perdas)*100,       2)
    retorno.media_ganhos = round(     ((retorno.media_ganhos-1)*100),      2)
    retorno.drawdown = round(         ((1-retorno.drawdown)*100),          2)    
    retorno.maior_retorno = round(    (retorno.maior_retorno-1)*100,       2)
    retorno.patrimonio = round(retorno.patrimonio, 2)
    retorno.retorno_total = round ((retorno.patrimonio - 1) * 100, 2)
    retorno.status_atual = status
    retorno.taxa_acerto = round(   retorno.operacoes_ganhas/retorno.numero_operacoes *100   , 2)
    try:
        retorno.longonly = round(    (ultima_cotacao - mm.primeira_cot) / mm.primeira_cot * 100  ,2)
    except:
        retorno.longonly = 0

    return retorno

func = mm_main
