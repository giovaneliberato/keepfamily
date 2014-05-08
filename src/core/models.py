import md5
from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    passwd = ndb.StringProperty(required=True)

    @classmethod
    def get_by_username_and_pw(cls, username, pw):
        return cls.query(cls.username == username, cls.passwd == pw).get()

    @classmethod
    def get_by_username(cls, username):
        return cls.query(cls.username == username).get()


TIPOS_DESPESAS = ('FIXA', 'RECORRENTE', 'AVULSA')

class Despesa(ndb.Model):
    tipo = ndb.StringProperty(required=True, choices=TIPOS_DESPESAS)
    nome_produto_servico = ndb.StringProperty(required=True)
    beneficiario = ndb.StringProperty(required=True)
    valor = ndb.FloatProperty(required=True)
    numero_parcelas = ndb.IntegerProperty()
    user_id = ndb.IntegerProperty(required=True)
    dia_vencimento = ndb.IntegerProperty()
    criacao = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def criar_despesa_fixa(cls, nome_produto_servico, beneficiario, valor, numero_parcelas,
                           dia_vencimento, user_id, **kwargs):
        despesa = cls()
        despesa.tipo = 'FIXA'
        despesa.nome_produto_servico = nome_produto_servico
        despesa.beneficiario = beneficiario
        despesa.valor = float(valor)
        despesa.numero_parcelas = int(numero_parcelas)
        despesa.dia_vencimento = int(dia_vencimento)
        despesa.user_id = user_id
        despesa.put()
        return despesa

    @classmethod
    def buscar_por_usuario(cls, user_id):
        return cls.query(cls.user_id == user_id).fetch(1000)