##################################==--
# python/paginas/coleta.py
##################################==--
 ##Exibe informações sobre compensação de carbono através da reciclagem de resíduos sólidos==--

import tkinter as tk
from .. import producao_de_carbono_db


##################################==--
# FUNÇÃO PRINCIPAL
##################################==--
def criar_pagina(parent):
    """Cria a página de coleta seletiva com informações, cálculos e atualização dinâmica."""
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


    ##################################==--
    # AJUSTE AUTOMÁTICO DE LARGURA E WRAPLENGTH
    ##################################==--
     ##Ajusta largura do frame interno e quebra de linha do texto quando a janela muda==--
    def ajuste_completo(event):
        canvas_width = event.width
        canvas.itemconfig(frame_window, width=canvas_width)

        nova_largura = event.width - 60
        if nova_largura > 100:
            label_texto.config(wraplength=nova_largura)

    canvas.bind("<Configure>", ajuste_completo)


    ##################################==--
    # CABEÇALHO E LABEL PRINCIPAL
    ##################################==--
     ##Título da seção e exibição inicial dos créditos de carbono==--
    tk.Label(
        scroll_frame,
        text="Coleta Seletiva ♻️",
        font=("Arial", 20, "bold"),
        bg="#008aff",
        fg="white"
    ).pack(pady=20, fill="x")

    label_valor = tk.Label(
        scroll_frame,
        text=f"Crédito de Carbono: {producao_de_carbono_db.moeda_C / 1000:.2f}",
        font=("Arial", 14),
        bg="#f2f2f2"
    )
    label_valor.pack(pady=10)

    tk.Label(
        scroll_frame,
        text="Compensar Crédito de Carbono com Coleta de Resíduos Sólidos:",
        font=("Arial", 15, "bold"),
        bg="#f2f2f2"
    ).pack(pady=10, fill="x")


    ##################################==--
    # TEXTO INFORMATIVO
    ##################################==--
     ##Explica como a coleta seletiva reduz emissões e gera créditos de carbono==--
    texto_label = (
        "Quando você coleta e destina corretamente resíduos recicláveis, evita emissões de CO₂ "
        "que ocorreriam se esses materiais fossem:\n"
        "   > enviados a aterros (gerando metano — CH₄, um gás 25x mais potente que o CO₂)\n"
        "   > produzidos novamente do zero (produção de alumínio, plástico e vidro novos emite muito CO₂).\n\n"
        "A reciclagem, portanto, reduz emissões e pode gerar créditos de carbono mensuráveis e certificados."
    )

    label_texto = tk.Label(
        scroll_frame,
        text=texto_label,
        font=("Arial", 10),
        justify="left",
        bg="#f2f2f2",
        wraplength=500
    )
    label_texto.pack(pady=10, padx=20, fill="x")


    ##################################==--
    # CÁLCULO DE TONELADAS NECESSÁRIAS
    ##################################==--
     ##Mostra a quantidade estimada de resíduos que compensam o crédito atual==--
    residuos = tk.Label(
        scroll_frame,
        text=(
            f"Toneladas de Papel para compensar: {producao_de_carbono_db.moeda_C / 1000 / producao_de_carbono_db.papel:.2f} t\n\n"
            f"Toneladas de Vidro para compensar: {producao_de_carbono_db.moeda_C / 1000 / producao_de_carbono_db.vidro:.2f} t\n\n"
            f"Toneladas de Plástico para compensar: {producao_de_carbono_db.moeda_C / 1000 / producao_de_carbono_db.plastico:.2f} t\n\n"
            f"Toneladas de Alumínio para compensar: {producao_de_carbono_db.moeda_C / 1000 / producao_de_carbono_db.aluminio:.2f} t\n"
        ),
        font=("Arial", 12, "bold"),
        justify="left",
        bg="#f2f2f2"
    )
    residuos.pack(side=tk.LEFT, pady=10, padx=20)


    ##################################==--
    # SCROLL E ROLAGEM COM O MOUSE
    ##################################==--
     ##Permite rolar o conteúdo com o mouse em diferentes sistemas operacionais==--
    def atualizar_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", atualizar_scrollregion)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    # Ativa rolagem apenas quando o mouse está sobre o canvas
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    canvas.bind("<Button-4>", _on_mousewheel_linux)
    canvas.bind("<Button-5>", _on_mousewheel_linux)


    ##################################==--
    # ATUALIZAÇÃO AUTOMÁTICA DOS VALORES
    ##################################==--
     ##Atualiza os valores de crédito e toneladas em tempo real==--
    def atualizar_valor():
        if not label_valor.winfo_exists():
            return

        valor_atual = producao_de_carbono_db.moeda_C / 1000
        label_valor.config(text=f"Crédito de Carbono: {valor_atual:.2f}")

        if not residuos.winfo_exists():
            return

        papel = valor_atual / producao_de_carbono_db.papel
        vidro = valor_atual / producao_de_carbono_db.vidro
        plastico = valor_atual / producao_de_carbono_db.plastico
        aluminio = valor_atual / producao_de_carbono_db.aluminio

        residuos.config(
            text=(
                f"Toneladas de Papel para compensar: {papel:.2f} t\n\n"
                f"Toneladas de Vidro para compensar: {vidro:.2f} t\n\n"
                f"Toneladas de Plástico para compensar: {plastico:.2f} t\n\n"
                f"Toneladas de Alumínio para compensar: {aluminio:.2f} t\n"
            )
        )

        parent.after(1000, atualizar_valor)

    atualizar_valor()
