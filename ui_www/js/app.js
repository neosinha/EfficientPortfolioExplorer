
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
		jum.appendChild(xlarea);
        jum.appendChild(rarea);
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
    var inpx = $('[name=tickers]').tagify();
    inpx.on('add', addTags);

    //tagify = new Tagify( input );

}

function addTags(e) {
    var tcx = document.getElementById('tickers').value;
    console.log('Added: '+ tcx) + '/'+ e.detail;
}

function readTickers() {
    var itickers = JSON.parse(document.getElementById('tickers').value);
    console.log('Tickers: '+ itickers);

    var sldr = document.getElementById('inputrow-col1');
    var tickers = new Array();
    for (i=0; i < itickers.length; i++) {
        var tkr = itickers[i]['value'];
        tickers.push(tkr);

        var sldrel = ui.createElement('input', 'weight'+i);
        sldrel.setAttribute('type', 'number');
        sldrel.setAttribute('name', 'weight'+i);
        sldrel.setAttribute('min', '0');
        sldrel.setAttribute('max', '0');

        sldr.appendChild(sldrel);


    }
    var stardate = document.getElementById('startingdate').value;
    console.log("Startdate: "+stardate + '/Ticker: '+ tickers);
    appmodel['tickers'] = tickers;
    //views.showProg();


    websx.sendtickers(tickers, stardate);

}




