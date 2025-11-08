##################################==--
# python/paginas/eolica.py
##################################==--
 ##Exibe informações sobre compensação de carbono via investimento em energia eólica==--

import tkinter as tk
from .. import producao_de_carbono_db


##################################==--
# FUNÇÃO PRINCIPAL
##################################==--
def criar_pagina(parent):
    """Cria a página de energia eólica com informações e cálculo de investimento."""
    parent.configure(bg="#f2f2f2")

    ##################################==--
    # CONTAINER COM SCROLL
    ##################################==--
     ##Cria um canvas com barra de rolagem vertical para todo o conteúdo==--
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
     ##Título da página e exibição do valor atual de créditos de carbono==--
    tk.Label(
        scroll_frame,
        text="Energia Eólica 💨",
        font=("Arial", 20, "bold"),
        bg="#8c4318",
        fg="white"
    ).pack(pady=20, fill="x")

    label_valor = tk.Label(
        scroll_frame,
        text=f"Crédito de Carbono: {producao_de_carbono_db.moeda_C / 1000:.2f}",
        font=("Arial", 14),
        bg="#f2f2f2"
    )
    label_valor.pack(pady=10, fill="x")

    tk.Label(
        scroll_frame,
        text="Compensar Crédito de Carbono com energia Eólica:",
        font=("Arial", 15, "bold"),
        bg="#f2f2f2"
    ).pack(pady=10, fill="x")


    ##################################==--
    # TEXTO INFORMATIVO
    ##################################==--
     ##Explicação sobre como a energia eólica compensa emissões de CO₂==--
    texto = (
        "Investir em energia eólica é uma forma de compensar emissões porque você financia a geração de energia limpa, "
        "que substitui a energia de fontes fósseis, evitando a emissão de CO₂.\n\n"
        "   > Cada MWh de energia eólica que substitui carvão ou gás evita uma quantidade específica de CO₂ "
        "(depende da matriz energética local).\n"
        "   > Projetos eólicos certificados podem gerar créditos de carbono, que podem ser usados por empresas ou "
        "indivíduos para neutralizar suas emissões.\n\n"
        "Como funciona na prática\n\n"
        "1. Investimento direto em projetos eólicos:\n"
        "   > Financiar construção ou operação de novos parques eólicos.\n"
        "   > Isso gera impacto adicional, ou seja, você ajuda a aumentar a produção de energia limpa.\n\n"
        "2. Compra de créditos de carbono de projetos eólicos:\n"
        "   > Cada crédito equivale a 1 tonelada de CO₂ evitada.\n"
        "   > Certifique-se de que os créditos são certificados (ex.: Verra VCS, Gold Standard).\n\n"
        "Monitoramento e certificação:\n\n"
        "   > É importante que o projeto seja auditado e que os créditos sejam rastreáveis, evitando dupla contagem."
    )

    label_texto = tk.Label(
        scroll_frame,
        text=texto,
        font=("Arial", 10),
        justify="left",
        wraplength=500,
        bg="#f2f2f2"
    )
    label_texto.pack(pady=10, padx=20, fill="x")


    ##################################==--
    # CÁLCULO DE INVESTIMENTO
    ##################################==--
     ##Mostra o valor estimado a ser investido em energia eólica para compensação==--
    tk.Label(
        scroll_frame,
        text="Valor a ser investido em Energia Eólica:",
        font=("Arial", 15, "bold"),
        bg="#f2f2f2"
    ).pack(pady=10)

    score = tk.Label(
        scroll_frame,
        text=f"R$ {producao_de_carbono_db.moeda_C / 1000 / producao_de_carbono_db.solar_eolica:.2f}",
        font=("Arial", 20, "bold"),
        bg="#f2f2f2"
    )
    score.pack(pady=10)


    ##################################==--
    # AJUSTE DE WRAPLENGTH
    ##################################==--
     ##Adapta o texto conforme a largura da janela e atualiza a área de rolagem==--
    def ajustar_wrap(event):
        nova_largura = event.width - 60
        if nova_largura > 100:
            label_texto.config(wraplength=nova_largura)
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


    ##################################==--
    # ATUALIZAÇÃO AUTOMÁTICA
    ##################################==--
     ##Atualiza periodicamente o valor do crédito e do investimento==--
    def atualizar_valor():
        if not label_valor.winfo_exists():
            return

        valor_atual = producao_de_carbono_db.moeda_C / 1000
        label_valor.config(text=f"Crédito de Carbono: {valor_atual:.2f}")

        if not score.winfo_exists():
            return

        atual = producao_de_carbono_db.moeda_C / 1000 / producao_de_carbono_db.solar_eolica
        score.config(text=f"R$ {atual:.2f}")

        parent.after(1000, atualizar_valor)

    atualizar_valor()
