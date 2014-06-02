#coding: utf-8

def validar_dados(kwargs):
    kwargs['valor'] = float(kwargs['valor'])
    if kwargs['valor'] < 0:
        raise BaseException("Atributo  Valor invalido: %d" % kwargs['valor'])

    if kwargs['tipo'] == 'AVULSA': return kwargs

    kwargs['juros'] = float(kwargs['juros'])    

    kwargs['dia_vencimento'] = int(kwargs['dia_vencimento'])
    if kwargs['dia_vencimento'] > 31:
        raise BaseException("Atributo Dia de vencimento invalido: %d" % kwargs['dia_vencimento'])

    kwargs['mes_vencimento'] = int(kwargs['mes_vencimento'])
    if kwargs['mes_vencimento'] > 31:
        raise BaseException("Atributo mes de vencimento invalido: %d" % kwargs['mes_vencimento'])

    kwargs['data_vencimento'] = (kwargs.pop('mes_vencimento'), kwargs.pop('dia_vencimento'))

    if kwargs.get('numero_parcelas'): 
        kwargs['numero_parcelas'] = int(kwargs['numero_parcelas'])
        if kwargs['numero_parcelas'] < 0:
            raise BaseException("Atributo Numero de parcelas invalido: %d" % kwargs['numero_parcelas'])

    return kwargs