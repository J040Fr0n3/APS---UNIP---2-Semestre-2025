##################################==--
# python/page_compensar.py
##################################==--
 ##Criação da janela principal com sidebar animada e páginas dinâmicas==--

import tkinter as tk
from pathlib import Path
from python.paginas import carbono, reflorestamento, eolica, solar, coleta


##################################==--
# CONFIGURAÇÕES GERAIS
##################################==--
 ##Constantes visuais e mapeamento das páginas==--
SIDE_BAR_WIDTH_MIN = 45
SIDE_BAR_WIDTH_MAX = 250
SIDE_BAR_COLOR = "#383838"
CONTENT_BG = "#f2f2f2"

PAGINAS = {
    "carbono": carbono,
    "reflorestamento": reflorestamento,
    "energia_eolica": eolica,
    "energia_solar": solar,
    "coleta": coleta,
}


##################################==--
# FUNÇÃO PRINCIPAL
##################################==--
def criar_pagina_compensar(root, trocar_pagina=None):
    """Cria a janela principal com sidebar animada e páginas dinâmicas."""
    base_dir = Path(__file__).parent
    imagens_dir = base_dir / "imagens"

    ##################################==--
    # CARREGAMENTO DE ÍCONES
    ##################################==--
     ##Carrega imagens de forma dinâmica conforme o nome das páginas==--
    icones = {
        nome: tk.PhotoImage(file=imagens_dir / f"{nome}.png")
        for nome in ["toggle_btn_icon", "close_btn_icon", "cc", "coleta", "eolica", "solar", "reflorestamento"]
    }

    ##################################==--
    # ESTRUTURA BASE DA INTERFACE
    ##################################==--
     ##Frame principal e organização entre sidebar e conteúdo==--
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    side_bar = tk.Frame(frame, bg=SIDE_BAR_COLOR, width=SIDE_BAR_WIDTH_MIN)
    side_bar.pack(side=tk.LEFT, fill=tk.Y)
    side_bar.pack_propagate(False)

    content_frame = tk.Frame(frame, bg=CONTENT_BG)
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    lb_indicator = tk.Label(side_bar, bg="white")
    lb_indicator.place(x=3, y=130, height=45, width=3)


    ##################################==--
    # FUNÇÕES AUXILIARES
    ##################################==--
     ##Funções para animação, troca de página e controle visual==--

    def animate(expand=True):
        """Anima expansão/retração da sidebar."""
        width = side_bar.winfo_width()
        step = 10 if expand else -10
        target = SIDE_BAR_WIDTH_MAX if expand else SIDE_BAR_WIDTH_MIN

        if (expand and width >= target) or (not expand and width <= target):
            return
        side_bar.config(width=width + step)
        frame.after(8, lambda: animate(expand))

    def expand_menu():
        animate(True)
        toggle_btn.config(image=icones["close_btn_icon"], command=contract_menu)

    def contract_menu():
        animate(False)
        toggle_btn.config(image=icones["toggle_btn_icon"], command=expand_menu)

    def mover_indicator(y_destino):
        """Anima o indicador lateral suavemente."""
        y_inicial = lb_indicator.winfo_y()
        passos = 40
        delta = (y_destino - y_inicial) / passos

        def passo(i=0):
            if i >= passos:
                lb_indicator.place(y=y_destino)
                return
            lb_indicator.place(y=y_inicial + delta * i)
            frame.after(4, lambda: passo(i + 1))

        passo()

    def limpar_content():
        """Remove widgets anteriores do conteúdo principal."""
        for widget in content_frame.winfo_children():
            widget.destroy()

    def mostrar_pagina(nome):
        """Carrega e mostra uma página específica no conteúdo."""
        limpar_content()
        pagina_modulo = PAGINAS.get(nome)
        if pagina_modulo:
            pagina_modulo.criar_pagina(content_frame)
        else:
            tk.Label(content_frame, text="Página não encontrada!", fg="red", font=("Arial", 16)).pack(pady=40)

    def mudar_cor_sidebar(cor, y_destino, nome_pagina):
        """Atualiza cor da sidebar e troca de página."""
        side_bar.config(bg=cor)
        toggle_btn.config(bg=cor, activebackground=cor)
        
        # Atualiza botões e legendas
        for btn in botoes_sidebar:
            btn.config(bg=cor, activebackground=cor)
        for lbl in legendas_sidebar:
            lbl.config(bg=cor)
        
        mover_indicator(y_destino)
        mostrar_pagina(nome_pagina)


    ##################################==--
    # SIDEBAR, BOTÕES E LEGENDAS
    ##################################==--
     ##Criação dos botões e legendas com animações e ícones==--

    toggle_btn = tk.Button(
        side_bar, image=icones["toggle_btn_icon"], bg=SIDE_BAR_COLOR, bd=0,
        activebackground=SIDE_BAR_COLOR, command=expand_menu
    )
    toggle_btn.place(x=4, y=10)

    botoes_sidebar = []
    legendas_sidebar = []

    botoes_config = [
        ("cc", "C.Carbono", 130, "#383838", "carbono"),
        ("reflorestamento", "Reflorestamento", 190, "#29ab24", "reflorestamento"),
        ("eolica", "E.Eólica", 250, "#8c4318", "energia_eolica"),
        ("solar", "E.Solar", 310, "#d99400", "energia_solar"),
        ("coleta", "Coleta", 370, "#008aff", "coleta"),
    ]

    for icone, texto, y, cor, nome_pagina in botoes_config:
        # Botão lateral
        btn = tk.Button(
            side_bar, image=icones[icone], bg=SIDE_BAR_COLOR, bd=0,
            activebackground=SIDE_BAR_COLOR,
            command=lambda c=cor, y=y, n=nome_pagina: (contract_menu(), mudar_cor_sidebar(c, y, n))
        )
        btn.place(x=9, y=y, width=32, height=40)
        botoes_sidebar.append(btn)

        # Legenda do botão
        lbl = tk.Label(
            side_bar, text=texto, fg="white", bg=SIDE_BAR_COLOR, font=("Arial", 15, "bold")
        )
        lbl.place(x=45, y=y)
        lbl.bind('<Button-1>', lambda event, c=cor, y=y, n=nome_pagina: (contract_menu(), mudar_cor_sidebar(c, y, n)))
        legendas_sidebar.append(lbl)


    ##################################==--
    # PÁGINA INICIAL
    ##################################==--
     ##Define a página inicial exibida ao abrir o programa==--
    mostrar_pagina("carbono")

    return frame


##################################==--
# EXECUÇÃO DIRETA (TESTE)
##################################==--
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Painel de Compensação Ambiental")
    root.geometry("1000x600")
    criar_pagina_compensar(root)
    root.mainloop()
