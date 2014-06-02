# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from models import DespesaFixa, DespesaRecorrente, CATEGORIAS_DEFAULT, DespesaAvulsa
from tekton import router


def index(_write_tmpl, _logged_user, errors=""):
    if _logged_user():
        user_id = _logged_user().key.id()
        despesas_fixas = DespesaFixa.buscar_por_usuario(user_id)
        despesas_recorrentes = DespesaRecorrente.buscar_por_usuario(user_id)
        despesas_avulsas = DespesaAvulsa.buscar_por_usuario(user_id)

        values = {
            'page': 'home',
            'despesas_neste_mes': max(len(despesas_fixas), len(despesas_recorrentes) ,len(despesas_avulsas), 0),
            'despesas_fixas': despesas_fixas,
            'despesas_recorrentes': despesas_recorrentes,
            'despesas_avulsas': despesas_avulsas
        }

        _write_tmpl('index.html', values)
    
    else:
        errors = errors.split()
        _write_tmpl('landing.html', {"errors": errors})
