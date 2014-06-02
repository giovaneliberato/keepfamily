function RelatoriosCrtl($scope){
    $scope.Math = window.Math;
    $scope.despesas = angular.fromJson(g_despesas);
    $scope.categorias = angular.fromJson(g_categorias).map(function(el){return {label: el, selected: false, cont: 0}});
    $scope.status = angular.fromJson(g_status).map(function(el){return {label: el, selected: false}});
    var cat_count = {}

    var status_cont = {
        'PAGA': 0,
        'ATRASADA': 0,
        'AGUARDANDO': 0
    }

    angular.forEach($scope.categorias, function(c){
        angular.forEach($scope.despesas, function(d){
            if (c.label === d.categoria){
                if (!cat_count[c.label]) cat_count[c.label] = 0;
                cat_count[c.label] = cat_count[c.label] + 1;  
            }  
        })
    })

    var pct = function(valor, total){
        if (!valor || !total)
            return 0;
        return (valor / total) * 100; 
    }

    $scope.config = {
      title: 'Númedo de despesas por categoria',
      tooltips: true,
      labels: false,
      mouseover: function() {},
      mouseout: function() {},
      click: function() {},
      legend: {
        display: true,
        //could be 'left, right'
        position: 'left'
      },
      innerRadius: 0, // applicable on pieCharts, can be a percentage like '50%'
      lineLegend: 'lineEnd' // can be also 'traditional'
    }

    var generate_data = function(){
        var data = []
        angular.forEach(angular.fromJson(g_categorias), function(cat){
            data.push({
                "x": cat,
                "y": [pct(cat_count[cat], $scope.despesas.length), 0, 0],
                "tooltip": cat_count[cat] + "/" + $scope.despesas.length
            })
        })
        return data;
    }

    $scope.data = {
      "series": [],
      "data": generate_data()
    }

    angular.forEach($scope.despesas, function(d){
        status_cont[d.status] = status_cont[d.status] + 1;
    })

    $scope.pagas_cont = pct(status_cont['PAGA'], $scope.despesas.length);
    $scope.aguardando_cont = pct(status_cont['AGUARDANDO'], $scope.despesas.length);
    $scope.atrasadas_cont = pct(status_cont['ATRASADA'], $scope.despesas.length);



    $scope.calcularTotal = function(){
        var total = 0;
        angular.forEach($scope.despesas, function(d){
            total = total + d.valor;
        })
        return total;
    }

    var get_selecteds = function(a){
        return a.filter(function(e){ return e.selected; }).map(function(e){ return e.label.toLowerCase(); })
    }

    $scope.filtrarDespesas = function(d){
        var status_selected = get_selecteds($scope.status);
        var categorias_selected = get_selecteds($scope.categorias);
        
        var filtros_ativos = (status_selected.length || 
                              categorias_selected.length ||
                              $scope.menor_que ||
                              $scope.maior_que);

        if(!filtros_ativos) return true;

        if (status_selected.indexOf(d.status.toLowerCase()) != -1) return true;
        
        if (categorias_selected.indexOf(d.categoria.toLowerCase()) != -1) return true;
        
        if ($scope.menor_que && $scope.maior_que){
            return d.valor < $scope.menor_que && d.valor > $scope.maior_que;
        } else {
            if ($scope.menor_que && d.valor < $scope.menor_que) return true;
            if ($scope.maior_que && d.valor > $scope.maior_que) return true;
        }

        return false;
    }

}