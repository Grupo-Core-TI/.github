"""Gera o topo e os quatro cartões do perfil público em SVG, em versão clara e escura.

Uso: python3 ferramentas/gerar_assets.py  (escreve em profile/assets/)
Cores, fontes e logos seguem o Manual de Identidade Visual 2026 (site-institucional).
"""
import base64
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "profile" / "assets"
FONTES = Path(__file__).parent / "fontes"

ESPECTRO = ("#6538B5", "#0090DA", "#47A23F", "#E97722")
TEMAS = {
    "claro": {"fundo": "#eeece8", "chip": "#ffffff", "tinta": "#27262b", "apagado": "#6f6d72",
              "linha": "#d9d6cf", "simbolo": "coreti-symbol-dark.png"},
    "escuro": {"fundo": "#27262b", "chip": "#33323a", "tinta": "#eeece8", "apagado": "#a3a1a7",
               "linha": "#3c3b41", "simbolo": "coreti-symbol-light.png"},
}
EMPRESAS = [
    {"slug": "service", "marca": "SERVICE", "nome": ("Evolution", "IT Service"),
     "tom": {"claro": "#0050B5", "escuro": "#0090DA"},
     "texto": ("Service Desk e atendimento presencial,", "gestão de ativos, Microsoft 365", "e outsourcing de TI.")},
    {"slug": "security", "marca": "SECURITY", "nome": ("Evolution", "IT Security"),
     "tom": {"claro": "#DC582A", "escuro": "#E97722"},
     "texto": ("SOC com EDR gerenciado, identidade", "e acesso, pentest, backup e", "recuperação de desastres.")},
    {"slug": "infra", "marca": "INFRAESTRUTURA", "nome": ("Evolution", "Infraestrutura"),
     "tom": {"claro": "#47A23F", "escuro": "#79BE20"},
     "texto": ("Redes LAN, WAN e Wi-Fi corporativo,", "data center e nuvem híbrida,", "virtualização e servidores Dell.")},
    {"slug": "bridge", "marca": "DATA BRIDGE", "nome": ("Evolution", "Data Bridge"),
     "tom": {"claro": "#6538B5", "escuro": "#9678D3"},
     "texto": ("Inteligência artificial aplicada,", "integração de sistemas e APIs,", "BI e automação de processos.")},
]


def _b64(nome):
    return base64.b64encode((ASSETS / nome).read_bytes()).decode()


def _gradiente(id_, extra=""):
    stops = "".join(f'<stop offset="{i / 3:.2f}" stop-color="{c}"/>' for i, c in enumerate(ESPECTRO))
    return f'<linearGradient id="{id_}" {extra}>{stops}</linearGradient>'


def _fontes():
    faces = [("Bricolage", "bricolage-grotesque-latin-wght-normal.woff2"),
             ("Hanken", "hanken-grotesk-latin-wght-normal.woff2"),
             ("JBMono", "jetbrains-mono-latin-wght-normal.woff2")]
    return "".join(f"@font-face{{font-family:{f};font-weight:100 900;src:url(data:font/woff2;base64,"
                   f"{base64.b64encode((FONTES / a).read_bytes()).decode()}) format('woff2')}}" for f, a in faces)


def _svg(w, h, titulo, t, corpo, defs=""):
    estilo = (_fontes() + ".d{font-family:Bricolage,'Segoe UI',sans-serif}"
              ".t{font-family:Hanken,'Segoe UI',sans-serif}.m{font-family:JBMono,ui-monospace,monospace}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(titulo)}"><title>{escape(titulo)}</title><style>{estilo}</style>'
            f'<defs>{_gradiente("esp", "x1=\"0\" x2=\"1\"")}'
            f'<clipPath id="moldura"><rect width="{w}" height="{h}" rx="24"/></clipPath>{defs}</defs>'
            f'<g clip-path="url(#moldura)"><rect width="{w}" height="{h}" fill="{t["fundo"]}"/>{corpo}</g>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="24" fill="none" stroke="{t["linha"]}"/></svg>')


def _sobrancelha(x, y, texto, t, cor="url(#esp)"):
    return (f'<rect x="{x}" y="{y - 9}" width="8" height="8" rx="2" fill="{cor}"/>'
            f'<text x="{x + 18}" y="{y}" class="m" font-size="12" letter-spacing="2.2" fill="{t["apagado"]}">'
            f"{escape(texto)}</text>")


