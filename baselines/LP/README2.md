# usage
`python main.py hmn -g sample_edge.csv -l sample_label.csv -o sample.output`

***
using hmn in LP, simply use the edges and labels in csv files
***

## input
> sample_edge.csv<br>
> first two columns are: node_from --> node_to的一条边<br>

> sample_label.csv<br> 
> first column is the labels

## output
> 4 columns in sample.output<br>
> Node Id, Predicted label ID, Prob 0, Prob 1<br>
