var temp = {
  x: [],
  y: [],
  mode: 'lines+markers',
  line: {
    color: '#4286f4',
    shape: 'spline'
  },
  name: 'Temperature',
  marker: {
    color: '#4286f4',
    size: 12,
    line: {
      color: 'white',
      width: 0.5
    }
  }
}

var ph = {
  x: [],
  y: [],
  xaxis: 'x2',
  yaxis: 'y2',
  mode: 'lines+markers',
  line: {color: '#DF56F1'},
  name: 'pH',
  marker: {
    color: '#DF56F1',
    size: 12,
    line: {
      color: 'white',
      width: 0.5
    }
  }
};

var layout = {
  xaxis: {
    type: 'date', 
    domain: [0, 1],

  },
  yaxis: {domain: [0.6,1]},
  xaxis2: {
    type: 'date', 
    anchor: 'y2', 
    domain: [0, 1]
  },
  yaxis2: {
    anchor: 'x2', 
    domain: [0, 0.4]},  
}

var data = [temp,ph]; 


Plotly.plot(document.getElementById('chart'),data, layout);
            
var cnt = 0;
function updateGraph(data,indicator){
			
	var time = new Date();
	if(indicator){
		document.getElementById('ph').innerText = JSON.stringify(data, null, 3);
		var update = {
			x:  [[],[time]],
			y: [[],[data]]
		}
	} else {
		document.getElementById('temp').innerText = JSON.stringify(data, null, 3);
		var update = {
			x:  [[time],[]],
			y: [[data],[]]
		}
	}
  
    Plotly.extendTraces(document.getElementById('chart'),update, [0,1]);
    cnt++;
    if(cnt > 500) {
		Plotly.relayout('chart',{
			xaxis: {
				range: [cnt-500,cnt]
			}
		});
    }
};


(function() {
	//init firebase
	const config = {
	apiKey: "AIzaSyAhALzFEglHgmSDc4X-LsVanKZiVWnx-bs",
	authDomain:  "biolumenreactor.firebaseapp.com",
	databaseURL: "https://biolumenreactor.firebaseio.com/",
	storageBucket: "biolumenreactor.appspot.com"
		};
	firebase.initializeApp(config);
	
	const tempObject = document.getElementById('temp');
	const phObject = document.getElementById('ph');
	const hoursObject = document.getElementById('hours');
	const tensminObject = document.getElementById('min');
	const onesminObject = document.getElementById('seconds');
	const runningObject = document.getElementById('running');
	
	const dbtempObject = firebase.database().ref().child('temp');
	const dbphObject = firebase.database().ref().child('ph');
	const dbHoursObject = firebase.database().ref().child('hours');
	const dbTensMinObject = firebase.database().ref().child('min');
	const dbOnesMinObject = firebase.database().ref().child('seconds');
	const dbRunningObject = firebase.database().ref().child('running');
	
	dbtempObject.on('value', snap => 
		updateGraph(snap.val(),0)
	);
	
	dbphObject.on('value', snap => 
		updateGraph(snap.val(),1)
	);
	
	dbHoursObject.on('value', snap => 
		hoursObject.innerText = JSON.stringify(snap.val(), null, 3)
	);
	
	dbTensMinObject.on('value', snap => 
		tensminObject.innerText = JSON.stringify(snap.val(), null, 3)
	);
	
	dbOnesMinObject.on('value', snap => 
		onesminObject.innerText = JSON.stringify(snap.val(), null, 3)
	);

	dbRunningObject.on('value', snap => 
		runningObject.innerText = snap.val()
	);

	if (runningObject.innerText =="Not Running"){
		reset()
	}

}());


// Loading bar
(function ($) {
  var
    $cont = $('#prog'),
    $bar  = $cont.find('.progress'),
    value = 0,
    time  = 288;
    
  function reset() {
    value = 0;
    $cont.removeClass('done');
    $bar.css('height', '0%').text('0');
    $bar.css('backgroundColor', '#114BAF').text('0');
    setTimeout(increment, 500);
  }
  
  function set(num) {
   
    $bar.css('height', num + '%').text(num);
    
    if (value === 100) {
	  $bar.css('backgroundColor', '#11AF19');
      $cont.addClass('done');
      return;
    }
  }
  $bar.css('backgroundColor', '#114BAF').text('0');
  reset();
  
}(this.jQuery));