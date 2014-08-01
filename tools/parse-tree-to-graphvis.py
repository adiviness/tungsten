#!/usr/bin/env python

"""A pathetically simple Python script to convert a simple tree representation
to a dot(1) configuration file.  Keith Hellman <khellman@mines.edu> for 
Spring 2014 Compilers.

On a Linux box with dot(1) installed (typically found in the graphvis package),
invoke like this:

 $ ls
 parsetree.txt
 $ cat parsetree.txt | ./parse-tree-to-graphvis | dot -Tpng -o parsetree.png
 $ display parsetree.png

Input format is in two parts:  node identification and then edge identification.

 $ cat parsetree.txt
 nodeA Node A
 leafB Leaf B
 nodeC Node C
 leafD Leaf D
 leafE Leaf E
 
 nodeA leafB nodeC
 nodeC leafD leafE
 $ 

This would generate a graph:

    Node A
    /    \
 Leaf B  Node C
         /   \
     Leaf C   \
             Leaf D


The input format is line oriented, ignores empty lines, and does not support
comments.
"""

import sys

def nextline( f ) :
    l = f.readline()
    while l : 
        l = l.split()
        if l :
            return l[0], l[1:]
        l = f.readline()
    return ['', []]

def read( f ) :
    nodes = {}
    edges = []

    node, resid = nextline( f )
    while node :
        if node in nodes :
            # node children links
            edges.extend( [ '"%s" -- "%s";' % (node,c) for c in resid ] )
        else :
            # new node
            nodes[node]=" ".join(resid) or node

        node, resid = nextline( f )

    return nodes, edges

def write( f, nodes, edges ) :
    sep="\n  ";
    f.write( "graph Pt {" + sep + "ordering=out;" + sep )
    f.write( sep.join( [ '"%s" [label="%s"];' % x for x in nodes.iteritems() ] ) + sep )
    f.write( sep.join( edges ) + sep )
    f.write( "}\n" );

n, e = read( sys.stdin )
write( sys.stdout, n, e )

