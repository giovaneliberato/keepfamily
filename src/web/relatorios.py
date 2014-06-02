import json
from models import Despesa, CATEGORIAS_DEFAULT, STATUS

def index(_write_tmpl, _logged_user):
    despesas = Despesa.buscar_por_usuario(_logged_user().key.id(), incluir_arquivadas=True)
    despesas = [d.to_dict_json() for d in despesas]

    values = {
        'despesas': json.dumps(despesas),
        'page': 'relatorios',
        'categorias': json.dumps(CATEGORIAS_DEFAULT),
        'status': json.dumps([s.title() for s in STATUS])
    }
    _write_tmpl('relatorios.html', values)