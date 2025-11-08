##################################==--
# python/paginas/solar.py
##################################==--
 ##Exibe informações sobre compensação de carbono via investimento em energia solar==--

import tkinter as tk
from .. import producao_de_carbono_db


##################################==--
# FUNÇÃO PRINCIPAL
##################################==--
def criar_pagina(parent):
    """Cria a página de energia solar com informações, cálculo e atualização automática."""
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
     ##Ajusta automaticamente a largura do frame e quebra de linha do texto==--
    def ajuste_completo(event):
        # Ajusta largura do frame dentro do canvas
        canvas_width = event.width
        canvas.itemconfig(frame_window, width=canvas_width)

        # Ajusta wraplength do texto informativo
        nova_largura = event.width - 60
        if nova_largura > 100:
            label_texto.config(wraplength=nova_largura)

    canvas.bind("<Configure>", ajuste_completo)


    ##################################==--
    # CABEÇALHO E LABELS PRINCIPAIS
    ##################################==--
     ##Título da página e valor inicial de créditos de carbono==--
    tk.Label(
        scroll_frame,
        text="Energia Solar ☀️",
        font=("Arial", 20, "bold"),
        bg="#d99400",
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
        text="Compensar Crédito de Carbono com energia Solar:",
        font=("Arial", 15, "bold"),
        bg="#f2f2f2"
    ).pack(pady=10, fill="x")


    ##################################==--
    # TEXTO INFORMATIVO
    ##################################==--
     ##Descrição detalhada sobre investimentos solares e certificações==--
    texto_label = (
        "Investir em energia solar (residencial, comercial ou em projetos de grande escala) "
        "reduz a dependência de combustíveis fósseis, diminuindo a emissão de CO₂. Essa redução "
        "de emissões pode gerar créditos de carbono, se o projeto estiver certificado.\n\n"
        "Exemplo:\n\n"
        "   > Um sistema solar de 100 kWp pode evitar a emissão de várias toneladas de CO₂ por ano, "
        "dependendo da matriz energética local.\n"
        "   > Com certificação, cada tonelada evitada pode se tornar um crédito de carbono negociável.\n\n"
        "Tipos de investimentos:\n\n"
        "1. Solar própria: instalar painéis solares no seu negócio ou residência. "
        "A compensação é indireta (você reduz suas próprias emissões).\n\n"
        "2. Projetos de terceiros: investir em usinas solares certificadas que geram créditos de carbono. "
        "Nesse caso, você compra créditos ou financia projetos que produzem créditos.\n\n"
        "3. Fundos de carbono ou green bonds: fundos que investem em energia renovável e geram créditos "
        "de carbono para investidores.\n\n"
        "Certificação:\n\n"
        "Para que o investimento conte como compensação oficial, ele precisa ser certificado por padrões "
        "reconhecidos, como:\n"
        "   • VCS (Verified Carbon Standard)\n"
        "   • Gold Standard\n"
        "   • CCB (Climate, Community & Biodiversity Standards)\n\n"
        "A certificação garante que a redução de CO₂ é real, mensurável e adicional (não ocorreria sem o projeto)."
    )

    label_texto = tk.Label(
        scroll_frame,
        text=texto_label,
        font=("Arial", 10),
        justify="left",
        wraplength=500,
        bg="#f2f2f2"
    )
    label_texto.pack(pady=10, padx=20, fill="x")


    ##################################==--
    # CÁLCULO DE INVESTIMENTO
    ##################################==--
     ##Mostra o valor estimado a ser investido em energia solar==--
    tk.Label(
        scroll_frame,
        text="Valor a ser investido em Energia Solar:",
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
    # SCROLL E ROLAGEM COM O MOUSE
    ##################################==--
     ##Permite rolar o conteúdo com o mouse, compatível com Windows e Linux==--
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
    # ATUALIZAÇÃO AUTOMÁTICA
    ##################################==--
     ##Atualiza periodicamente o valor do crédito e o investimento exibido==--
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
