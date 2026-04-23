from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        # -------------------------
        # 🔹 Coleta dos dados
        # -------------------------
        nome_item = request.form.get("nome_item")

        preco_material = float(request.form.get("preco_material") or 0)
        peso_unitario_g = float(request.form.get("peso_unitario") or 0)

        preco_master = float(request.form.get("preco_master") or 0)
        porcent_master = float(request.form.get("porcent_master") or 0)

        cavidades = int(request.form.get("cavidades") or 1)
        ciclo_seg = float(request.form.get("ciclo_seg") or 1)

        hora_maquina = float(request.form.get("hora_maquina") or 0)

        porcent_perca = float(request.form.get("porcent_perca") or 0)

        preco_emb = float(request.form.get("preco_emb") or 0)
        peso_emb_g = float(request.form.get("peso_emb") or 0)
        capacidade_emb = int(request.form.get("capacidade_emb") or 1)

        icms = float(request.form.get("icms") or 0)
        pis = float(request.form.get("pis") or 0)
        cofins = float(request.form.get("cofins") or 0)

        margem = float(request.form.get("margem") or 0)

        qtd_producao = float(request.form.get("qtd_producao") or 0)

        # -------------------------
        # 🔹 Cálculo básico
        # -------------------------
        peso_ciclo_g = peso_unitario_g * cavidades
        peso_unit_kg = peso_unitario_g / 1000
        peso_emb_kg = peso_emb_g / 1000

        # -------------------------
        # 🔹 Material por unidade
        # -------------------------
        custo_material_unit = peso_unit_kg * preco_material

        # -------------------------
        # 🔹 Cálculo do master
        # -------------------------
        master_por_kg = porcent_master / 100
        custo_master_unit = preco_master * master_por_kg * peso_unit_kg

        # -------------------------
        # 🔹 Cálculo da hora-máquina
        # -------------------------
        ciclos_por_hora = 3600 / ciclo_seg
        unidades_por_hora = ciclos_por_hora * cavidades
        custo_hora_unit = hora_maquina / unidades_por_hora

        # -------------------------
        # 🔹 Embalagem por unidade
        # -------------------------
        custo_emb_unit = (peso_emb_kg * preco_emb) / capacidade_emb

        # -------------------------
        # 🔹 Perda por unidade
        # -------------------------
        custo_perca_unit = custo_material_unit * (porcent_perca / 100)

        # -------------------------
        # 🔹 Impostos por unidade
        # -------------------------
        imposto_total = icms + pis + cofins
        custo_imposto_unit = imposto_total / 100

        # -------------------------
        # 🔹 Custo total sem lucro
        # -------------------------
        custo_unit_sem_lucro = (
            custo_material_unit +
            custo_master_unit +
            custo_hora_unit +
            custo_emb_unit +
            custo_perca_unit +
            custo_imposto_unit
        )

        # -------------------------
        # 🔹 Aplicação da margem
        # -------------------------
        custo_final_unit = custo_unit_sem_lucro * (1 + margem / 100)

        # -------------------------
        # 🔹 Produção total
        # -------------------------
        material_total_kg = (peso_unit_kg * qtd_producao)
        master_total_kg = material_total_kg * master_por_kg
        perca_total_kg = material_total_kg * (porcent_perca / 100)

        unidades_por_dia = unidades_por_hora * 10  # 10 horas por dia
        dias_para_produzir = qtd_producao / unidades_por_dia if unidades_por_dia > 0 else 0

        return render_template(
            "index.html",
            result=True,
            nome_item=nome_item,
            custo_final_unit=round(custo_final_unit, 4),
            custo_material_unit=round(custo_material_unit, 4),
            custo_master_unit=round(custo_master_unit, 4),
            custo_hora_unit=round(custo_hora_unit, 4),
            custo_emb_unit=round(custo_emb_unit, 4),
            custo_perca_unit=round(custo_perca_unit, 4),
            custo_imposto_unit=round(custo_imposto_unit, 4),
            material_total_kg=round(material_total_kg, 3),
            master_total_kg=round(master_total_kg, 3),
            perca_total_kg=round(perca_total_kg, 3),
            dias_para_produzir=round(dias_para_produzir, 2),
            unidades_por_dia=int(unidades_por_dia),
        )

    return render_template("index.html", result=False)


if __name__ == "__main__":
    app.run(debug=True)
