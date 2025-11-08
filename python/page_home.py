##################################==--
# python/page_home.py
##################################==--
## Página "Home" da Calculadora de Crédito de Carbono
import tkinter as tk
from tkinter import ttk


##################################==--
# FUNÇÃO PRINCIPAL: CRIAR PÁGINA HOME
##################################==--
## Cria a página inicial com sistema de rolagem e textos explicativos
def criar_pagina_home(root, trocar_pagina):
    """Cria a página de configurações com Scroll."""
    frame = ttk.Frame(root)

    ##################################==--
    # ÁREA COM SCROLL
    ##################################==--
    ## Cria o canvas e adiciona scrollbar vertical
    canvas = tk.Canvas(frame, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    ## Frame interno que conterá o conteúdo da página
    content_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    ## Atualiza a área de rolagem automaticamente conforme o conteúdo
    def update_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", update_scroll)

    ## Habilita o scroll do mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)


    ##################################==--
    # CONTEÚDO PRINCIPAL DA PÁGINA
    ##################################==--
    ## Título principal da aplicação
    titulo = tk.Label(
        content_frame,
        bg="#7C7C7C",
        fg="white",
        text="Calculadora de Crédito de Carbono",
        font=("Arial", 20, "bold")
    )
    titulo.pack(fill=tk.X, padx=0, pady=20)


    ##################################==--
    # SEÇÃO: OBJETIVO DA APLICAÇÃO
    ##################################==--
    ## Título e texto explicativo sobre o propósito da aplicação
    sub_titulo = tk.Label(
        content_frame,
        text="Objetivo da Aplicação",
        font=("Arial", 15, "bold"),
        anchor="w"
    )
    sub_titulo.pack(fill=tk.X, padx=10, pady=(40, 0))

    texto_1 = tk.Label(
        content_frame,
        text=(
            "O objetivo principal desta aplicação é mensurar a Pegada de Carbono Pessoal "
            "de um usuário e, com base nesse cálculo, determinar a quantidade de Créditos "
            "de Carbono necessária para compensar esse impacto ambiental anualmente.\n\n"
            "Um Crédito de Carbono é o certificado de que uma tonelada (1t) de CO₂ "
            "equivalente (CO₂e) deixou de ser emitida ou foi removida da atmosfera.\n\n"
            "Ao usar esta calculadora, você está dando o primeiro passo para entender "
            "e neutralizar seu impacto no aquecimento global."
        ),
        font=("Arial", 12),
        justify="left",
        anchor="w",
        wraplength=750
    )
    texto_1.pack(fill=tk.X, padx=12, pady=(0, 5))


    ##################################==--
    # SEÇÃO: ESTRUTURA DE NAVEGAÇÃO
    ##################################==--
    ## Explica as funções de cada aba da aplicação
    sub_titulo_2 = tk.Label(
        content_frame,
        text="Estrutura de Navegação",
        font=("Arial", 15, "bold"),
        anchor="w"
    )
    sub_titulo_2.pack(fill=tk.X, padx=10, pady=(40, 0))

    texto_2 = tk.Label(
        content_frame,
        text="Utilize as abas acima para interagir com o sistema:",
        font=("bold", 12),
        justify="left",
        anchor="w",
        wraplength=750
    )
    texto_2.pack(fill=tk.X, padx=12, pady=(0, 5))


    ##################################==--
    # SUBSEÇÃO: HOME
    ##################################==--
    ## Descrição da aba "Home"
    sub_titulo_home = tk.Label(
        content_frame,
        text="1 - Home: (Esta Página)",
        font=("Arial", 15, "bold"),
        anchor="w"
    )
    sub_titulo_home.pack(fill=tk.X, padx=20, pady=(5, 0))

    texto_home = tk.Label(
        content_frame,
        text="Apresenta a proposta e a missão da calculadora.",
        font=("bold", 10),
        anchor="w"
    )
    texto_home.pack(fill=tk.X, padx=25, pady=(0, 5))


    ##################################==--
    # SUBSEÇÃO: CRÉDITO
    ##################################==--
    ## Descrição da aba "Crédito"
    sub_titulo_credito = tk.Label(
        content_frame,
        text="2 - Crédito:",
        font=("Arial", 15, "bold"),
        anchor="w"
    )
    sub_titulo_credito.pack(fill=tk.X, padx=20, pady=(5, 0))

    texto_credito = tk.Label(
        content_frame,
        text=(
            "FUNÇÃO PRINCIPAL: É onde você inserirá seus dados de consumo "
            "(transporte, eletricidade, gás, etc.)."
        ),
        font=("bold", 10),
        anchor="w",
        wraplength=750
    )
    texto_credito.pack(fill=tk.X, padx=25, pady=(0, 5))


    ##################################==--
    # SUBSEÇÃO: COMPENSAR
    ##################################==--
    ## Descrição da aba "Compensar"
    sub_titulo_compensar = tk.Label(
        content_frame,
        text="3 - Compensar:",
        font=("Arial", 15, "bold"),
        anchor="w"
    )
    sub_titulo_compensar.pack(fill=tk.X, padx=20, pady=(5, 0))

    texto_compensar = tk.Label(
        content_frame,
        text=(
            "COMPENSAÇÃO: Esta seção exibe o resultado da aba 'Crédito' de forma "
            "simplificada, indicando quantos Créditos de Carbono (toneladas de CO₂e) "
            "você precisaria adquirir para neutralizar seu impacto ambiental."
        ),
        font=("bold", 10),
        anchor="w",
        wraplength=750
    )
    texto_compensar.pack(fill=tk.X, padx=25, pady=(0, 5))


    ##################################==--
    # RETORNO
    ##################################==--
    ## Retorna o frame principal para exibição
    return frame
