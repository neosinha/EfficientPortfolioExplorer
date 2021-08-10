
var loginstatus = 1 ; 

var views = new Views();
var websx = new WebServices();
var appmodel = {};
appmodel['tickers'] = null;

function appInit() {
    views.hideProg();
	var varx = "Example 2 View1"; 
	appNavBar();
	loadLandingView(varx);
    initInputTags();

}


function loadLandingView( varx ) {
		var h1x = ui.h3('h3id', varx , null);

		var jum = ui.jumbotron('view1', 'Portfolio' ,' bg-basic');

        var tickinp = tickerInput();
        var tickerwt = ui.createElement('div', 'tweights');

		var row1 = ui.addRowColContent('inputrow', [ {'size': 6, 'content' : tickerInput() },
		                                             {'size': 6, 'content' : tickerwt} ]
		                                 );
		//<input name="tags" placeholder="write some tags" value="predefined tags here">
		//var tickinp = ui.createElement('input', 'tickers');
		//tickinp.setAttribute('name', 'tickers');
		//tickinp.setAttribute('placeholder', 'Enter a stock Tickers (SPY) and then hit enter');



		//create tab area
		var xlarea = ui.addRowCol('xlarea', 2);
        var rarea = ui.addRowCol('resultarea', 2);
		var frontier = ui.addRowCol('frontier', 2);

		var notifyarea = ui.createElement('div', 'notify');


		jum.appendChild(row1);
		//jum.appendChild(tickinp);
		jum.appendChild(ui.hr());
		jum.appendChild(xlarea);

		jum.appendChild(ui.hr());
        jum.appendChild(rarea);
		jum.appendChild(ui.hr());
        jum.appendChild(frontier);


		//jum.appendChild(navtabs);
		jum.appendChild(notifyarea);
		
		
		ui.addSubViewToMain([jum]);


	}


function loginRegisterPage() {
	var h1x = ui.h3('h3id', 'Login Failed'  , null);
	ui.addSubViewToMain([h1x]);

}



function initInputTags() {
    var inpx = $('[name=tickers]').tagify().on('add', appendTags).on('removeTag', removeTags);
    //tagify = new Tagify( input );

}
var tagNum = 0;


function sliderEl (tagName, pos) {
    var inpgrp = ui.createElement('div', 'grp-'+pos);
    inpgrp.setAttribute('class', 'input-group');
    var label = ui.createElement('label', 'label-'+pos);
    label.setAttribute('for', 'weight'+pos);
    label.innerHTML = tagName;



    var sldrel = ui.createElement('input', 'weight'+pos);
    sldrel.setAttribute('type', 'number');
    sldrel.setAttribute('name', 'weight'+pos);
    sldrel.setAttribute('min', '0');
    sldrel.setAttribute('max', '100');


    inpgrp.appendChild(label);
    inpgrp.appendChild(sldrel);

    return inpgrp;
}

var tagArray = new Array();

function appendTags(e, tagName) {
    var tcx = document.getElementById('tickers').value;
    console.log('TagActivity: '+ tcx + '/'+ e.detail + '/'+ JSON.stringify(tagName) );
    var newtag = tagName['tag']['__tagifyTagData']['value'];
    console.log('New Tag: '+ newtag);
    if (newtag.includes('=')) {
        var sldr = document.getElementById('inputrow-col1');
        tagArray.push(newtag);
        console.log('Arr: '+ JSON.stringify(tagArray));
    } else {
        confirm(newtag + '= ? Please enter "=" and a portfolio weight. Eg. SPY=50');
    }

   wtCharts();
}

function removeTags(tagName) {
    var newtag = tagName['tag'];
    var list = document.getElementById('tickers').value;
    console.log('Short List: '+ list);
    //console.dir('Removed: '+ tagName );
    //updateWeightChart();
    wtCharts();
}

function wtCharts() {

    var wChart = document.createElement('canvas', 'weightchart');
    wChart.setAttribute('width', '400');
    wChart.setAttribute('height', '400');

    var chartEl = document.getElementById('inputrow-col1');
    chartEl.innerHTML = '';
    chartEl.appendChild(wChart);

    var valx = document.getElementById('tickers').value;
    console.log("WeightData: "+valx);
    if ((valx != null) && (valx.length > 0)) {
        var weightData = JSON.parse(valx);
        var labels = new Array();
        var data = new Array();
        for (i=0 ; i < weightData.length; i++) {
        }
    }


}

function readTickers() {
    var itickers = JSON.parse(document.getElementById('tickers').value);
    console.log('Tickers: '+ itickers);


    var tickers = new Array();
    for (i=0; i < itickers.length; i++) {
        var tkr = itickers[i]['value'];
        tickers.push(tkr);
    }
    var stardate = document.getElementById('startingdate').value;
    console.log("Startdate: "+stardate + '/Ticker: '+ tickers);
    appmodel['tickers'] = tickers;
    //views.showProg();


    websx.sendtickers(tickers, stardate);

}




