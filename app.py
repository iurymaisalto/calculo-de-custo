from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    d = None

    if request.method == 'POST':
        nome = request.form['nome']

        peso = float(request.form['peso'])
        preco_kg = float(request.form['preco_kg'])

        preco_master = float(request.form['preco_master'])
        perc_master = float(request.form['perc_master'])

        hora = float(request.form['hora_maquina'])
        tempo = float(request.form['tempo'])
        cav = float(request.form['cav'])

        preco_emb = float(request.form['preco_emb'])
        peso_emb = float(request.form['peso_emb'])
        cap = float(request.form['cap'])

        perda = float(request.form['perda'])
        impostos = float(request.form['impostos'])
        lucro = float(request.form['lucro'])

        qtd = float(request.form['qtd'])

        # --- CUSTO POR UNIDADE ---
        mat = (peso / 1000) * preco_kg
        master = (peso / 1000) * (perc_master / 100) * preco_master
        emb = ((peso_emb / 1000) * preco_emb) / cap

        maq_total = hora * (tempo / 3600)
        maq = maq_total / cav

        base = mat + master + emb + maq

        perda_v = base * (perda / 100)
        imp_v = (base + perda_v) * (impostos / 100)
        lucro_v = (base + perda_v + imp_v) * (lucro / 100)

        final = base + perda_v + imp_v + lucro_v

        # --- PRODUÇÃO ---
        prod_h = (3600 / tempo) * cav
        prod_d = prod_h * 10  # produção por dia (10h)
        dias = qtd / prod_d

        # Totais
        total_mat = (peso / 1000) * qtd
        total_master = total_mat * (perc_master / 100)
        perda_total = (base * (perda / 100)) * qtd

        d = {
            "nome": nome,
            "mat": round(mat, 4),
            "master": round(master, 4),
            "emb": round(emb, 4),
            "maq": round(maq, 4),
            "perda": round(perda_v, 4),
            "imp": round(imp_v, 4),
            "lucro": round(lucro_v, 4),
            "final": round(final, 4),

            "prod_h": round(prod_h, 2),
            "prod_d": round(prod_d, 2),
            "dias": round(dias, 2),

            "tot_mat": round(total_mat, 2),
            "tot_master": round(total_master, 2),
            "perda_total": round(perda_total, 2)
        }

    return render_template("index.html", d=d)

app.run(host="0.0.0.0", port=10000)
