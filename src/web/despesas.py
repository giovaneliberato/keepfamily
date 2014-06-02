#coding: utf-8
import time
import despesas_svc
from models import CATEGORIAS_DEFAULT, Despesa, DespesaFixa, DespesaRecorrente, DespesaAvulsa
from tekton import router


def index(_write_tmpl, _logged_user, aba="fixa", success=''):
    user_id = _logged_user().key.id()
    values = {'page': 'despesas',
              'aba': aba,
              'success': success,
              'categorias': CATEGORIAS_DEFAULT,
              'action_url': router.to_path(cadastrar)}

    if aba == 'recorrente':
        values['modelos'] = DespesaRecorrente.buscar_modelos(user_id)
    
    _write_tmpl('despesas.html', values)


def cadastrar(_handler, _write_tmpl, _logged_user, **kwargs):
    kwargs['user_id'] = _logged_user().key.id()


    try:
        kwargs = despesas_svc.validar_dados(kwargs)
    except BaseException as e:
        _write_tmpl("error.html", {'msg': e.message})
        return

    tipo = kwargs.pop('tipo')
    if tipo == "FIXA":
        DespesaFixa(**kwargs).put()

    elif tipo == "RECORRENTE":
        kwargs['salvar_modelo'] = kwargs['salvar_modelo'] == 'on' 
        DespesaRecorrente(**kwargs).put()

    else:
        DespesaAvulsa(**kwargs).put()
    
    _handler.redirect(router.to_path(index, tipo.lower()) + "?success=true")


def usar_modelo(_write_tmpl, modelo_id):
    modelo = Despesa.get_by_id(long(modelo_id))
    
    aba = 'recorrente'
    nova_despesa = DespesaRecorrente()
    nova_despesa.populate(**modelo.to_dict(exclude=["class_", "salvar_modelo"]))
    nova_despesa.put()
    
    values = {
        'categorias': CATEGORIAS_DEFAULT,
        'despesa': nova_despesa,
        'aba': aba,
        'action_url': router.to_path(completar_edicao, nova_despesa.key.id()),
        'esconder_salvar_modelo': True
    }

    _write_tmpl('despesas.html', values)


def alterar_status(_handler, despesa_id, status):
    d = Despesa.get_by_id(long(despesa_id))
    d.status = status.upper()
    d.put()
    time.sleep(.3)

    if isinstance(d, DespesaFixa):
        tipo = 'fixa'
    elif isinstance(d, DespesaRecorrente):
        tipo = 'recorrente'
    else:
        tipo = 'avulsa'

    _handler.redirect("/#%s" % tipo)


def editar(_write_tmpl, despesa_id):
    d = Despesa.get_by_id(long(despesa_id))
    
    if isinstance(d, DespesaFixa):
        aba = 'fixa'
    elif isinstance(d, DespesaRecorrente):
        aba = 'recorrente'
    else:
        aba = 'avulsa'    
    
    values = {
        'categorias': CATEGORIAS_DEFAULT,
        'despesa': d,
        'aba': aba,
        'editar': True,
        'action_url': router.to_path(completar_edicao, despesa_id)
    }

    _write_tmpl('despesas.html', values)


def completar_edicao(_handler, _write_tmpl, despesa_id, **kwargs):
    despesa = Despesa.get_by_id(long(despesa_id))
    try:
        kwargs = despesas_svc.validar_dados(kwargs)
    except BaseException as e:
        _write_tmpl("error.html", {'msg': e.message})
        return

    tipo = kwargs.pop('tipo')
    despesa.populate(**kwargs)
    despesa.put()
    time.sleep(.3)

    _handler.redirect("/#%s" % tipo.lower())
