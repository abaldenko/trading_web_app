
// D3
// d3.csv("static/org_pairs.csv", function(error,d){
	
// 	//init search box
	
// });




 
// density
function norm_pdf(x, mu, sigma){
  return Math.exp(-Math.pow((x-mu),2)/(2*Math.pow(sigma,2)))/(sigma*Math.sqrt(2*Math.PI));
}


var mu = 0, sigma = 1


function generate_dist(mu, sigma){
	labels=[]
	series=[]
	xmin = mu - 3*sigma
	xmax = mu + 3*sigma
	for (var i = 0; i <= 10; i += 1) {
			x_raw = xmin + (6*sigma/10)*i
			x = Math.round(x_raw*100)/100
	        labels.push(x)
	        series.push(norm_pdf(x,mu,sigma)); 
	    }

	norm = {labels: labels, series: [series]}
	return(norm)
}

var df, symbols

console.log("HI")
	


document.addEventListener('DOMContentLoaded',function(){
	
	// search box
	d3.json('/get_symbols', function(d){
		symbols = d
		
		$("#search").select2({
			data: symbols,
			minimumInputLength: 2
		});

	})

	//attach search box listener
	$("#search").on("select2-selecting", function(e) {
		// console.log(e.choice.text)
		$.ajax({
		    type : "POST",
		    url : "/parameter_estimates",
		    data: JSON.stringify(e.choice.text),
		    contentType: 'application/json;charset=UTF-8',
		    success: function(d) {
		    	d = JSON.parse(d)
				mean = d.mean
				std = d.std
				norm = generate_dist(mean,std)
				new Chartist.Line('.distribution-chart', norm);
		    }
		});
	})
})

 