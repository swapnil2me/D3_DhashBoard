var apiURL = "http://127.0.0.1:8001/getData?id=19&nVals=10"

var parseDate = d3.timeParse("%Y-%m-%d,%H:%M:%S");
var times = 500; // gap in Milli Seconds;

function startRefresh() {

  setTimeout(startRefresh,times);

};

d3.json(apiURL).get(function (error, data) {
  //console.log(data);
  var value = data.map(function(d) {return Number(d.value);});
  var time = data.map(function(d) {return parseDate(d.time.split(".")[0].split("T").join());});

  var dataZip = time.map(function(e, i) {
                return [e, value[i]];
              });

  //console.log(dataZip);

  var height = 300;
  var width = 500;

  var max = d3.max(value);
  var min = d3.min(value)
  //console.log(max);
  var minDate = d3.min(time);
  var maxDate = d3.max(time);

  var y = d3.scaleLinear()
            .domain([min, max])
            .range([height, 0]);

  var x = d3.scaleTime()
            .domain([minDate, maxDate])
            .range([0, width]);

  var yAxis = d3.axisLeft(y);
  var xAxis = d3.axisBottom(x);

  var svg = d3.select("body").append("svg").attr("height","100%")
                                           .attr("width","100%");

  var margin = {left:50, right:50, top:40, bottom:0};

  var chartGroup = svg.append("g")
                      .attr("transform","translate("+margin.left+","+margin.top+")");

  var line = d3.line()
                .x(function(d){return x(d[0]);})
                .y(function(d){return y(d[1]);});

  chartGroup.append("path").attr("d",line(dataZip));
  chartGroup.append("g").attr("class", "x axis")
                        .attr("transform","translate(0,"+height+")")
                        .call(xAxis);
  chartGroup.append("g").attr("class", "y axis").call(yAxis);

});