def _hero(t, x0, y0):
    cx, cy, anel = x0 + 866, y0 + 214, 140
    chips = [("service", 0, -1), ("security", 1, 0), ("infra", 0, 1), ("bridge", -1, 0)]
    satelites = "".join(
        f'<circle cx="{cx + dx * anel}" cy="{cy + dy * anel}" r="28" fill="{t["chip"]}" stroke="{t["linha"]}"/>'
        f'<image x="{cx + dx * anel - 16}" y="{cy + dy * anel - 16}" width="32" height="32" '
        f'href="data:image/png;base64,{_b64(slug + "-symbol.png")}"/>' for slug, dx, dy in chips)
    return (
        _sobrancelha(x0 + 24, y0 + 84, "GRUPO CORE TI · HOLDING DE TECNOLOGIA", t)
        + f'<text class="d" font-size="56" font-weight="700" letter-spacing="-1.8" fill="{t["tinta"]}">'
        f'<tspan x="{x0 + 22}" y="{y0 + 162}">O núcleo onde sistemas,</tspan>'
        f'<tspan x="{x0 + 22}" y="{y0 + 226}">processos e soluções</tspan>'
        f'<tspan x="{x0 + 22}" y="{y0 + 290}" fill="url(#texto)">se conectam.</tspan></text>'
        f'<text class="t" font-size="19" fill="{t["apagado"]}">'
        f'<tspan x="{x0 + 24}" y="{y0 + 348}">Quatro empresas especialistas conectadas sob uma única estrutura:</tspan>'
        f'<tspan x="{x0 + 24}" y="{y0 + 376}">serviço, segurança, infraestrutura e dados.</tspan></text>'
        f'<circle cx="{cx}" cy="{cy}" r="{anel + 42}" fill="none" stroke="{t["linha"]}" stroke-dasharray="2 6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{anel}" fill="none" stroke="url(#anel)" stroke-width="3"/>'
        f'<image x="{cx - 86}" y="{cy - 86}" width="172" height="172" href="data:image/png;base64,{_b64(t["simbolo"])}"/>'
        + satelites)


def _ladrilho(e, t, tema, x, y, w, h, n):
    tom = e["tom"][tema]
    descricao = "".join(f'<tspan x="{x + 36}" y="{y + 200 + i * 27}">{escape(l)}</tspan>' for i, l in enumerate(e["texto"]))
    return (
        f'<clipPath id="l{n}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20"/></clipPath>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{t["chip"]}" stroke="{t["linha"]}"/>'
        f'<g clip-path="url(#l{n})"><image x="{x + w - 222}" y="{y + h - 206}" width="310" height="310" '
        f'href="data:image/png;base64,{_b64(e["slug"] + "-symbol.png")}"/></g>'
        + _sobrancelha(x + 36, y + 60, f"EVOLUTION · {e['marca']}", t, cor=tom)
        + f'<text class="d" font-size="42" font-weight="700" letter-spacing="-1.2" fill="{t["tinta"]}">'
        f'<tspan x="{x + 34}" y="{y + 118}">{e["nome"][0]}</tspan><tspan x="{x + 34}" y="{y + 164}">{e["nome"][1]}</tspan></text>'
        f'<text class="t" font-size="18" fill="{t["apagado"]}">{descricao}</text>'
        f'<text x="{x + 36}" y="{y + h - 34}" class="m" font-size="13" font-weight="500" fill="{tom}">'
        f'grupocoreti.com.br/{e["slug"]} →</text>')


def _bloco_texto(t, x, y, rotulo, linhas, rodape=None):
    corpo = "".join(f'<tspan x="{x}" y="{y + 44 + i * 28}">{escape(l)}</tspan>' for i, l in enumerate(linhas))
    extra = (f'<text x="{x}" y="{y + 44 + len(linhas) * 28 + 22}" class="m" font-size="13" font-weight="500" '
             f'fill="{t["tinta"]}">{escape(rodape)}</text>' if rodape else "")
    return (_sobrancelha(x, y, rotulo, t)
            + f'<text class="t" font-size="18" fill="{t["tinta"]}">{corpo}</text>' + extra)


# Altura ótica de cada logo (px) na ordem em que o site mostra os parceiros.
PARCEIROS = [("dell", 46), ("microsoft", 30), ("acronis", 24), ("bitdefender", 21), ("milvus", 30), ("ubiquiti", 50)]


