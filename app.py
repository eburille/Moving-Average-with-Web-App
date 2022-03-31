from flask import Flask, render_template, request, redirect, url_for
from precoXmm import func

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():

    if len(request.form) > 0:
        ticker = request.form['search']
        return redirect(url_for('empresa', ticker=ticker))
        
    return render_template("inicio.html")

@app.route('/<ticker>', methods=['POST', 'GET'])
def empresa(ticker):

    outro_periodo = 0

    maior_patrimonio = 0
 
    if func(2, ticker) == 'erro':
        return redirect(url_for('erro', ticker=ticker))
    for period in range(1, 150):
        retorno = func(period, ticker)
        if retorno.patrimonio > maior_patrimonio:
            maior_patrimonio = retorno.patrimonio
            melhor_resultado = retorno
    
    if len(request.form) > 0:
        outro_periodo = int(request.form['periodo'])
        resultado = func(outro_periodo, ticker)
        return render_template("ticker.html", melhor_resultado=melhor_resultado, resultado=resultado, ticker=ticker)
        
    return render_template("ticker.html", melhor_resultado=melhor_resultado, ticker=ticker, periodo=0)


@app.route('/erro/<ticker>')
def erro(ticker):
    inicio = 'https://finance.yahoo.com/quote/'
    meio = '.SA/history?p='
    fim = '.SA'
    ticker = ticker.upper()
    link = inicio + ticker + meio + ticker + fim  

    return render_template('erro.html', link = link, ticker = ticker)  

app.run()