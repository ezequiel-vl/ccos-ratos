// Quebra [data-palavras] em palavras e [data-digita] em letras, com atraso progressivo.
// As animacoes sao CSS: o render pausa e posiciona cada uma no tempo do quadro.
(function () {
  document.querySelectorAll("[data-palavras]").forEach(function (el) {
    var inicio = +el.dataset.palavras || 0, passo = +el.dataset.passo || 90, i = 0;
    var andar = function (no) {
      Array.from(no.childNodes).forEach(function (filho) {
        if (filho.nodeType === 3) {
          var frag = document.createDocumentFragment();
          filho.textContent.split(/(\s+)/).forEach(function (pedaco) {
            if (!pedaco) return;
            if (/^\s+$/.test(pedaco)) { frag.appendChild(document.createTextNode(pedaco)); return; }
            var s = document.createElement("span");
            s.className = "w"; s.textContent = pedaco;
            s.style.animationDelay = inicio + i++ * passo + "ms";
            frag.appendChild(s);
          });
          no.replaceChild(frag, filho);
        } else if (filho.nodeType === 1) {
          if (filho.classList.contains("pt")) { filho.classList.add("w"); filho.style.animationDelay = inicio + i++ * passo + "ms"; }
          else andar(filho);
        }
      });
    };
    andar(el);
  });
  document.querySelectorAll("[data-digita]").forEach(function (el) {
    var inicio = +el.dataset.digita || 0, passo = +el.dataset.passo || 55;
    var texto = el.textContent; el.textContent = "";
    Array.from(texto).forEach(function (c, i) {
      var s = document.createElement("span");
      s.className = "l"; s.textContent = c;
      s.style.animationDelay = inicio + i * passo + "ms";
      el.appendChild(s);
    });
    if (el.hasAttribute("data-cursor")) { var k = document.createElement("i"); k.className = "cursor"; el.appendChild(k); }
  });
})();
