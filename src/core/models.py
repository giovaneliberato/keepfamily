#coding: utf-8
import md5
from google.appengine.ext import ndb
from google.appengine.ext.ndb.polymodel import PolyModel


CATEGORIAS_DEFAULT = [u"Alimentação", u"Animal de estição", u"Casa", u"Educação",
                      u"Filhos", u"Lazer", u"Saúde", u"Veículo", u"Outros"]

STATUS = ['PAGA', 'AGUARDANDO', 'ATRASADA', 'ARQUIVADA']

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
    status = ndb.StringProperty(required=True, choices=STATUS, default='AGUARDANDO')
    data_vencimento = ndb.IntegerProperty(repeated=True)
    juros = ndb.FloatProperty()
    valor_corrigido = ndb.FloatProperty()

    @classmethod
    def buscar_por_usuario(cls, user_id, incluir_arquivadas=False):
        query = cls.query(cls.user_id == user_id)
        if not incluir_arquivadas:
            query = query.filter(cls.status != 'ARQUIVADA') 
        return query.fetch(1000)


    def to_dict_json(self):
        return {
            'nome_produto_servico': self.nome_produto_servico,
            'valor': self.valor_corrigido or self.valor,
            'beneficiario': self.beneficiario,
            'categoria': self.categoria,
            'status': self.status if self.status != "ARQUIVADA" else "PAGA" 
        }

class DespesaFixa(Despesa):
    numero_parcelas = ndb.IntegerProperty(required=True)
    pass

class DespesaRecorrente(Despesa):
    salvar_modelo = ndb.BooleanProperty(default=False)

    @classmethod
    def buscar_modelos(cls, user_id):
        return cls.query(cls.salvar_modelo == True, cls.user_id == user_id).fetch()

class DespesaAvulsa(Despesa):
    pass