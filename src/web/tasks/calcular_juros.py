from datetime import datetime
from google.appengine.ext import ndb
from models import Despesa


def index():
    despesas = Despesa.query().fetch()
    now = datetime.now()
    for despesa in despesas:
        dias_vencidos = (now - datetime(year=now.year, month=despesa.data_vencimento[0],
                         day=despesa.data_vencimento[1])).days
        if dias_vencidos and despesa.juros:
            despesa.valor_corrigido = despesa.valor * ((1 + despesa.juros) * dias_vencidos)
            despesa.status = "ATRASADA"

    ndb.put_multi(despesas)