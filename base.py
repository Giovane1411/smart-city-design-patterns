# Esse projeto é referente ao trabalho final da Disciplina de Projeto de Software.
# Os códigos serão comentados para que o público do GitHub possa aprender sobre boas práticas de arquitetura de software.
# Dedico essa parte ao professor Lucas, que teve um papel muito importante no meu aprendizado sobre arquitetura de software.
# Atenciosamente, Giovane da Silva Gobeti.

from abc import ABC, abstractmethod  # Importa as ferramentas de classe abstrata para firmar contratos que as subclasses serão obrigadas a implementar.

# ==========================================
# 1. COMPONENTES DO OBSERVER (Eventos)
# ==========================================

# Aqui eu tenho a central de alertas: é o que faz a intermediação entre o sensor e o órgão público.
# É o Publicador (Subject) do padrão Observer.
class CentralAlertas(ABC):
    """Subject (Publicador)"""
    def __init__(self):  # Construtor com a lista de "inscrição" dos órgãos públicos que vão receber as notificações.
        self._orgaos_interessados = []

    def registrar_orgao(self, orgao):  # Método responsável por inscrever um órgão na lista.
        self._orgaos_interessados.append(orgao)

    def notificar_emergencia(self, local, tipo_emergencia):  # Aqui é o coração do padrão Observer.
        # Recebo o local e o tipo de emergência vindos do sensor.
        # Percorro cada órgão registrado e notifico cada um com o local e o tipo de emergência.
        for orgao in self._orgaos_interessados:
            orgao.update(local, tipo_emergencia)

# A classe que vai receber da central de alertas as informações de local e tipo_emergencia.
# É o Assinante (Observer).
class OrgaoPublico(ABC):
    """Observer (Assinante)"""
    @abstractmethod
    def update(self, local, tipo_emergencia): pass


# Lembre-se: usamos classe abstrata porque ela garante que o contrato (os métodos abstratos) será implementado pelas subclasses.
# Isso mantém o sistema expansível: podemos adicionar novas tecnologias respeitando a mesma interface.
# =================================================
# 2. COMPONENTES DA ESTRUTURA (Composite & Visitor)
# =================================================

# O padrão Visitor é interessante quando o tipo da classe não precisa de alteração.
# Ele é viável em contextos onde toda hora precisamos adicionar uma operação nova sem mexer na classe de origem.
# Isto é, respeitando o princípio Aberto/Fechado: se uma classe já foi implementada, não devemos mexer nela, para evitar bugs depois.
# Neste caso, criamos a classe abstrata e seus filhos que herdam dela.

# Aqui estou obrigando todas as classes que herdarem de Visitor a implementar visit_sensor_temperatura, visit_sensor_fumaca e visit_regiao.
class Visitor(ABC):
    @abstractmethod  # Marca o método como obrigatório na implementação das subclasses.
    def visit_sensor_temperatura(self, sensor): pass
    @abstractmethod
    def visit_sensor_fumaca(self, sensor): pass
    @abstractmethod
    def visit_regiao(self, regiao): pass

