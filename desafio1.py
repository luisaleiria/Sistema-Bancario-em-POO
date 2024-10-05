from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Conta():
    def __init__(self, saldo, numero, agencia, cliente, historico):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def novaConta(cls, cliente, numero, agencia):
       return cls(0, numero, agencia, cliente, [])
    
    def sacar(self, valor):
        saldo = self.saldo
        if valor > saldo:
            print("O valor digitado é maior que seu saldo")
            return False

        elif valor <= 0:
            print("Impossivel sacar valores negativos")
            return False
    
        self._saldo = self._saldo - valor
        print("Saque realizado")
        return True
        
    def depositar(self, valor):
        if valor < 0:
            print("Impossivel depositar valores negativos")
            return False
    
        self._saldo = self._saldo + valor
        print("Deposito realizado")
        return True
    
class ContaCorrente (Conta):
    def __init__(self, saldo, numero, agencia, cliente, historico, limite=500, limiteSaques=3):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self.limite = limite
        self.limiteSaques = limiteSaques

    def sacar(self,valor):
        qtdSaques = len(
            [transacao for transacao in self.historico.transacoes 
                if transacao["tipo"] == "Saque"]
        )

        if valor > self.limite:
            print("Valor do saque maior que o limite")
            return False

        if qtdSaques >= self.limiteSaques:
            print("Excedeu o numero de saques possiveis diariamente")
            return False

        else:
            return super().sacar(valor)
        
    def depositar(self, valor):
        return super().depositar(valor)
    
    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            Conta Corrente:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionarTransacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__, #saque ou deposito
                "valor" : transacao.valor,
                "data": datetime.datetime.now()
            }
        )

class Cliente():
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizarTransacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionarConta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, dtNascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.dtNascimento = dtNascimento
        self.contas = []

class Transacao(ABC):
    @abstractclassmethod
    def registrar(self, conta):
        pass

    @property
    @abstractproperty
    def valor(self):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionarTransacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionarTransacao(self)

    
