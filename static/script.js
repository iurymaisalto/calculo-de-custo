function calcular() {
    const peso = parseFloat(document.getElementById("peso").value);
    const perda = parseFloat(document.getElementById("perda").value);
    const preco = parseFloat(document.getElementById("preco").value);
    const pedido = parseFloat(document.getElementById("pedido").value);

    const icms = parseFloat(document.getElementById("icms").value);
    const pis = parseFloat(document.getElementById("pis").value);
    const cofins = parseFloat(document.getElementById("cofins").value);
    const lucro = parseFloat(document.getElementById("lucro").value);

    if (!peso || !preco) {
        document.getElementById("resultado").innerHTML = "<b>Preencha peso e preço do material!</b>";
        return;
    }

    const pesoKg = peso / 1000;
    const perdaMultiplicador = 1 + (perda ? perda / 100 : 0);

    const custoMaterial = pesoKg * preco * perdaMultiplicador;

    const impostos = (icms + pis + cofins) / 100;
    const margem = lucro / 100;

    const custoFinal = custoMaterial * (1 + impostos) * (1 + margem);

    let html = `
        <h3>DADOS INFORMADOS</h3>
        <p><b>Peso do produto:</b> ${peso} g</p>
        <p><b>Perda:</b> ${perda || 0}%</p>
        <p><b>Preço do material:</b> R$ ${preco.toFixed(2)} / kg</p>
        <p><b>ICMS:</b> ${icms || 0}%</p>
        <p><b>PIS:</b> ${pis || 0}%</p>
        <p><b>COFINS:</b> ${cofins || 0}%</p>
        <p><b>Margem de lucro:</b> ${lucro || 0}%</p>
    `;

    if (pedido) {
        html += `<p><b>Quantidade do pedido:</b> ${pedido} unidades</p>`;
    }

    html += `
        <h3>RESULTADO</h3>
        <p><b>Custo do material por unidade:</b> R$ ${custoMaterial.toFixed(4)}</p>
        <p><b>Preço final de venda unitário:</b> <span style="color:green; font-size:20px;"><b>R$ ${custoFinal.toFixed(2)}</b></span></p>
    `;

    if (pedido) {
        html += `
            <p><b>Total para o pedido (${pedido} unidades):</b> 
            <span style="color:blue; font-size:18px;"><b>R$ ${(custoFinal * pedido).toFixed(2)}</b></span></p>
        `;
    }

    document.getElementById("resultado").innerHTML = html;
}
