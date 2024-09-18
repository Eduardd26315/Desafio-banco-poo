from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime



class Cliente(ABC):
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
            transacao.registrar(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    _contador_contas = 1  # Variável de classe para gerar número de contas únicas

    def __init__(self, cliente, agencia="0001"):
        self._saldo = 0.0  # Atributo privado
        self._numero = Conta._contador_contas  # Atributo privado para o número da conta
        Conta._contador_contas += 1  # Incrementa o contador de contas
        self._agencia = agencia  # Atributo privado
        self._cliente = cliente  # Atributo privado
        self._historico = Historico()  # Cada conta tem um histórico próprio

    # Getter e Setter para o saldo
    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if valor < 0:
            print("Erro! O saldo não pode ser negativo.")
        else:
            self._saldo = valor

    # Getter e Setter para o número da conta (somente leitura)
    @property
    def numero(self):
        return self._numero

    # Getter e Setter para a agência
    @property
    def agencia(self):
        return self._agencia

    @agencia.setter
    def agencia(self, valor):
        if isinstance(valor, str):
            self._agencia = valor
        else:
            print("Erro! O valor da agência deve ser uma string.")

    # Getter e Setter para o cliente
    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, cliente):
        if isinstance(cliente, Cliente):
            self._cliente = cliente
        else:
            print("Erro! O cliente deve ser uma instância da classe Cliente.")

    # Getter para o histórico (somente leitura)
    @property
    def historico(self):
        return self._historico

    # Método para sacar dinheiro
    def sacar(self, valor):
        if valor <= 0:
            print("Erro! Valor de saque inválido.")
            return False
        if valor > self._saldo:
            print("Erro! Saldo insuficiente.")
            return False
        self._saldo -= valor
        self._historico.adicionar_transacao(Saque(valor))
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        return True

    # Método para depositar dinheiro
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(Deposito(valor))
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
            return True
        else:
            print("Erro! Valor de depósito inválido.")
            return False

    # Método para exibir o extrato da conta
    def exibir_extrato(self):
        print(f"\nExtrato da conta {self._numero}:")
        self._historico.exibir()
        print(f"Saldo atual: R$ {self._saldo:.2f}")

class ContaCorrente(Conta):
    def __init__(self, cliente, limite=500, limite_saques=3):
        super().__init__(cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        if self._saques_realizados >= self._limite_saques:
            print("Erro! Número máximo de saques atingido.")
        elif valor > self._limite:
            print(f"Erro! O valor do saque excede o limite de R$ {self._limite:.2f}.")
        else:
            saque = Saque(valor)
            saque.registrar(self)
            self._saques_realizados += 1

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()

    def registrar(self, conta):
        if self.valor > 0:
            conta._saldo += self.valor
            conta.historico.adicionar_transacao(self)
            print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso!")
        else:
            print("Erro! Valor inválido para depósito.")

    def __str__(self):
        return f"Depósito de R$ {self.valor:.2f} em {self.data}"

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass



class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()

    def registrar(self, conta):
        if self.valor <= 0:
            print("Erro! Valor inválido para saque.")
        elif self.valor > conta._saldo:
            print("Erro! Saldo insuficiente.")
        else:
            conta._saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso!")

    def __str__(self):
        return f"Saque de R$ {self.valor:.2f} em {self.data}"


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def exibir(self):
        if not self.transacoes:
            print("Nenhuma transação realizada.")
        else:
            for transacao in self.transacoes:
                print(transacao)



# Exemplo de uso do sistema bancário
def main():
    # Criando cliente
    cliente1 = PessoaFisica(cpf="12345678900", nome="João da Silva", data_nascimento="01/01/1990", endereco="Rua A, 100")
    
    # Criando conta corrente para o cliente
    conta_corrente1 = ContaCorrente(cliente=cliente1)
    cliente1.adicionar_conta(conta_corrente1)
    
    # Realizando transações
    cliente1.realizar_transacao(conta_corrente1, Deposito(1000))
    cliente1.realizar_transacao(conta_corrente1, Saque(200))
    
    # Exibindo extrato
    conta_corrente1.exibir_extrato()

if __name__ == "__main__":
    main()
