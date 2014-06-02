function DespesasCtrl($scope){
    $scope.calcularTotal = function(){
        if ($scope.numero_parcelas == undefined || $scope.valor_parcela == undefined)
            return 0;
        return $scope.numero_parcelas * $scope.valor_parcela; 
    }
}