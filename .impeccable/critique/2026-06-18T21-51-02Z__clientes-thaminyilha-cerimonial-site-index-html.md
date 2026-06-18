---
target: clientes/ThaminyIlha.Cerimonial/site/index.html
total_score: 30
p0_count: 0
p1_count: 5
timestamp: 2026-06-18T21-51-02Z
slug: clientes-thaminyilha-cerimonial-site-index-html
---
## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | CTAs dependem de JS; sem noscript fallback |
| 2 | Match System / Real World | 4 | Linguagem perfeita pro público |
| 3 | User Control and Freedom | 2 | Nav oculta em mobile sem substituto |
| 4 | Consistency and Standards | 3 | Side-stripe em .note e .card-ps quebra padrão |
| 5 | Error Prevention | 3 | WhatsApp approach elimina erros de formulário |
| 6 | Recognition Rather Than Recall | 4 | Labels claros, preços visíveis |
| 7 | Flexibility and Efficiency | 2 | Sem nav mobile |
| 8 | Aesthetic and Minimalist Design | 3 | Eyebrow em 11 seções; cadência saturada |
| 9 | Error Recovery | 3 | JS failure quebra CTAs sem fallback |
| 10 | Help and Documentation | 3 | FAQ excelente; sem aria-expanded |
| Total | | 30/40 | Good — base sólida, bloqueadores claros |

## Anti-Patterns Verdict

Site não parece gerado por AI — o copy tem voz real. O que soa como AI grammar: 11 eyebrows uppercase em sequência. Toda seção tem seu próprio eyebrow tracked.

Detector findings: em-dash-overuse (8 em-dashes — violação do briefing "Sem travessão"), numbered-section-markers (advisory — passos 01-03 são sequência genuína, lista de dores 01-06 é defensável).

## Priority Issues

[P1] Developer warning visível: `⚠ Substituir pelos depoimentos reais` está no HTML público.
[P1] Testimonials sem foto real e sem nome — placeholders cinzas.
[P1] Mobile sem navegação — nav oculta a 880px sem hamburger.
[P1] Eyebrow em 11 seções consecutivas — AI grammar tell.
[P1] 8 em-dashes contra guideline explícito "Sem travessão".

## Minor Observations

- text-wrap: balance ausente em h1-h3
- scroll-behavior: smooth sem reduced-motion check no CSS
- FAQ .faq-q sem aria-expanded
- Taupe 13px sobre cream: ~3.2:1, falha WCAG AA
- Side-stripe border-left em .note e .card-ps (banido pelo DESIGN.md)
- prefers-reduced-motion ausente no CSS para transitions

## Persona Red Flags

Jordan (mobile first-timer): nav oculta, warning de dev visível, placeholders de depoimento.
Riley (stress tester): JS desativado = zero CTAs funcionam.
Noiva Ansiosa (primário): depoimentos sem foto real = abandono antes de preço.