def _faixa_parceiros(t, tema, x_ini, x_fim, y_meio):
    medidas = []
    for nome, altura in PARCEIROS:
        larg, alt = _dimensoes(ASSETS / "parceiros" / f"{nome}.png")
        medidas.append((nome, altura * larg / alt, altura))
    folga = (x_fim - x_ini - sum(l for _, l, _ in medidas)) / (len(medidas) - 1)
    filtro = ' filter="url(#mono)"' if tema == "escuro" else ""
    partes, x = [], x_ini
    for nome, larg, alt in medidas:
        partes.append(f'<image x="{x:.1f}" y="{y_meio - alt / 2:.1f}" width="{larg:.1f}" height="{alt}"{filtro} '
                      f'href="data:image/png;base64,{_b64("parceiros/" + nome + ".png")}"/>')
        x += larg + folga
    return "".join(partes)


def _dimensoes(caminho):
    cabecalho = caminho.read_bytes()[16:24]
    return int.from_bytes(cabecalho[:4], "big"), int.from_bytes(cabecalho[4:], "big")


def perfil(tema):
    t = TEMAS[tema]
    w, m = 1200, 40
    lw, lh, gap = (w - 2 * m - 24) // 2, 400, 24
    y_lad = 470
    ladrilhos = "".join(_ladrilho(e, t, tema, m + (i % 2) * (lw + gap), y_lad + (i // 2) * (lh + gap), lw, lh, i)
                        for i, e in enumerate(EMPRESAS))
    y_txt = y_lad + 2 * lh + gap + 72
    textos = (
        _bloco_texto(t, m + 24, y_txt, "COMO TRABALHAMOS",
                     ["Mensalidade fixa para o serviço contínuo e projeto", "orçado sob escopo. Cada empresa pode ser contratada",
                      "sozinha ou em conjunto, com uma equipe que", "conhece o seu ambiente."])
        + _bloco_texto(t, m + lw + gap + 24, y_txt, "DIAGNÓSTICO GRATUITO",
                       ["Uma conversa de 40 minutos por vídeo e, em até", "5 dias úteis, um documento com a fotografia do",
                        "seu ambiente, os riscos prioritários e um plano", "por fases."],
                       rodape="grupocoreti.com.br/contato →"))
    y_par = y_txt + 262
    y_rod = y_par + 150
    rodape = (
        f'<line x1="{m + 24}" y1="{y_par - 44}" x2="{w - m - 24}" y2="{y_par - 44}" stroke="{t["linha"]}"/>'
        + _sobrancelha(m + 24, y_par, "PARCEIROS DE TECNOLOGIA", t)
        + _faixa_parceiros(t, tema, m + 24, w - m - 24, y_par + 62)
        + f'<line x1="{m + 24}" y1="{y_rod - 40}" x2="{w - m - 24}" y2="{y_rod - 40}" stroke="{t["linha"]}"/>'
        + f'<text x="{m + 24}" y="{y_rod}" class="m" font-size="13" letter-spacing="1.6" fill="{t["apagado"]}">'
          f"SANTA MARIA · PORTO ALEGRE · RS</text>"
        + f'<text x="{w - m - 24}" y="{y_rod}" text-anchor="end" class="m" font-size="14" fill="{t["tinta"]}">'
          f"grupocoreti.com.br  ·  contato@grupocoreti.com.br</text>")
    h = y_rod + 52
    defs = (_gradiente("texto", f'gradientUnits="userSpaceOnUse" x1="{m + 22}" x2="{m + 380}"')
            + _gradiente("anel", 'x1="0" y1="0" x2="1" y2="1"')
            + '<filter id="mono"><feColorMatrix type="matrix" '
              'values="0 0 0 0 .933 0 0 0 0 .925 0 0 0 0 .91 0 0 0 .85 0"/></filter>')
    corpo = (_hero(t, m, 20) + f'<line x1="{m + 24}" y1="438" x2="{w - m - 24}" y2="438" stroke="{t["linha"]}"/>'
             + ladrilhos + textos + rodape)
    return _svg(w, h, "Grupo Core TI: quatro empresas especialistas operando como uma só. Evolution IT Service, "
                      "IT Security, Infraestrutura e Data Bridge.", t, corpo, defs)


def main():
    for tema in TEMAS:
        (ASSETS / f"perfil-{tema}.svg").write_text(perfil(tema), encoding="utf-8")
    print("ok:", ", ".join(p.name for p in sorted(ASSETS.glob("perfil-*.svg"))))


if __name__ == "__main__":
    main()
