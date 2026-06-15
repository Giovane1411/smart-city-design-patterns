from abc import ABC, abstractmethod

# ==========================================
# 1. COMPONENTES DO OBSERVER (Eventos)
# ==========================================
class CentralAlertas(ABC):
    """Subject (Publicador)"""
    def __init__(self):
        self._orgaos_interessados = []

    def registrar_orgao(self, orgao):
        self._orgaos_interessados.append(orgao)

    def notificar_emergencia(self, local, tipo_emergencia):
        for orgao in self._orgaos_interessados:
            orgao.update(local, tipo_emergencia)

class OrgaoPublico(ABC):
    """Observer (Assinante)"""
    @abstractmethod
    def update(self, local, tipo_emergencia): pass


# ==========================================
# 2. COMPONENTES DA ESTRUTURA (Composite & Visitor)
# ==========================================
class Visitor(ABC):
    @abstractmethod
    def visit_sensor_temperatura(self, sensor): pass
    @abstractmethod
    def visit_sensor_fumaca(self, sensor): pass
    @abstractmethod
    def visit_regiao(self, regiao): pass

class ComponenteIoT(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor): 
        pass

# TODO: Implementar a classe Regiao (Composite)
class Regiao(ComponenteIoT):
    def __init__(self, nome):
        self.nome = nome
        self._filhos = [] # a lista de filhos (Regioes ou Sensores)
    
    def adicionar_filho(self, componente): # Aumentando a "ramificação da árvore"
        self._filhos.append(componente)

    def accept(self, visitor: Visitor):
        visitor.visit_regiao(self)     # Aqui a região visita ela mesma
    
# TODO: Implementar SensorTemperatura e SensorFumaca (Leafs)
class SensorTemperatura(ComponenteIoT):
    def __init__(self, nome, bateria):
        self.nome = nome
        self.bateria = bateria

    def accept(self, visitor: Visitor):
        return visitor.visit_sensor_temperatura(self)

class SensorFumaca(ComponenteIoT):
    def __init__(self, nome, bateria, nivel_fumaca, central):
        self.nome = nome
        self.bateria = bateria
        self.nivel_fumaca = nivel_fumaca
        self.central = central     # conhece a CENTRAL, nunca os órgãos

    def accept(self, visitor: Visitor):
        return visitor.visit_sensor_fumaca(self)
    
    def verificar_fumaca(self, local):
        if self.nivel_fumaca > 80:
            self.central.notificar_emergencia(local, "fumaça") # a central se encarrega de avisar Bombeiros e Hospital

# TODO: Implementar RelatorioXMLVisitor e DiagnosticoBateriaVisitor
class RelatorioXMLVisitor(Visitor):
    def __init__(self):
        self.xml = "" # Acumula resultado para cada visita para posteriormente exibir o resultado o final
    
    def visit_sensor_temperatura(self, sensor):
        self.xml += f"<sensor tipo='temperatura' nome='{sensor.nome}'/>\n"

    def visit_sensor_fumaca(self, sensor):
        self.xml += f"<sensor tipo='fumaca' nome='{sensor.nome}'/>\n"

    def visit_regiao(self, regiao):
        self.xml += f"<regiao nome='{regiao.nome}'>\n"
        for filho in regiao._filhos:       # E posteriormente consigo acessar cada filho ou ramificação da região.
            filho.accept(self)             # Pode englobar tanto região quanto sensores, isto é, polimorfismo 
        self.xml += "</regiao>\n"
                                       

class DiagnosticoBateriaVisitor(Visitor):
    def visit_sensor_temperatura(self, sensor):
        print(f"Bateria {sensor.nome}: Em {sensor.bateria}%") # Ex. 44% de bateria
    def visit_sensor_fumaca(self, sensor):
        print(f"Bateria {sensor.nome}: Em {sensor.bateria}%")
    def visit_regiao(self, regiao):
        print(f"Região: {regiao.nome}")
        for filho in regiao._filhos:
            filho.accept(self)

# TODO: Implementar CorpoDeBombeiros e Hospital (Observers)

class CorpoDeBombeiros(OrgaoPublico):
    def update(self, local, tipo_emergencia):
        print(f"Bombeiros acionados. Emergência de {tipo_emergencia} em {local}")

class Hospital (OrgaoPublico):
    def update(self, local, tipo_emergencia):
        print(f"Hospital acionados. Emergência de {tipo_emergencia} em {local}")