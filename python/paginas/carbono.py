##################################==--
# python/paginas/carbono.py
##################################==--
 ##Criação da página de compensação de carbono com diversas opções (reflorestamento, energia, etc)==--

import tkinter as tk
import os
from .. import producao_de_carbono_db


##################################==--
# FUNÇÃO PRINCIPAL
##################################==--
def criar_pagina(parent):
    """Cria a página de compensação de carbono com opções de investimento ambiental."""
    color_content = "#ffffff"

    ##################################==--
    # ÍCONES
    ##################################==--
     ##Carregamento dinâmico dos ícones de cada categoria==--
    base_path = os.path.join(os.path.dirname(__file__), "..", "imagens")
    icones = {
        "reflorestamento": tk.PhotoImage(file=os.path.join(base_path, "reflorestamento.png")),
        "eolica": tk.PhotoImage(file=os.path.join(base_path, "eolica.png")),
        "solar": tk.PhotoImage(file=os.path.join(base_path, "solar.png")),
        "coleta": tk.PhotoImage(file=os.path.join(base_path, "coleta.png")),
    }

    ##################################==--
    # CABEÇALHO E INFORMAÇÕES INICIAIS
    ##################################==--
     ##Título, subtítulo e valor atual de crédito de carbono==--
    tk.Label(
        parent,
        text="Compensação de Carbono 🌍",
        font=("Arial", 20, "bold"),
        bg="#383838",
        fg="white"
    ).pack(pady=20, fill="x")

    label_valor = tk.Label(
        parent,
        text=f"Crédito de Carbono: {producao_de_carbono_db.moeda_C / 1000:.2f}",
        font=("Arial", 14),
        bg="#f2f2f2"
    )
    label_valor.pack(pady=10)

    tk.Label(
        parent,
        text="Converta seu crédito de diversas formas ao mesmo tempo.",
        font=("Arial", 14, "bold"),
        bg="#f2f2f2"
    ).pack(padx=15)


    ##################################==--
    # ATUALIZAÇÃO AUTOMÁTICA DO CRÉDITO
    ##################################==--
     ##Atualiza o valor do crédito de carbono exibido na tela==--
    def atualizar_moeda():
        if not label_valor.winfo_exists():
            return
        valor_atual = producao_de_carbono_db.moeda_C / 1000
        label_valor.config(text=f"Crédito de Carbono: {valor_atual:.2f}")
        parent.after(1000, atualizar_moeda)

    atualizar_moeda()


    ##################################==--
    # FUNÇÃO DE ESTILO DE BOTÕES
    ##################################==--
     ##Aplica cores, efeitos hover e estilo consistente aos botões==--
    def estilizar_botao(botao, cor_base="#29ab24", cor_hover="#34d832", cor_texto="white"):
        botao.config(
            bg=cor_base, fg=cor_texto,
            activebackground=cor_hover, activeforeground=cor_texto,
            relief="flat", bd=0, highlightthickness=0,
            cursor="hand2"
        )
        botao.bind("<Enter>", lambda e: botao.config(bg=cor_hover))
        botao.bind("<Leave>", lambda e: botao.config(bg=cor_base))


    ##################################==--
    # CONTROLE DE SEÇÕES
    ##################################==--
     ##Armazena dados das seções e controla valores acumulados==--
    secoes = []

    leg_total = tk.Label(parent, text="Total de Créditos: 0.00", font=("Arial", 12, "bold"))
    leg_total.place(relx=0.10, rely=0.85)

    def atualizar_total():
        total = sum(sec['valor'] * sec['peso'] for sec in secoes)
        moeda = producao_de_carbono_db.moeda_C / 1000

        if moeda == 0:
            leg_total.config(text="")
        elif total >= moeda:
            leg_total.config(
                text=f"Valor: {total:.2f} — Paga seu Crédito pendente: {moeda:.2f}",
                fg="green"
            )
        else:
            leg_total.config(
                text=f"Valor: {total:.2f} — Não paga seu Crédito pendente: {moeda:.2f}",
                fg="red"
            )


    ##################################==--
    # MULTIPLICADOR DE AÇÕES (x1, x10, x100)
    ##################################==--
     ##Alterna o valor de incremento dos botões de adição==--
    def criar_bnt_vezes(botao, valor_inicial):
        contador = 0
        valor_atual = valor_inicial

        def alterar():
            nonlocal contador, valor_atual
            contador = (contador + 1) % 3
            if contador == 0:
                valor_atual = valor_inicial
            elif contador == 1:
                valor_atual = valor_inicial * 10
            else:
                valor_atual = valor_inicial * 100
            botao.config(text=f"Adicionar: {valor_atual:.0f}x")
            alterar.valor_atual = valor_atual

        alterar.valor_atual = valor_inicial
        return alterar


    ##################################==--
    # CONFIGURAÇÃO DOS BOTÕES DE CONTAGEM
    ##################################==--
     ##Define lógica de incremento, decremento e atualização das legendas==--
    def configurar_botoes_contagem(btn_mais, btn_menos, legenda, func_vezes,
                                   texto_legenda, peso=1, tipo="arvores", limite=None):
        valor = 0.0
        legenda.valor = valor
        secoes.append({'valor': valor, 'peso': peso, 'legenda': legenda})

        def formatar(v):
            if tipo == "reais":
                return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            elif tipo == "toneladas":
                return f"{v:.1f} t"
            else:
                return f"{int(v)}"

        def atualizar_legenda():
            legenda.config(text=f"{texto_legenda}\n\n{formatar(valor)}")
            for sec in secoes:
                if sec['legenda'] == legenda:
                    sec['valor'] = valor
            atualizar_total()

        def adicionar():
            nonlocal valor
            valor += func_vezes.valor_atual
            if limite and valor > limite:
                valor = limite
            atualizar_legenda()

        def remover():
            nonlocal valor
            valor = max(0, valor - func_vezes.valor_atual)
            atualizar_legenda()

        btn_mais.config(command=adicionar)
        btn_menos.config(command=remover)
        atualizar_legenda()


    ##################################==--
    # AJUSTE AUTOMÁTICO DO TEXTO
    ##################################==--
     ##Ajusta a quebra de linha conforme o redimensionamento==--
    def ajustar_wrap(event, *labels):
        nova_largura = event.width - 20
        for lbl in labels:
            lbl.config(wraplength=nova_largura)


    ##################################==--
    # CRIAÇÃO DAS SEÇÕES DE AÇÃO
    ##################################==--
     ##Cada seção representa uma forma de compensação (árvores, energia, coleta)==--
    rely_inicio, rely_fim = 0.30, 0.80
    relheight = rely_fim - rely_inicio

    def criar_secao(relx, titulo, icone, cor, cor_hover, texto_legenda, peso, tipo):
        frame = tk.Frame(parent, bg=color_content)
        frame.place(relx=relx, rely=rely_inicio, relwidth=0.25, relheight=relheight)

        # Ícone e título
        tk.Label(frame, image=icone, bg=color_content).place(relx=0.5, y=2, anchor="n")
        tk.Label(frame, text=titulo, font=("Arial", 12, "bold"), bg=color_content).place(relx=0.5, y=50, anchor="n")

        # Botão multiplicador
        btn_x = tk.Button(frame, text="Adicionar: 1x", font=("Arial", 12))
        estilizar_botao(btn_x, cor, cor_hover)
        btn_x.place(relx=0.5, y=80, anchor="n")
        func_vezes = criar_bnt_vezes(btn_x, 1)
        btn_x.config(command=func_vezes)

        # Legenda
        leg = tk.Label(frame, text="", font=("Arial", 12), bg=color_content, justify="center")
        leg.place(relx=0.5, y=120, anchor="n")
        frame.bind("<Configure>", lambda e: ajustar_wrap(e, leg))

        # Botões + e -
        btn_menos = tk.Button(frame, text="-", font=("Arial", 12, "bold"), width=5)
        estilizar_botao(btn_menos, cor, cor_hover)
        btn_menos.place(relx=0.25, y=230, anchor="n")

        btn_mais = tk.Button(frame, text="+", font=("Arial", 12, "bold"), width=5)
        estilizar_botao(btn_mais, cor, cor_hover)
        btn_mais.place(relx=0.75, y=230, anchor="n")

        configurar_botoes_contagem(btn_mais, btn_menos, leg, func_vezes, texto_legenda, peso, tipo)


    ##################################==--
    # INSERÇÃO DAS SEÇÕES NA INTERFACE
    ##################################==--
     ##Cria visualmente as seções configuradas acima==--
    criar_secao(0.00, "Reflorestamento", icones["reflorestamento"], "#29ab24", "#35c12c",
                "Número de árvores a serem plantadas:", producao_de_carbono_db.arvore, "arvores")

    criar_secao(0.25, "Energia Eólica", icones["eolica"], "#8c4318", "#a85c24",
                "Valor a ser investido em energia Eólica:", producao_de_carbono_db.solar_eolica, "reais")

    criar_secao(0.50, "Energia Solar", icones["solar"], "#d99400", "#f0ac00",
                "Valor a ser investido em energia Solar:", producao_de_carbono_db.solar_eolica, "reais")

    criar_secao(0.75, "Coleta de Resíduos", icones["coleta"], "#008aff", "#33a3ff",
                "Quantidade de Resíduos Sólidos:", producao_de_carbono_db.residuos_solidos, "toneladas")
