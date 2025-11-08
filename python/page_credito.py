##################################==--
# python/page_credito.py
##################################==--
## Página "Crédito de Carbono" — cálculo e exibição de resultados individuais e totais
import tkinter as tk
from tkinter import ttk

##################################==--
# IMPORTAÇÃO CONDICIONAL PARA TESTE LOCAL
##################################==--
## Usa o módulo local em modo de teste ou o módulo real do pacote principal
Teste = False
if Teste is True:
    import producao_de_carbono_db
else:
    from python import producao_de_carbono_db


##################################==--
# FUNÇÃO PRINCIPAL: CRIAR PÁGINA CRÉDITO
##################################==--
## Cria a página de cálculo de créditos de carbono com formulário, scroll e resultados
def criar_pagina_credito(root, trocar_pagina):
    container = ttk.Frame(root)


    ##################################==--
    # VALIDAÇÃO DE ENTRADAS
    ##################################==--
    ## Permite apenas números nos campos de entrada
    def apenas_numeros(P):
        return P.isdigit() or P == ""

    vcmd = (container.register(apenas_numeros), "%P")


    ##################################==--
    # EXIBIÇÃO DO CRÉDITO ATUAL
    ##################################==--
    ## Mostra o valor atual de crédito acumulado
    frame_borda = tk.Frame(container, highlightbackground="black", highlightthickness=2, width=230, height=35)
    frame_borda.pack(padx=20, pady=20, anchor="e")
    frame_borda.pack_propagate(False)

    lbl_credito = tk.Label(
        frame_borda,
        text=f"Crédito Mês: {producao_de_carbono_db.moeda_C:.2f}",
        font=("Bold", 15)
    )
    lbl_credito.pack()


    ##################################==--
    # CANVAS COM SCROLL
    ##################################==--
    ## Cria o container rolável para o conteúdo
    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    frame_interno = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_interno, anchor="nw")

    frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    ## Ativa/desativa o scroll com o mouse
    def on_mousewheel(event):
        canvas.yview_scroll(-int(event.delta / 120), "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    ##################################==--
    # TÍTULO E TEXTO EXPLICATIVO
    ##################################==--
    ## Apresenta informações sobre o que é Crédito de Carbono
    tk.Label(frame_interno, text="O que é Crédito de Carbono?", font=("Bold", 20)).pack(pady=10)

    texto_info = (
        "Crédito de Carbono\n\n"
        "O crédito de carbono é um certificado que representa a redução ou remoção de uma tonelada "
        "de dióxido de carbono (CO₂) da atmosfera. Ele funciona como um mecanismo de mercado, permitindo "
        "que empresas e países que emitem mais gases do que o permitido comprem créditos de projetos que "
        "reduzem ou capturam carbono.\n\n"
        "Como funciona\n\n"
        "1. Geração de créditos:\n"
        "Projetos que comprovadamente reduzem emissões — como iniciativas de reflorestamento, energia renovável "
        "ou eficiência energética — podem gerar créditos de carbono.\n\n"
        "2. Mecanismo de mercado:\n"
        "Existem dois tipos principais de mercado de carbono:\n"
        "• Mercado regulado: o governo estabelece limites de emissão, e as empresas podem negociar créditos.\n"
        "• Mercado voluntário: empresas e organizações compram créditos espontaneamente para compensar emissões.\n\n"
        "3. Comercialização:\n"
        "Os créditos podem ser comprados e vendidos entre empresas, países ou organizações, criando um sistema dinâmico.\n\n"
        "4. Ação climática:\n"
        "Ao transferir o custo das emissões para os poluidores, o mercado de carbono estimula investimentos "
        "em tecnologias limpas e projetos sustentáveis, promovendo uma economia de baixo carbono."
    )

    ## Cria área de texto rolável para a explicação
    texto_frame = ttk.Frame(frame_interno)
    texto_frame.pack(padx=20, pady=10, fill="x")

    texto_scroll = ttk.Scrollbar(texto_frame, orient="vertical")
    caixa_texto = tk.Text(
        texto_frame, wrap="word", yscrollcommand=texto_scroll.set,
        width=80, height=12, font=("Segoe UI", 11), relief="flat", padx=10, pady=10
    )

    texto_scroll.config(command=caixa_texto.yview)
    texto_scroll.pack(side="right", fill="y")
    caixa_texto.pack(side="left", fill="both", expand=True)
    caixa_texto.insert("1.0", texto_info)
    caixa_texto.config(state="disabled")

    ## Evita conflito de scroll entre texto e canvas
    caixa_texto.bind("<Enter>", lambda e: canvas.unbind_all("<MouseWheel>"))
    caixa_texto.bind("<Leave>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))


    ##################################==--
    # FORMULÁRIO DE CÁLCULO
    ##################################==--
    ## Campos de entrada para calcular a pegada de carbono
    tk.Label(frame_interno, text="Calculadora de Carbono", font=("Bold", 20)).pack(pady=10)
    tk.Label(frame_interno, text="*Coloque 0 se não utiliza*", font=("Bold", 10)).pack(anchor="w", padx=10)

    frame_inputs = ttk.Frame(frame_interno)
    frame_inputs.pack(padx=10, pady=5, fill="x")

    ## Gerencia ativação do scroll no formulário
    def ativar_scroll(event=None):
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def desativar_scroll(event=None):
        canvas.unbind_all("<MouseWheel>")

    frame_inputs.bind("<Enter>", ativar_scroll)
    frame_inputs.bind("<Leave>", desativar_scroll)


    ##################################==--
    # SCROLL NOS FILHOS DO FORMULÁRIO
    ##################################==--
    ## Aplica eventos de scroll recursivamente a todos os widgets filhos
    def aplicar_scroll_em_filhos(widget):
        for child in widget.winfo_children():
            try:
                child.bind("<Enter>", ativar_scroll)
                child.bind("<Leave>", desativar_scroll)
                aplicar_scroll_em_filhos(child)
            except:
                pass


    ##################################==--
    # RESULTADOS (TABELA)
    ##################################==--
    ## Cria tabela com os resultados individuais e totais
    resultados_labels = {}
    nomes_resultados = [
        "Carro (CO₂):", "Moto (CO₂):", "Ônibus (CO₂):", "Metrô (CO₂):", "Avião (CO₂):",
        "Eletricidade (CO₂):", "Gás (CO₂):", "Banho (CO₂):",
        "Carne (CO₂):", "Vegetariana (CO₂):", "Vegana (CO₂):",
        "Streaming (CO₂):", "PC/Celular (CO₂):",
        "TOTAL TRANSPORTE:", "TOTAL ENERGIA:", "TOTAL ALIMENTAÇÃO:", "TOTAL TECNOLOGIA:",
    ]

    col_base, row_base = 3, 1
    for i, nome in enumerate(nomes_resultados):
        r = row_base + i
        ttk.Label(frame_inputs, text=nome, font=("bold", 10)).grid(row=r, column=col_base, sticky="w")
        lbl = ttk.Label(frame_inputs, text="0", font=("bold", 10))
        lbl.grid(row=r, column=col_base + 1, sticky="w")
        resultados_labels[nome] = lbl


    ##################################==--
    # FUNÇÃO SALVAR DADOS
    ##################################==--
    ## Coleta os valores inseridos, realiza cálculos e atualiza os resultados
    def salvar_dados():
        def get_num(entry):
            try:
                return float(entry.get()) if entry.get() else 0
            except ValueError:
                return 0

        ## Coleta os dados das entradas
        dados = {nome: get_num(e) for nome, e in entradas.items()}

        ## Cálculos por categoria
        producao_de_carbono_db.co2_transporte = producao_de_carbono_db.calcular_transporte(
            carro_km=dados["Carro/Uber (Km/dia):"],
            moto_km=dados["Moto (Km/dia):"],
            onibus_km=dados["Ônibus (Km/dia):"],
            metro_km=dados["Trem/Metrô (Km/dia):"],
            voo_km=dados["Avião (Km/Mês):"]
        )

        producao_de_carbono_db.co2_energia = producao_de_carbono_db.calcular_energia(
            eletricidade_kwh=dados["Eletricidade (kWh/mês):"],
            gas_kg=dados["Gás de Cozinha (dias de duração):"],
            banho_min=dados["Duração do banho (min):"]
        )

        producao_de_carbono_db.co2_alimentacao = producao_de_carbono_db.calcular_alimentacao(
            carne_co=dados["Carne consumida (Kg/dia):"],
            vega_co=dados["Refeições veganas (dia):"],
            vegeta_co=dados["Refeições vegetarianas (dia):"]
        )

        producao_de_carbono_db.co2_tecnologia = producao_de_carbono_db.calcular_tecnologia(
            horas_streaming=dados["Tempo na internet (horas):"],
            horas_pc=dados["Tempo de tela Celular/PC (horas):"]
        )

        ## Soma total de CO₂
        producao_de_carbono_db.moeda_C = (
            producao_de_carbono_db.co2_transporte +
            producao_de_carbono_db.co2_energia +
            producao_de_carbono_db.co2_alimentacao +
            producao_de_carbono_db.co2_tecnologia
        )

        lbl_credito.config(text=f"Crédito: {producao_de_carbono_db.moeda_C / 1000:.2f}")

        ## Atualiza tabela de resultados
        for chave, valor in producao_de_carbono_db.SALVAR.items():
            nome_label = {
                "carro": "Carro (CO₂):", "moto": "Moto (CO₂):", "onibus": "Ônibus (CO₂):",
                "metro": "Metrô (CO₂):", "aviao": "Avião (CO₂):",
                "eletricidade": "Eletricidade (CO₂):", "gas": "Gás (CO₂):", "banho": "Banho (CO₂):",
                "carne": "Carne (CO₂):", "vegetariana": "Vegetariana (CO₂):", "vegana": "Vegana (CO₂):",
                "streaming": "Streaming (CO₂):", "pc": "PC/Celular (CO₂):"
            }.get(chave)

            if nome_label and nome_label in resultados_labels:
                resultados_labels[nome_label].config(text=f"{valor:.2f}")

        resultados_labels["TOTAL TRANSPORTE:"].config(text=f"{producao_de_carbono_db.co2_transporte:.2f}")
        resultados_labels["TOTAL ENERGIA:"].config(text=f"{producao_de_carbono_db.co2_energia:.2f}")
        resultados_labels["TOTAL ALIMENTAÇÃO:"].config(text=f"{producao_de_carbono_db.co2_alimentacao:.2f}")
        resultados_labels["TOTAL TECNOLOGIA:"].config(text=f"{producao_de_carbono_db.co2_tecnologia:.2f}")

        ## Limpa as entradas após o cálculo
        for entry in entradas.values():
            entry.delete(0, tk.END)


    ##################################==--
    # CAMPOS DO FORMULÁRIO
    ##################################==--
    ## Estrutura das seções e respectivos campos de entrada
    secoes = {
        "====-Transportes-====": [
            ("Carro/Uber (Km/dia):", "Km/d"),
            ("Ônibus (Km/dia):", "Km/d"),
            ("Moto (Km/dia):", "Km/d"),
            ("Trem/Metrô (Km/dia):", "Km/d"),
            ("Avião (Km/Mês):", "Km/m"),
        ],
        "====-Energias-====": [
            ("Eletricidade (kWh/mês):", "kWh"),
            ("Gás de Cozinha (dias de duração):", "Dias"),
            ("Duração do banho (min):", "Min"),
        ],
        "====-ALIMENTOS-====": [
            ("Carne consumida (Kg/dia):", "Kg"),
            ("Refeições vegetarianas (dia):", "Refeições"),
            ("Refeições veganas (dia):", "Refeições"),
        ],
        "====-Tecnologia-====": [
            ("Tempo na internet (horas):", "Horas"),
            ("Tempo de tela Celular/PC (horas):", "Horas"),
        ],
    }

    row = 0
    entradas = {}

    ## Função auxiliar para adicionar cada linha do formulário
    def add_linha(label_txt, unidade, r):
        ttk.Label(frame_inputs, text=label_txt, font=("bold", 12)).grid(row=r, column=0, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(frame_inputs, width=15, validate="key", validatecommand=vcmd)
        entry.grid(row=r, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(frame_inputs, text=unidade, font=("bold", 12)).grid(row=r, column=2, sticky="w", padx=5, pady=5)
        return entry

    for secao, campos in secoes.items():
        ttk.Label(frame_inputs, text=secao, font=("bold", 14)).grid(row=row, column=0, columnspan=3, pady=6)
        row += 1
        for texto, unidade in campos:
            entradas[texto] = add_linha(texto, unidade, row)
            row += 1

    aplicar_scroll_em_filhos(frame_inputs)

    ## Botão principal de ação
    tk.Button(
        frame_inputs, text="Salvar", font=("bold", 20), width=30, command=salvar_dados
    ).grid(row=row + 1, column=0, columnspan=3, padx=5, pady=5)


    ##################################==--
    # RETORNO
    ##################################==--
    ## Retorna o container principal da página
    return container


##################################==--
# TESTE LOCAL DA JANELA
##################################==--
## Permite rodar o arquivo individualmente para testes
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Crédito de Carbono")
    root.geometry("800x600")

    pagina = criar_pagina_credito(root, None)
    pagina.pack(fill="both", expand=True)

    root.mainloop()
