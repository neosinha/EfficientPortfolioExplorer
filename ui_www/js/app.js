
var loginstatus = 1 ; 

var views = new Views();
var websx = new WebServices();
var appmodel = {};
appmodel['tickers'] = null;

function appInit() {
	var varx = "Example 2 View1"; 
	appNavBar();
	loadLandingView(varx);
    initInputTags();

}


function loadLandingView( varx ) {
		var h1x = ui.h3('h3id', varx , null);

		var jum = ui.jumbotron('view1', 'Portfolio' ,' bg-basic');
		
		//<input name="tags" placeholder="write some tags" value="predefined tags here">
		//var tickinp = ui.createElement('input', 'tickers');
		//tickinp.setAttribute('name', 'tickers');
		//tickinp.setAttribute('placeholder', 'Enter a stock Tickers (SPY) and then hit enter');

        var tickinp = tickerInput();

		//create tab area
        var rarea = ui.createElement('div', 'resultarea');
		
		var notifyarea = ui.createElement('div', 'notify');

		jum.appendChild(tickinp);
        jum.appendChild(rarea);

		//jum.appendChild(navtabs);
		jum.appendChild(notifyarea);
		
		
		ui.addSubViewToMain([jum]);
	}


function loginRegisterPage() {
	var h1x = ui.h3('h3id', 'Login Failed'  , null);
	ui.addSubViewToMain([h1x]);

}



function initInputTags() {
    $('[name=tickers]').tagify();
    //var input = document.querySelector('input[name=tags]'),
    //tagify = new Tagify( input );

}


function readTickers() {
    var itickers = document.getElementById('tickers').value;
    //console.log('Tickers: '+ tickers);
    var tickers = new Array();
    for (i=0; i < itickers.length; i++) {
        tickers.push(itickers[i]['value']);
    }
    var stardate = document.getElementById('startingdate').value;
    console.log(stardate);
    appmodel['tickers'] = tickers;

    websx.sendtickers(tickers, startingdate);

}




