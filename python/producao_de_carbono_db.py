# database.py
# Banco de dados de emissões de CO₂ com cálculos baseados em inputs do usuário

# -----------------------------------------------------
# SCORE / VARIÁVEIS GLOBAIS
# -----------------------------------------------------

moeda_C = 0.0  # Crédito de carbono total (kg CO₂)
residuos_solidos = 3
arvore = 0.2
solar_eolica = 0.087


aluminio = 10.00
plastico = 3.00
papel = 1.50
vidro = 0.40


SALVAR = {
    "carro": 0.0,
    "moto": 0.0,
    "onibus": 0.0,
    "metro": 0.0,
    "aviao": 0.0,
    "eletricidade": 0.0,
    "gas": 0.0,
    "banho": 0.0,
    "carne": 0.0,
    "vegetariana": 0.0,
    "vegana": 0.0,
    "streaming": 0.0,
    "pc": 0.0
}
# 1T Papelão/Papel = 4T Co2 /-/ 1T plástico = 2T Co2
# 1 árvore = 0,2 CC
# SOlar / Eólica R$ 75,00 por crédito de carbono 
# -----------------------------------------------------
# FATORES DE EMISSÃO APROXIMADOS (kg CO₂ por unidade)
# -----------------------------------------------------

FATORES = {
    "energia": {
        "eletricidade": 0.4,     # kg CO₂ por kWh
        "gas_cozinha": 2.0,      # kg CO₂ por kg de GLP
        "aquecimento_agua": 0.05 # kg CO₂ por minuto de banho quente
    },
    "alimentacao": {
        "carne": 15.5,       # kg CO₂ por kg de carne
        "vegetariana": 1.3,  # kg CO₂ por refeição vegetariana
        "vegana": 1.0        # kg CO₂ por refeição vegana
    },
    "transporte": {
        "carro_gasolina": 0.12,  # kg CO₂ por km
        "moto": 0.08,            # kg CO₂ por km
        "onibus": 0.08,          # kg CO₂ por km por passageiro
        "metro": 0.05,           # kg CO₂ por km por passageiro
        "voo": 0.25              # kg CO₂ por km
    },
    "tecnologia": {
        "internet_streaming": 0.2, # kg CO₂ por hora
        "smartphone_pc": 0.1       # kg CO₂ por hora
    }
}

# -----------------------------------------------------
# FUNÇÕES DE CÁLCULO
# -----------------------------------------------------

def calcular_energia(eletricidade_kwh=0.0, gas_kg=0.0, banho_min=0.0) -> float:
    """Calcula emissões de energia em kg CO₂/dia"""
    SALVAR["eletricidade"] = eletricidade_kwh / 30 * FATORES["energia"]["eletricidade"]
    SALVAR["gas"] = gas_kg * FATORES["energia"]["gas_cozinha"]
    SALVAR["banho"] = banho_min * FATORES["energia"]["aquecimento_agua"]
    return (SALVAR["eletricidade"] + SALVAR["gas"] + SALVAR["banho"])*30


def calcular_alimentacao(carne_co=0.0, vega_co=0.0, vegeta_co=0.0) -> float:
    """Calcula emissões de alimentação em kg CO₂/dia"""
    SALVAR["carne"] = carne_co * FATORES["alimentacao"]["carne"]
    SALVAR["vegana"] = vega_co * FATORES["alimentacao"]["vegana"]
    SALVAR["vegetariana"] = vegeta_co * FATORES["alimentacao"]["vegetariana"]
    return (SALVAR["carne"] + SALVAR["vegana"] + SALVAR["vegetariana"])*30


def calcular_transporte(carro_km=0.0, moto_km=0.0, onibus_km=0.0, metro_km=0.0, voo_km=0.0) -> float:
    """Calcula emissões de transporte em kg CO₂/dia"""
    SALVAR["carro"] = carro_km * FATORES["transporte"]["carro_gasolina"]
    SALVAR["moto"] = moto_km * FATORES["transporte"]["moto"]
    SALVAR["onibus"] = onibus_km * FATORES["transporte"]["onibus"]
    SALVAR["metro"] = metro_km * FATORES["transporte"]["metro"]
    SALVAR["aviao"] = voo_km / 30 * FATORES["transporte"]["voo"]
    return (SALVAR["carro"] + SALVAR["moto"] + SALVAR["onibus"] + SALVAR["metro"] + SALVAR["aviao"])*30


def calcular_tecnologia(horas_streaming=0.0, horas_pc=0.0) -> float:
    """Calcula emissões de tecnologia em kg CO₂/dia"""
    SALVAR["streaming"] = horas_streaming * FATORES["tecnologia"]["internet_streaming"]
    SALVAR["pc"] = horas_pc * FATORES["tecnologia"]["smartphone_pc"]
    return (SALVAR["streaming"] + SALVAR["pc"])*30


def calcular_total_diario(**kwargs) -> float:
    """
    Calcula o total diário de CO₂.
    Aceita kwargs:
        energia: eletricidade_kwh, gas_kg, banho_min
        alimentacao: carne_co, vega_co, vegeta_co
        transporte: carro_km, moto_km, onibus_km, metro_km, voo_km
        tecnologia: horas_streaming, horas_pc
    """
    total = 0.0
    total += calcular_energia(**kwargs.get("energia", {}))
    total += calcular_alimentacao(**kwargs.get("alimentacao", {}))
    total += calcular_transporte(**kwargs.get("transporte", {}))
    total += calcular_tecnologia(**kwargs.get("tecnologia", {}))
    return total
