
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    resultado = None
    if request.method == 'POST':
        preco_kg = float(request.form['preco_kg'])
        peso_g = float(request.form['peso_g'])
        hora_maquina = float(request.form['hora_maquina'])
        tempo_seg = float(request.form['tempo_seg'])
        perda = float(request.form['perda'])
        lucro = float(request.form['lucro'])
        impostos = float(request.form['impostos'])
        cavidades = float(request.form['cavidades'])
        preco_embalagem = float(request.form['preco_embalagem'])
        peso_embalagem = float(request.form['peso_embalagem'])

        custo_material = (peso_g/1000) * preco_kg
        custo_ciclo_total = hora_maquina * (tempo_seg/3600)
        custo_maquina = custo_ciclo_total / cavidades
        custo_embalagem = (peso_embalagem/1000)*preco_embalagem

        custo_base = custo_material + custo_maquina + custo_embalagem
        custo_base += custo_base * (perda/100)
        custo_base += custo_base * (impostos/100)
        preco_final = custo_base * (1 + lucro/100)

        resultado = round(preco_final,4)

    return render_template('index.html', resultado=resultado)

app.run(host="0.0.0.0", port=10000)
