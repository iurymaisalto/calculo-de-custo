from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # -------------------------
        # 📥 ENTRADAS
        # -------------------------
        nome_item = request.form.get("nome_item")

        peso_unit = float(request.form.get("peso_unitario") or 0)
        cavidades = int(request.form.get("cavidades") or 1)
        ciclo_seg = float(request.form.get("ciclo_seg") or 1)

        preco_mat = float(request.form.get("preco_material") or 0)
        preco_master = float(request.form.get("preco_master") or 0)
        porcent_master = float(request.form.get("porcent_master") or 0)

        hora_maquina = float(request.form.get("hora_maquina") or 0)
        porcent_perca = float(request.form.get("porcent_perca") or 0)

        preco_emb = float(request.form.get("preco_emb") or 0)
        peso_emb = float(request.form.get("peso_emb") or 0)
        capacidade_emb = int(request.form.get("capacidade_emb") or 1)

        icms = float(request.form.get("icms") or 0)
        pis = float(request.form.get("pis") or 0)
        cofins = float(request.form.get("cofins") or 0)
        margem = float(request.form.get("margem") or 0)

        qtd_producao = float(request.form.get("qtd_producao") or 0)

        # -------------------------
        # 🔄 CONVERSÕES
        # -------------------------
        peso_unit_kg = peso_unit / 1000
        peso_emb_kg = peso_emb / 1000

        icms_pct = icms / 100
        pis_pct = pis / 100
        cofins_pct = cofins / 100
        margem_pct = margem / 100
        master_pct = porcent_master / 100
        perca_pct = porcent_perca / 100

        # -------------------------
        # 🧮 CUSTOS UNITÁRIOS
        # -------------------------

        # Material
        custo_material_unit = peso_unit_kg * preco_mat

        # Master
        custo_master_unit = peso_unit_kg * master_pct * preco_master

        # Máquina (custo por unidade)
        ciclos_por_hora = 3600 / ciclo_seg
        unidades_por_hora = ciclos_por_hora * cavidades
        custo_maquina_unit = hora_maquina / unidades_por_hora if unidades_por_hora > 0 else 0

        # Embalagem
        custo_emb_unit = (peso_emb_kg * preco_emb) / capacidade_emb if capacidade_emb > 0 else 0

        # Perda
        custo_perda_unit = custo_material_unit * perca_pct

        # -------------------------
        # 💰 CUSTO BASE
        # -------------------------
        custo_base = (
            custo_material_unit +
            custo_master_unit +
            custo_maquina_unit +
            custo_emb_unit +
            custo_perda_unit
        )

        # -------------------------
        # 🧾 IMPOSTOS
        # -------------------------
        impostos_unit = custo_base * (icms_pct + pis_pct + cofins_pct)

        # -------------------------
        # 📈 LUCRO
        # -------------------------
        lucro_unit = (custo_base + impostos_unit) * margem_pct

        # -------------------------
        # 💵 PREÇO FINAL
        # -------------------------
        preco_final = custo_base + impostos_unit + lucro_unit

        # -------------------------
        # 📦 PRODUÇÃO (OPCIONAL)
        # -------------------------
        if qtd_producao > 0:
            material_total_kg = peso_unit_kg * qtd_producao
            master_total_kg = material_total_kg * master_pct
            perca_total_kg = material_total_kg * perca_pct

            unidades_dia = unidades_por_hora * 10
            dias = qtd_producao / unidades_dia if unidades_dia > 0 else 0
        else:
            material_total_kg = None
            master_total_kg = None
            perca_total_kg = None
            unidades_dia = None
            dias = None

        # -------------------------
        # 📤 RETORNO
        # -------------------------
        return render_template(
            "index.html",
            result=True,
            nome_item=nome_item,

            custo_material_unit=round(custo_material_unit, 4),
            custo_master_unit=round(custo_master_unit, 4),
            custo_maquina_unit=round(custo_maquina_unit, 4),
            custo_emb_unit=round(custo_emb_unit, 4),
            custo_perda_unit=round(custo_perda_unit, 4),
            impostos_unit=round(impostos_unit, 4),
            preco_final=round(preco_final, 4),

            material_total_kg=material_total_kg,
            master_total_kg=master_total_kg,
            perca_total_kg=perca_total_kg,
            unidades_dia=unidades_dia,
            dias=dias
        )

    return render_template("index.html", result=False)


# 🔥 CONFIGURAÇÃO PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