# Aqui implemento o contrato do Composite. A ideia é tratar todas as peças da estrutura como uma árvore,
# eliminando cadeias de IFs (isinstance) do projeto graças ao polimorfismo.
class ComponenteIoT(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

# ------------------------------------------------------------
# Composite: a classe Regiao
# ------------------------------------------------------------

# Aqui implemento a árvore (Composite). A "região" é um conceito que engloba Zona, Bairro e Rua.
# Depois, se eu quiser percorrer um bairro, começo pela zona e desço até o bairro.
# Por exemplo, se quero saber quantas ruas um bairro tem, eu pergunto à zona:
# "Quantas ruas você tem?" A zona não sabe sozinha; ela pede a informação aos seus subramos e devolve o total.

# Todo elemento que existe num Composite é um componente. Então cada vez que adiciono um filho, a ramificação aumenta,
# até chegar nas folhas, que são o fim.

# De forma análoga, funciona assim: Região (Zona -> Bairro -> Rua) -> Sensor (Folha)

class Regiao(ComponenteIoT):
    def __init__(self, nome):
        self.nome = nome   # Nome da região (Zona, Bairro ou Rua)
        self._filhos = []  # a lista de filhos (Regioes ou Sensores)

    def adicionar_filho(self, componente):  # Aumenta a ramificação da árvore
        self._filhos.append(componente)

    # Aqui recebo o visitor e devolvo os dados da região (self) de volta para o visitor.
    # Isso é bom, pois posso criar várias operações sem mexer na classe; ela só precisa do accept.
    def accept(self, visitor: Visitor):
        visitor.visit_regiao(self)  # Aqui a região visita ela mesma

# ------------------------------------------------------------
# Leafs: SensorTemperatura e SensorFumaca
# ------------------------------------------------------------

# Os sensores são as folhas, o ponto final do ramo das regiões.
class SensorTemperatura(ComponenteIoT):
    def __init__(self, nome, bateria):  # Atributos do sensor de temperatura: nome e bateria
        self.nome = nome
        self.bateria = bateria

    # Aqui aceito o visitor e, por sua vez, o accept rebate ao visitor os dados (nome e bateria).
    # Depois o método do visitor faz o que quiser com os dados que recebeu da classe SensorTemperatura.
    def accept(self, visitor: Visitor):
        return visitor.visit_sensor_temperatura(self)  # Esse self significa que vão inclusos os dados da classe

# Outra folha é o SensorFumaca, com atributos nome, bateria, nivel_fumaca e central (a própria central de alertas).
class SensorFumaca(ComponenteIoT):
    def __init__(self, nome, bateria, nivel_fumaca, central):
        self.nome = nome
        self.bateria = bateria
        self.nivel_fumaca = nivel_fumaca
        self.central = central  # conhece a CENTRAL, nunca os órgãos

    # Mesmo esquema: recebe o visitor e devolve a ele os próprios dados da classe SensorFumaca.
    def accept(self, visitor: Visitor):
        return visitor.visit_sensor_fumaca(self)

    # Se o nível de fumaça passar de 80, notifica a emergência informando o local e o tipo (fumaça).
    def verificar_fumaca(self, local):
        if self.nivel_fumaca > 80:
            self.central.notificar_emergencia(local, "fumaça")  # a central se encarrega de avisar Bombeiros e Hospital

# ------------------------------------------------------------
# Visitors: RelatorioXMLVisitor e DiagnosticoBateriaVisitor
# ------------------------------------------------------------

# Aqui temos classes do tipo Visitor. Elas entram como parâmetro no accept, e o accept rebate
# os dados da classe de origem ao visitor. Neste caso, o visitor abaixo é o RelatorioXMLVisitor.
class RelatorioXMLVisitor(Visitor):
    def __init__(self):
        self.xml = ""  # Acumula o resultado de cada visita para exibir o documento completo no final

    # Com os dados vindos da classe do sensor de temperatura, consigo montá-los em XML.
    # Registra cada sensor de temperatura e acumula na variável xml.
    def visit_sensor_temperatura(self, sensor):
        self.xml += f"<sensor tipo='temperatura' nome='{sensor.nome}'/>\n"

    def visit_sensor_fumaca(self, sensor):
        self.xml += f"<sensor tipo='fumaca' nome='{sensor.nome}'/>\n"

    # O que acontece aqui? Eu percorro a árvore inteira.
    # Começo pela zona; se houver zona sul e norte, percorro uma e depois a outra, com todos os bairros e suas ruas.
    def visit_regiao(self, regiao):
        self.xml += f"<regiao nome='{regiao.nome}'>\n"
        for filho in regiao._filhos:  # Acesso cada filho (ramificação) da região.
            filho.accept(self)        # Pode ser tanto região quanto sensor: isto é polimorfismo.
        self.xml += "</regiao>\n"     # Fecha a região, para o XML ficar organizado e aninhado.

# Aqui busco o diagnóstico da bateria, percorrendo toda a árvore para visitar todos os sensores.
# Com os dados que a classe de origem rebateu ao visitor, consigo manipulá-los.
class DiagnosticoBateriaVisitor(Visitor):
    def visit_sensor_temperatura(self, sensor):
        print(f"Bateria {sensor.nome}: Em {sensor.bateria}%")  # Ex.: 44% de bateria
    def visit_sensor_fumaca(self, sensor):
        print(f"Bateria {sensor.nome}: Em {sensor.bateria}%")
    def visit_regiao(self, regiao):
        print(f"Região: {regiao.nome}")
        for filho in regiao._filhos:
            filho.accept(self)

# ------------------------------------------------------------
# Observers concretos: CorpoDeBombeiros e Hospital
# ------------------------------------------------------------

# As classes CorpoDeBombeiros e Hospital recebem da central de alertas o local e o tipo_emergencia.
class CorpoDeBombeiros(OrgaoPublico):
    def update(self, local, tipo_emergencia):
        print(f"Bombeiros acionados. Emergência de {tipo_emergencia} em {local}")

class Hospital(OrgaoPublico):
    def update(self, local, tipo_emergencia):
        print(f"Hospital acionado. Emergência de {tipo_emergencia} em {local}")