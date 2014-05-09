#coding: utf-8
import md5
from google.appengine.ext import ndb
from google.appengine.ext.ndb.polymodel import PolyModel


CATEGORIAS_DEFAULT = [u"Alimentação", u"Animal de estição", u"Casa", u"Educação",
                      u"Filhos", u"Lazer", u"Saúde", u"Veículo", u"Outros"]

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


class Despesa(PolyModel):
    nome_produto_servico = ndb.StringProperty(required=True)
    user_id = ndb.IntegerProperty(required=True)
    valor = ndb.FloatProperty(required=True)
    beneficiario = ndb.StringProperty(required=True)
    categoria = ndb.StringProperty(required=True, choices=CATEGORIAS_DEFAULT)
    criacao = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def buscar_por_usuario(cls, user_id):
        return cls.query(cls.user_id == user_id).order(cls.criacao).fetch(1000)

class DespesaFixa(Despesa):
    numero_parcelas = ndb.IntegerProperty(required=True)
    dia_vencimento = ndb.IntegerProperty(required=True)

    @classmethod
    def criar(cls, **kwargs):
        kwargs['valor'] = float(kwargs['valor']) 
        kwargs['numero_parcelas'] = int(kwargs['numero_parcelas']) 
        kwargs['dia_vencimento'] = int(kwargs['dia_vencimento']) 

        d = cls(**kwargs)
        d.put()
        return d

class DespesaRecorrente(Despesa):
    dia_vencimento = ndb.IntegerProperty(required=True)

    @classmethod
    def criar(cls, **kwargs):
        kwargs['valor'] = float(kwargs['valor'])
        kwargs['dia_vencimento'] = int(kwargs['dia_vencimento']) 
        d = cls(**kwargs)
        d.put()
        return d    