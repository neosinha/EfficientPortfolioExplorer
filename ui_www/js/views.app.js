// file holds the code which designs the UI views
// or bigger/composite UI view elements
ui = new Bootstrap();

function appNavBar() {
	navbar = ui.navbar("navarea", 'Portfolio Optimizer');
	ui.addSubViewToMain([navbar]);
}

function loadPanels() {
	var px = new Array(); 
	var h3 = ui.h3('id1', 'Good header');
	var b = ui.button('id2', 'Click Me', 'clicker();');
	
	px.push({'type': 'default', 'heading': 'Panel1', 'content': b });
	px.push({'type': 'default', 'heading': 'Panel2', 'content': h3 });
	
	var panel = ui.createPanels('uipanel', px);

	return panel;
}

function clicker() {
	alert('Clicked..');
}


function registerForm() {
	
	inpx = new Array();
	inpx.push({'label' : "User Name", 
			'type' : "text", 
			'name' : 'rusername',
			'id'   : 'rusername',
			'placeholder': "User Name"});
	
	inpx.push({'label' : "Password", 
		'type' : "password", 
		'name' : 'rpasswordx',
		'id'   : 'rpasswordx',
		'placeholder': "Password"}); 
	
	inpx.push({'label' : "Confirm Password", 
		'type' : "password", 
		'name' : 'cpasswordx',
		'id'   : 'cpasswordx',
		'placeholder': "Confirm Password"}); 
	
	inpx.push({'label' : null, 
		'type' : "submit", 
		'name' : 'Register',
		'value': 'Register', 
		'class': 'btn-info', 
		'onclick': 'register();', //call a function to perform registeration
		'placeholder': "Register"});
		
	var form1 = ui.createForm('registerform', inpx);
	
	return form1
}




function loginForm() {

	var inpx = new Array();
	inpx.push({'label' : "User Name", 
			'type' : "text", 
			'id'	: 'usernamex',
			'name' : 'usernamex',
			'placeholder': "User Name Please"});

	inpx.push({'label' : "Last Name", 
			'type' : "text", 
			'id'	: 'lusernamex',
			'name' : 'lusernamex',
			'placeholder': "Last User Name Please"});

	
	inpx.push({'label' : "Password", 
		'type' : "password", 
		'name' : 'passwordx',
		'id' : 'passwordx',
		'placeholder': "Password"}); 
	
	inpx.push({'label' : null, 
		'type' : "submit", 
		'name' : 'Login',
		'value': 'Login', 
		'class': 'btn-info',
		'onclick' : 'authenticate();',
		'placeholder': "Login"});
		
	var form1 = ui.createForm('loginform', inpx);
	
	return form1; 
}


function authenticate() {
	alert( 'Authenticate button was clicked' );
}




function loginView() {
	var h1x = ui.h3(null, '', null);
	jum = ui.jumbotron('view1', h1x);
	
	
	tabs = new Array();
	tabs.push({'name' : "Login" , 'content' : designLoginForm()});
	tabs.push({'name' : "Register" , 'content' : registerForm()});
	navtabs= ui.navtabs('tabbed', 'justified', tabs);
	
	notifyarea = ui.createElement('div', 'notify');
	
	jum.appendChild(navtabs);
	jum.appendChild(notifyarea);
	
	
	//loginview = ui.addSubView(jum, navtabs);
	
	//showView([navbar, jum]);
	//view = ui.addSubViewById('mcontent', [loginview]);
	ui.addSubViewToMain([jum]);
}


function tickerInput() {
    var  inpx = new Array();
    inpx.push({'label' : "TICKERS",
    			'type' : "text",
    			'id'	: 'tickers',
    			'name' : 'tickers',
    			'append' : {'label' : 'Analyze', 'onclick' : 'readTickers();'},
    			'placeholder': "Portfolio STOCK Tickers (Eg: SPY)"});

    var form1 = ui.createForm('loginform', inpx);

   return form1;

}


