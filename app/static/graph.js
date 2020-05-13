function doGraph(mode_id,word,threshold){

var canvas = document.querySelector("canvas"),
context = canvas.getContext("2d"),
width = canvas.width,
height = canvas.height;
context.clearRect(0, 0, width, height);
context.font = "30px Verdana";
context.fillStyle = "#333";
context.fillText('loading...', width/2,height/2);

context.font = "13px Verdana";
var simulation = d3.forceSimulation()
.force("link", d3.forceLink().id(function(d) { return d.id; }))
.force("charge", d3.forceManyBody())
.force("center", d3.forceCenter(width / 2, height / 2));

d3.json("/graph_data/"+mode_id+"/"+word+"/"+threshold, function(error, graph) {
if (error) throw error;

console.log("/graph_data/"+mode_id+"/"+word+"/"+threshold);
console.log(graph);

simulation
  .nodes(graph.nodes)
  .on("tick", ticked);

simulation.force("link")
  .links(graph.links);

d3.select(canvas)
  .call(d3.drag()
      .container(canvas)
      .subject(dragsubject)
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

function ticked() {
context.clearRect(0, 0, width, height);

context.beginPath();
graph.links.forEach(drawLink);
context.strokeStyle = "#aaa";
context.stroke();


graph.nodes.forEach(drawNode);


}

function dragsubject() {
return simulation.find(d3.event.x, d3.event.y);
}
});

function dragstarted() {
if (!d3.event.active) simulation.alphaTarget(0.3).restart();
d3.event.subject.fx = d3.event.subject.x;
d3.event.subject.fy = d3.event.subject.y;
}

function dragged() {
d3.event.subject.fx = d3.event.x;
d3.event.subject.fy = d3.event.y;
}

function dragended() {
if (!d3.event.active) simulation.alphaTarget(0);
d3.event.subject.fx = null;
d3.event.subject.fy = null;
}

function drawLink(d) {
context.moveTo(d.source.x, d.source.y);
context.lineTo(d.target.x, d.target.y);
}

function drawNode(d) {
    context.beginPath();
    r = (3 - d.level)*2;
    context.moveTo(d.x + r, d.y);
    context.arc(d.x, d.y, r, 0, 2 * Math.PI);
    
    context.fillStyle = "#333";
    context.fillText(d.id, d.x, d.y);

    if(d.level==0){
        color = "#007bff";
    }
    else if(d.level==1){
        color = "#28a745";
    }
    else{
        color = "#dc3545";
    }
    context.strokeStyle = color;
    context.fillStyle = color;
    context.fill();
    context.stroke();
}
}