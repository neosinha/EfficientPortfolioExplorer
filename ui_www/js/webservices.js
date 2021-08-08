var serverLocation = location.host;
var server = "http://" + serverLocation ;
console.log("Location: "+ server);

var movetable = null;


var WebServices = function () {

    this.sendtickers = function(tickerdata, startdate) {
          //var tickerdata = ['AAPL', 'SPY'];
          var datax = {'assets' : tickerdata, 'startdate' : startdate}
          $.ajax( {url : server+'/getstocktable',
                  sync: false,
                  method: "POST",
                  data : {'assetdata': JSON.stringify(datax)},
                  success: views.loadtickertable
                  } );
    }


 }
