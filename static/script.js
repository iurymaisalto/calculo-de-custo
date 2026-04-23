// ----------------------------------------
//   LEMPLAS – SISTEMA DE CUSTOS INDUSTRIAIS
//   Script principal
// ----------------------------------------

// Seleção de elementos
const body = document.body;
const toggleBtn = document.getElementById("toggleMode");
const clearBtn = document.getElementById("clearBtn");
const resultBox = document.getElementById("resultBox");

// ------------------------------
// 🔘 Alternar Modo Escuro/Claro
// ------------------------------
function applyTheme(theme) {
    if (theme === "dark") {
        body.classList.add("darkmode");
        toggleBtn.innerText = "☀️ Modo Claro";
    } else {
        body.classList.remove("darkmode");
        toggleBtn.innerText = "🌙 Modo Escuro";
    }
}

// Ao clicar, alterna o tema
toggleBtn.addEventListener("click", () => {
    const currentTheme = body.classList.contains("darkmode") ? "light" : "dark";
    applyTheme(currentTheme);
    localStorage.setItem("lemiplasTheme", currentTheme);  // salva tema
});

// Carregar tema salvo
document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("lemiplasTheme") || "light";
    applyTheme(savedTheme);
});

// ------------------------------
// 🧹 Limpar todos os campos
// ------------------------------
if (clearBtn) {
    clearBtn.addEventListener("click", () => {
        document.querySelectorAll("input").forEach(input => {
            input.value = "";
        });

        if (resultBox) {
            resultBox.style.display = "none";  // esconde resultado
        }

        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

// ------------------------------
// 📦 Mostrar resultado suavemente
// ------------------------------
function showResult() {
    if (resultBox) {
        resultBox.style.display = "block";
        resultBox.style.opacity = 0;

        setTimeout(() => {
            resultBox.style.transition = "0.5s ease";
            resultBox.style.opacity = 1;
        }, 50);
    }
}

// Exporta função global (Flask chama após cálculo)
window.showResult = showResult;
