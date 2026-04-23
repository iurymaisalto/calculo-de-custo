from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}

    if request.method == 'POST':
        # Dados enviados pelo usuário
        item_nome = request.form.get("item_nome", "")
        peso_unitario = float(request.form.get("peso_unitario", 0))
        unidades_por_embalagem = int(request.form.get("unidades_por_embalagem", 1))
        valor_material_kg = float(request.form.get("valor_material_kg", 0))
        porcentagem_perda = float(request.form.get("porcentagem_perda", 0))
        valor_energia_kwh = float(request.form.get("valor_energia_kwh", 0))
        consumo_maquina_kwh = float(request.form.get("consumo_maquina_kwh", 0))
        horas_dia = 10  # 10h de produção fixa
        producao_dia = int(request.form.get("producao_dia", 0))
        producao_total = int(request.form.get("producao_total", 0))

        # Master
        valor_master_kg = float(request.form.get("valor_master_kg", 0))
        porcentagem_master = float(request.form.get("porcentagem_master", 0))

        # Cálculos principais
        material_por_peca = peso_unitario / 1000  # gramas → kg
        master_por_peca = material_por_peca * (porcentagem_master / 100)

        custo_material_unit = material_por_peca * valor_material_kg
        custo_master_unit = master_por_peca * valor_master_kg

        custo_energia_unit = (consumo_maquina_kwh * valor_energia_kwh) / producao_dia if producao_dia > 0 else 0

        perda_unit = (custo_material_unit + custo_master_unit) * (porcentagem_perda / 100)

        preco_final = custo_material_unit + custo_master_unit + custo_energia_unit + perda_unit

        # Produção total
        total_material_kg = material_por_peca * producao_total
        total_master_kg = master_por_peca * producao_total

        dias_para_produzir = producao_total / producao_dia if producao_dia > 0 else 0

        result = {
            "item_nome": item_nome,
            "preco_final": round(preco_final, 4),
            "custo_material_unit": round(custo_material_unit, 4),
            "custo_master_unit": round(custo_master_unit, 4),
            "custo_energia_unit": round(custo_energia_unit, 4),
            "perda_unit": round(perda_unit, 4),
            "total_material_kg": round(total_material_kg, 2),
            "total_master_kg": round(total_master_kg, 2),
            "dias_para_produzir": round(dias_para_produzir, 2)
        }

    return render_template("index.html", result=result)


# -------------------------------
# 🔥 CONFIGURAÇÃO OBRIGATÓRIA DO RENDER
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
