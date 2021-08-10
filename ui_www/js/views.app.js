// file holds the code which designs the UI views
// or bigger/composite UI view elements
var ui = new Bootstrap();


var Views = function () {

     this.showProg = function() {
         var prog = document.getElementById('progbody');
         //<img src="img/prog-linear.gif" class="img-rounded imcenter" >
         var img = document.createElement('img');
         img.setAttribute('src', 'img/stock-animate.gif');
         img.setAttribute('class', 'img-rounded imcenter');

        prog.innerHTML = '';
        prog.appendChild(img);

        $("#progress").modal("show");
     };

    this.hideProg = function() {
         var prog = document.getElementById('progress');
         $("#progress").modal("hide");
    };

    //Response from Ticker Table
    this.loadtickertable = function(msg) {
        console.log('Ticker Table: '+msg);
        var robj = JSON.parse(msg);

        $("#progress").modal("hide");;

        var assetimage = ui.createElement('img', 'assetperf');
        assetimage.setAttribute('src', 'images/assetperformance/'+robj['asset']);
        assetimage.setAttribute('class', "img-responsive" );

        var corelimage = ui.createElement('img', 'correlation');
        corelimage.setAttribute('src', 'images/assetperformance/'+robj['covariancetable']['correlation']);
        corelimage.setAttribute('class', "img-responsive" );

        var exlicon = ui.createElement('img', 'excelicon');
        exlicon.setAttribute('onclick', 'window.open(\'images/assetperformance/'+robj['covariancetable']['msexcel']+'\');');
        exlicon.setAttribute('class', "img-responsive pull-right" );
        exlicon.setAttribute('src', 'img/excel-icon-48px.png');

        var ricon = document.getElementById('xlarea-col1');
        ricon.innerHTML = '';
        ricon.appendChild(exlicon);


        var tabs = new Array();
        tabs.push({'name' : "Adjusted Close" , 'content' : ''});
        //tabs.push({'name' : "CoRelation" ,'content' : registerForm()});
        //tabs.push({'name' : "Portfolio" ,'content' : loadPanels()});

        //var navtabs= ui.navtabs('tabbed', 'justified bg-basic text-warning', tabs);
        var rarea = document.getElementById('resultarea-col0');
        rarea.innerHTML = '';
        rarea.appendChild(ui.br());
        rarea.appendChild(assetimage);

         var rarea = document.getElementById('resultarea-col1');
        rarea.innerHTML = '';
        rarea.appendChild(ui.hr());
        rarea.appendChild(corelimage);


        /*rarea.appendChild(ui.br());
        rarea.appendChild(assetimage);
        rarea.appendChild(ui.br());
        rarea.appendChild(corelimage);
        */
    };

    this.initView = function() {

    };


 }


function appNavBar() {
	navbar = ui.navbar("navarea", 'Portfolio Optimizer');
	ui.addSubViewToMain([navbar]);
}


function tickerInput() {
    var  inpx = new Array();

    var todayDate = new Date();
    var yy = todayDate.getFullYear()-2;
    var mm = todayDate.getMonth();
    var dd = todayDate.getDay();
    var today = yy +'-'+mm+'-'+dd;
    console.log('Today: '+ today);

    inpx.push({'label' : "Starting Date",
        		'type' : "date",
        		'name' : 'startingdate',
        		'id' : 'startingdate',
        		'value' : today,
        		'placeholder': "Date"});



    inpx.push({'label' : "TICKERS",
    			'type' : "text",
    			'id'	: 'tickers',
    			'name' : 'tickers',
    			'append' : {'label' : 'Analyze', 'onclick' : 'readTickers();'},
    			'placeholder': "Portfolio STOCK Tickers (Eg: SPY)"});

    var form1 = ui.createForm('loginform', inpx);

   return form1;

}


