##################################==--
# python/paginas/reflorestamento.py
##################################==--
 ##Exibe informações sobre compensação de carbono via plantio de árvores==--

import tkinter as tk
import math
from .. import producao_de_carbono_db


##################################==--
# FUNÇÃO PRINCIPAL
##################################==--
def criar_pagina(parent):
    """Cria a página de reflorestamento com scroll e cálculo automático de árvores."""
    parent.configure(bg="#f2f2f2")

    ##################################==--
    # CONTAINER COM SCROLL
    ##################################==--
     ##Cria área de rolagem vertical no container principal==--
    canvas = tk.Canvas(parent, bg="#f2f2f2", highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f2f2f2")

    frame_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def ajustar_largura(event):
        canvas_width = event.width
        canvas.itemconfig(frame_window, width=canvas_width)

    canvas.bind("<Configure>", ajustar_largura)


    ##################################==--
    # CABEÇALHO E INFORMAÇÕES PRINCIPAIS
    ##################################==--
     ##Título e valor atual de crédito de carbono==--
    tk.Label(
        scroll_frame, text="Reflorestamento 🌳",
        font=("Arial", 20, "bold"), bg="#29ab24", fg="white"
    ).pack(pady=20, fill="x")

    moeda = tk.Label(
        scroll_frame,
        text=f"Crédito de Carbono: {producao_de_carbono_db.moeda_C / 1000:.2f}",
        font=("Arial", 14), bg="#f2f2f2"
    )
    moeda.pack(pady=10, fill="x")

    tk.Label(
        scroll_frame,
        text="Compensar Crédito de Carbono com o Plantio de Árvores",
        font=("Arial", 15, "bold"), bg="#f2f2f2"
    ).pack(pady=10, fill="x")


    ##################################==--
    # TEXTO INFORMATIVO
    ##################################==--
     ##Explicação sobre o funcionamento do crédito de carbono e reflorestamento==--
    text_info = (
        "Quando uma árvore cresce, ela absorve CO₂ da atmosfera por meio da fotossíntese e armazena esse carbono em sua biomassa "
        "(tronco, folhas, raízes e solo). Esse processo é chamado de sequestro de carbono.\n\n"
        "Para transformar isso em créditos de carbono:\n"
        " 1. Um projeto de reflorestamento é desenvolvido (com plano técnico, área delimitada e espécies definidas);\n"
        " 2. A quantidade de CO₂ que as árvores irão absorver é estimada, com base em dados científicos (biomassa por hectare, tempo de crescimento, etc.);\n"
        " 3. O projeto é validado e certificado por uma entidade reconhecida (ex: Verra, Gold Standard, Clean Development Mechanism da ONU);\n"
        " 4. A cada tonelada de CO₂ sequestrada, é emitido um crédito de carbono;\n"
        " 5. Esses créditos podem ser vendidos a empresas ou pessoas que desejam compensar suas emissões.\n\n"
        "A “troca” de créditos de carbono\n\n"
        "Depois que os créditos são gerados, eles entram em um mercado de carbono, que pode ser:\n\n"
        " • Voluntário: empresas ou pessoas compram créditos por vontade própria (ex: uma empresa quer ser “carbono neutro”);\n"
        " • Regulado: governos impõem limites de emissões e permitem a compra de créditos para compensar o que passa do limite.\n\n"
        "Assim:\n\n"
        " • Quem planta as árvores e sequestra carbono → ganha créditos;\n"
        " • Quem compra os créditos → compensa suas emissões e pode declarar neutralidade de carbono."
    )

    texto_label = tk.Label(
        scroll_frame, text=text_info,
        font=("Arial", 10), justify="left",
        wraplength=500, bg="#f2f2f2"
    )
    texto_label.pack(pady=15, padx=20, fill="x")


    ##################################==--
    # CÁLCULO DE ÁRVORES NECESSÁRIAS
    ##################################==--
     ##Determina quantas árvores são necessárias para compensar o carbono gerado==--
    tk.Label(
        scroll_frame,
        text="Com isso, o número de Árvores a plantar é:",
        font=("Arial", 15, "bold")
    ).pack(pady=10)

    score_valor = producao_de_carbono_db.moeda_C / 1000 / producao_de_carbono_db.arvore
    score_valor = math.ceil(score_valor)  # arredonda para cima

    score = tk.Label(
        scroll_frame,
        text=f"{score_valor}",
        font=("Arial", 20, "bold")
    )
    score.pack(pady=10)


    ##################################==--
    # ATUALIZAÇÃO AUTOMÁTICA
    ##################################==--
     ##Atualiza periodicamente o valor de crédito e árvores necessárias==--
    def atualizar_moeda():
        if not moeda.winfo_exists():
            return

        valor_atual = producao_de_carbono_db.moeda_C / 1000
        moeda.config(text=f"Crédito de Carbono: {valor_atual:.2f}")

        if not score.winfo_exists():
            return

        atual = producao_de_carbono_db.moeda_C / 1000 / producao_de_carbono_db.arvore
        score.config(text=f"{math.ceil(atual)}")
        parent.after(1000, atualizar_moeda)

    atualizar_moeda()


    ##################################==--
    # AJUSTE DE WRAPLENGTH
    ##################################==--
     ##Adapta o comprimento do texto conforme o tamanho da janela==--
    def ajustar_wrap(event):
        nova_largura = event.width - 60
        if nova_largura > 100:
            texto_label.config(wraplength=nova_largura)
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", ajustar_wrap)


    ##################################==--
    # ROLAGEM COM O MOUSE
    ##################################==--
     ##Permite scroll com a roda do mouse (Windows e Linux)==--
    def _on_mousewheel(event):
        if canvas.winfo_exists():
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", _on_mousewheel_linux)
    canvas.bind_all("<Button-5>", _on_mousewheel_linux)
