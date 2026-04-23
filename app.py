from flask import Flask, render_template, request
import os
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        # Dados gerais
        nome_item = request.form.get("nome_item")
        peso_unit = float(request.form.get("peso_unit"))
        cavidades = int(request.form.get("cavidades"))
        qtd_produzir = int(request.form.get("qtd_produzir"))

        # Matéria-prima
        preco_mat = float(request.form.get("preco_mat"))
        perca = float(request.form.get("perca"))
        preco_master = float(request.form.get("preco_master"))
        porcent_master = float(request.form.get("porcent_master"))

        # Máquina
        hora_maquina = float(request.form.get("hora_maquina"))
        ciclo_seg = float(request.form.get("ciclo_seg"))

        # Embalagem
        preco_emb_kg = float(request.form.get("preco_emb_kg"))
        peso_emb = float(request.form.get("peso_emb"))
        capacidade_emb = int(request.form.get("capacidade_emb"))

        # Impostos e lucro
        icms = float(request.form.get("icms"))
        pis = float(request.form.get("pis"))
        cofins = float(request.form.get("cofins"))
        margem = float(request.form.get("margem"))

        # CÁLCULOS --------------------------------------------------

        # Material por ciclo
        peso_ciclo_g = peso_unit * cavidades  
        peso_ciclo_kg = peso_ciclo_g / 1000  

        # Custo matéria-prima base
        custo_mat_ciclo = peso_ciclo_kg * preco_mat

        # Custo perca
        custo_perca_ciclo = custo_mat_ciclo * (perca / 100)

        # Custo master
        master_kg_por_kg = porcent_master / 100
        master_por_ciclo = peso_ciclo_kg * master_kg_por_kg
        custo_master_ciclo = master_por_ciclo * preco_master

        # Hora máquina por ciclo
        custo_maquina_ciclo = (hora_maquina / 3600) * ciclo_seg

        # Embalagem (saco dividido pela capacidade)
        custo_embalagem_unit = (peso_emb / 1000) * preco_emb_kg / capacidade_emb

        # Custo total do ciclo
        custo_total_ciclo = (
            custo_mat_ciclo +
            custo_perca_ciclo +
            custo_master_ciclo +
            custo_maquina_ciclo
        )

        # Custo unitário antes de impostos
        custo_unitario = custo_total_ciclo / cavidades

        # Impostos
        imposto_unit = custo_unitario * (icms + pis + cofins) / 100

        # Total com embalagem
        custo_unit_final_sem_lucro = custo_unitario + imposto_unit + custo_embalagem_unit

        # Margem de lucro
        custo_final_com_lucro = custo_unit_final_sem_lucro * (1 + margem / 100)

        # Produção total
        ciclos_necessarios = qtd_produzir / cavidades
        material_total_kg = (peso_unit * qtd_produzir) / 1000
        master_total_kg = material_total_kg * master_kg_por_kg

        tempo_total_seg = ciclos_necessarios * ciclo_seg
        horas_totais = tempo_total_seg / 3600
        dias_totais = horas_totais / 10  # 10h por dia

        resultado = {
            "nome_item": nome_item,
            "custo_unit": round(custo_unitario, 4),
            "custo_emb_unit": round(custo_embalagem_unit, 4),
            "imposto_unit": round(imposto_unit, 4),
            "custo_final_lucro": round(custo_final_com_lucro, 4),
            "custo_master_unit": round(custo_master_ciclo / cavidades, 4),
            "material_total_kg": round(material_total_kg, 3),
            "master_total_kg": round(master_total_kg, 3),
            "dias_totais": round(dias_totais, 2),
            "perca_unit": round(custo_perca_ciclo / cavidades, 4),
            "maquina_unit": round(custo_maquina_ciclo / cavidades, 4)
        }

    return render_template("index.html", resultado=resultado)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
