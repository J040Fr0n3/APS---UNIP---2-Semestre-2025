import os
import sys
import math
import tkinter as tk
from tkinter import ttk
from python.paginas import carbono, coleta, reflorestamento, solar, eolica
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'python')))

from python.page_credito import criar_pagina_credito
from python.page_home import criar_pagina_home
from python.page_compensar import criar_pagina_compensar


##################################==--
# CONFIGURAÇÕES DE INTERFACE (Tkinter)
##################################==--
## Definindo as cores e o estilo da barra de navegação
nav_bar_color = "#383838"
nav_bar_text = "#ffffff"


##################################==--
# FUNÇÃO DE MOVIMENTO ANIMADO
##################################==--
## Função responsável por animar o indicador de navegação
def move_indicator(target_relx, target_label, duracao=0.2):
    passos = 40
    intervalo = int((duracao / passos) * 1000)

    atual_relx = float(lb_indicator.place_info()['relx'])
    delta_relx = target_relx - atual_relx

    # Ajustar largura da barra para o texto do label clicado
    texto = target_label.cget("text")
    largura_texto = len(texto) * 2  # fator ajustável conforme a fonte
    lb_indicator.config(width=largura_texto)

    # Função de easing (ease-in-out)
    def ease_in_out(t):
        return 0.5 * (1 - math.cos(math.pi * t))

    def animar(passo):
        if passo <= passos:
            t = passo / passos
            eased = ease_in_out(t)
            novo_relx = atual_relx + delta_relx * eased
            lb_indicator.place_configure(relx=novo_relx)
            root.after(intervalo, animar, passo + 1)

    animar(0)


##################################==--
# FECHA JANELAS TKINTER ANTERIORES
##################################==--
## Fecha janelas Tkinter anteriores em caso de reload
if tk._default_root:
    try:
        tk._default_root.destroy()
    except:
        pass


##################################==--
# CRIAÇÃO DA JANELA PRINCIPAL
##################################==--
## Cria e configura a janela principal da aplicação
root = tk.Tk()
root.geometry("800x600")
root.resizable(False, False)
root.title("Calculadora de Carbono")


##################################==--
# BARRA DE NAVEGAÇÃO
##################################==--
## Cria a barra de navegação superior
nav_bar = tk.Frame(root, bg=nav_bar_color, height=35)
nav_bar.pack(side=tk.TOP, fill=tk.X)
nav_bar.pack_propagate(False)


##################################==--
# ÁREA PRINCIPAL (ONDE AS PÁGINAS SERÃO EXIBIDAS)
##################################==--
## Área principal onde as páginas de conteúdo serão exibidas
pages = ttk.Frame(root)
pages.pack(fill='both', expand=True)


##################################==--
# DICIONÁRIO DE PÁGINAS CRIADAS
##################################==--
## Dicionário para armazenar as páginas criadas e evitar recriação
paginas = {}


##################################==--
# FUNÇÃO PARA TROCAR PÁGINAS
##################################==--
## Função para trocar de página sem recriar todas as páginas
def trocar_pagina(nome):
    """Mostra a página escolhida (sem recriar todas as vezes)."""
    # Esconde todas as páginas já criadas
    for pagina in paginas.values():
        pagina.pack_forget()

    # Cria a página se ainda não existir
    if nome not in paginas:
        funcoes_paginas = {
            "home": criar_pagina_home,
            "credito": criar_pagina_credito,
            "compensar": criar_pagina_compensar
        }
        if nome not in funcoes_paginas:
            return
        paginas[nome] = funcoes_paginas[nome](pages, trocar_pagina)

    # Exibe a página selecionada
    paginas[nome].pack(fill="both", expand=True)


##################################==--
# PRÉ-CARREGAMENTO DA PÁGINA "COMPENSAR"
##################################==--
## Cria a página "compensar" uma única vez (não a exibe ainda)
if "compensar" not in paginas:
    paginas["compensar"] = criar_pagina_compensar(pages, trocar_pagina)


##################################==--
# EXIBE A PÁGINA INICIAL "HOME"
##################################==--
## Exibe a página inicial assim que a aplicação inicia
trocar_pagina("home")


##################################==--
# CRIAÇÃO DOS BOTÕES DE NAVEGAÇÃO
##################################==--
## Função para criar os botões de navegação na barra superior
def criar_label_nav(texto, relx, pagina_nome):
    label = tk.Label(
        nav_bar,
        text=texto,
        bg=nav_bar_color,
        fg=nav_bar_text,
        font=("Bold", 15)
    )
    label.place(relx=relx, y=2)
    label.bind(
        "<Button-1>",
        lambda e: (move_indicator(relx, label), trocar_pagina(pagina_nome))
    )
    return label

home = criar_label_nav("Home", 0.1, "home")
credito = criar_label_nav("Crédito", 0.3, "credito")
compensar = criar_label_nav("Compensar", 0.5, "compensar")


##################################==--
# INDICADOR INICIAL
##################################==--
## Cria o indicador de navegação na barra
lb_indicator = tk.Label(nav_bar, bg="white", height=1, width=len("Home") * 2)
lb_indicator.place(relx=0.1, y=30)


##################################==--
# LOOP PRINCIPAL
##################################==--
## Inicia o loop principal do Tkinter
root.mainloop()
