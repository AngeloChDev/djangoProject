var treeData = [
      { name: "Torneo", children: [
            { name: "Squadra A", children: [
                  { name: "Giocatore 1" },
                  { name: "Giocatore 2" }
            ]},
            { name: "Squadra B", children: [
                  { name: "Giocatore 3" },
                  { name: "Giocatore 4" }
            ]}
      ]}
];

var margin = { top: 20, right: 90, bottom: 30, left: 90 },
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("#tree")
  .append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var treemap = d3.tree().size([height, width]);

var nodes = d3.hierarchy(treeData[0], function(d) { return d.children; });
nodes = treemap(nodes);

var link = svg.selectAll(".link")
  .data(nodes.descendants().slice(1))
  .enter().append("path")
    .attr("class", "link")
    .attr("d", function(d) {
      return "M" + d.y + "," + d.x
        + "C" + (d.y + d.parent.y) / 2 + "," + d.x
        + " " + (d.y + d.parent.y) / 2 + "," + d.parent.x
        + " " + d.parent.y + "," + d.parent.x;
    });

var node = svg.selectAll(".node")
  .data(nodes.descendants())
  .enter().append("g")
    .attr("class", function(d) { return "node" + (d.children ? " node--internal" : " node--leaf"); })
    .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

node.append("circle")
  .attr("r", 10);

node.append("text")
  .attr("dy", ".35em")
  .attr("x", function(d) { return d.children ? -13 : 13; })
  .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
  .text(function(d) { return d.data.name; });