//let snack = $("snack").attr('value');
//let desert = $("desert").attr('value');
//let noodles = $("noodles").attr('value');
//let unclassion = $("unclassion").attr('value');
//let room_temperature_hmr = $("room_temperature_hmr").attr('value');
//let household_goods = $("household_goods").attr('value');
//let lee_beauty = $("lee_beauty").attr('value');
//let sauce = $("sauce").attr('value');
//let dairy_product = $("dairy_product").attr('value');
//let beverage = $("beverage").attr('value');
//let coffee = $("coffee").attr('value');
//let canned_snacks = $("canned_snacks").attr('value');
//let home_clean = $("home_clean").attr('value');
//alert(snack)
function display(data){
        Highcharts.chart('container', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: '상품 통계'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: data
        });
    };


function getdata(){
       var data= [{
        name: 'Food category',
        colorByPoint: true,
        data: [{
            name: '과자',
            y: 19.3
        }, {
            name: '디저트',
            y: 0.5
        }, {
            name: '면류',
            y: 4.8
        }, {
            name: '미분류',
            y: 0.03
        }, {
            name: '상온HMR',
            y: 12.4
        }, {
            name: '생활용품',
            y: 5
        }, {
            name: '의약외품',
            y: 7.1
        }, {
            name: '소스',
            y: 13.2
        }, {
            name: '유제품',
            y: 3.9
        }, {
            name: '음료',
            y: 3.9
        }, {
            name: '커피/차',
            y: 4.85
        }, {
            name: '주류',
            y: 4.8
        }, {
            name: '톰조림/안주',
            y: 4.7
        }, {
            name: '홈클린',
            y: 4.5
        }]
    }]
    display(data);
 };

 $(document).ready(function(){
    getdata();
 });