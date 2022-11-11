from downloader import melhor_result
from models import *
from downloader import *
from precoXmm import Retorno 

def follow_btn(current_user, ticker):
    if current_user.is_authenticated:
        query = lista_de_acoes.query.filter_by(user_id = current_user.id, acao = ticker).first()

        if type(query) is lista_de_acoes:
            return 'unfollow'
        else: return 'follow'

def following(current_user, ticker):
    nova_acao = lista_de_acoes(acao = ticker, user_id = current_user.id)
    db.session.add(nova_acao)
    db.session.commit()

def unfollowing(current_user, ticker):
    acao_excluida = lista_de_acoes.query.filter_by(user_id = current_user.id, acao = ticker).first()
    db.session.delete(acao_excluida)
    db.session.commit()

def follower_system(current_user, ticker, action):

    if action == 'follow':
        following(current_user=current_user, ticker=ticker)
        
    elif action == 'unfollow':
        unfollowing(current_user=current_user, ticker=ticker)

class Retornos():
    melhor_resultado = 0
    resultado_periodo_espec = 0

    def call_otimizador_operation(self, ticker):
        if type(self.melhor_resultado) is not Retorno:
            self.melhor_resultado = otimizador(ticker)

        elif type(self.melhor_resultado) is Retorno and self.melhor_resultado.ticker != ticker:
            self.melhor_resultado = otimizador(ticker)

        return

    def call_res_operation(self, ticker, periodo):
        self.resultado_periodo_espec = res(ticker, periodo) 

    def __init__(self):
        pass
