/* 
 *Author : Anenth
 */
$("#settings").find("input").on("change",function(){
    checkbox = $(this);
    checked_flag = checkbox.attr("checked") == "checked"
    if(checkbox.attr("id") == "allGraph"){
        if(checked_flag){
            //all the graph visible
        }else{
            // toggle
        }
    }else{
        if(checked_flag){
            //news
        }else{
            // toggle
        }
    }
});
var flag = 0;

var stockChart = $("#stockChart");
var linearRegration = $("#linearRegration");
var bayesianAnalysis = $("#bayesianAnalysis");
var graph = $("#graph_show");    
var home = $("#home");
    
////***chart     
//google.load('visualization', '1.0', {
//    'packages':['corechart']
//});
//google.setOnLoadCallback(drawChart);
//user_settings = $("#user-settings");
var stock_data = [];
var linearReg_data =[];
var bayesian_data =[];
var data_store;
function drawChart(table) {
    if(flag == 0){
      graph.css("visibility","visible");
      home.hide();
    }else{flag++;}
    
    get_data(0);
    get_data(1);
    // draw(2);
    
    
    function get_data(tab_val){
    	 data_store=$.ajax({
            url: "report",
            data:{
                table:table,
                tab:tab_val
            },
            dataType:"json",
            async: false
        }).responseText;
    	thearray = [];
    	data = JSON.parse(data_store)
    	for(i in data){
    		thearray.push({
    			date: new Date(data[i].data.replace(/-/g,',')),
    			value: data[i].val
    			});
    		}
    	
       if(tab_val == 0)
    	   stock_data = thearray;
       else if(tab_val == 1)
    	   linearReg_data = thearray;
       else
    	   bayesian_data = thearray;
    }

    createStockChart();
}


function createStockChart() {
    var chart = new AmCharts.AmStockChart();
    chart.pathToImages = "./static/img/";

    // DATASETS //////////////////////////////////////////
    // create data sets first
    var dataSet1 = new AmCharts.DataSet();
    dataSet1.title = "Stock Chart";
    dataSet1.fieldMappings = [{
        fromField: "value",
        toField: "value"},
    {
        fromField: "volume",
        toField: "volume"}];
    dataSet1.dataProvider = stock_data;
    dataSet1.categoryField = "date";

    var dataSet2 = new AmCharts.DataSet();
    dataSet2.title = "Linear Regression";
    dataSet2.fieldMappings = [{
        fromField: "value",
        toField: "value"},
    {
        fromField: "volume",
        toField: "volume"}];
    dataSet2.dataProvider = linearReg_data;
    dataSet2.categoryField = "date";

    var dataSet3 = new AmCharts.DataSet();
    dataSet3.title = "Bayesian Analysis";
    dataSet3.fieldMappings = [{
        fromField: "value",
        toField: "value"},
    {
        fromField: "volume",
        toField: "volume"}];
    dataSet3.dataProvider = bayesian_data;
    dataSet3.categoryField = "date";

 
    // set data sets to the chart
    chart.dataSets = [dataSet1, dataSet2, dataSet3];
    chart.mainDataSet = dataSet1;

    // PANELS ///////////////////////////////////////////                                                  
    // first stock panel
    var stockPanel1 = new AmCharts.StockPanel();
    stockPanel1.showCategoryAxis = false;
    stockPanel1.title = "Value";
    stockPanel1.percentHeight = 60;

    // graph of first stock panel
    var graph1 = new AmCharts.StockGraph();
    graph1.valueField = "value";
    graph1.comparable = true;
    graph1.compareField = "value";
    stockPanel1.addStockGraph(graph1);

    // create stock legend                
    stockPanel1.stockLegend = new AmCharts.StockLegend();


    // set panels to the chart
    chart.panels = [stockPanel1];


    // OTHER SETTINGS ////////////////////////////////////
    var sbsettings = new AmCharts.ChartScrollbarSettings();
    sbsettings.graph = graph1;
    sbsettings.usePeriod = "WW";
    chart.chartScrollbarSettings = sbsettings;


    // PERIOD SELECTOR ///////////////////////////////////
    var periodSelector = new AmCharts.PeriodSelector();
    periodSelector.position = "left";
    periodSelector.periods = [{
        period: "DD",
        count: 10,
        label: "10 days"},
    {
        period: "MM",
        selected: true,
        count: 1,
        label: "1 month"},
    {
        period: "YYYY",
        count: 1,
        label: "1 year"},
    {
        period: "YTD",
        label: "YTD"},
    {
        period: "MAX",
        label: "MAX"}];
    chart.periodSelector = periodSelector;


    // DATA SET SELECTOR
    var dataSetSelector = new AmCharts.DataSetSelector();
    dataSetSelector.position = "left";
    chart.dataSetSelector = dataSetSelector;

    chart.write('chartdiv');
}

