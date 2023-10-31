import argparse
import sys
import os
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.patches import Ellipse
import associate

matplotlib.use('Agg')


def plot_traj(ax,stamps,traj,style,color,label):
    """
    Plot a trajectory using matplotlib. 
    
    Input:
    ax -- the plot
    stamps -- time stamps (1xn)
    traj -- trajectory (3xn)
    style -- line style
    color -- line color
    label -- plot legend
    
    """
    stamps.sort()
    interval = numpy.median([s-t for s,t in zip(stamps[1:],stamps[:-1])])
    x = []
    y = []
    last = stamps[0]
    for i in range(len(stamps)):
        if stamps[i]-last < 2*interval:
            x.append(traj[i][0])
            y.append(traj[i][1])
        elif len(x)>0:
            ax.plot(x,y,style,color=color,label=label)
            label=""
            x=[]
            y=[]
        last= stamps[i]
    if len(x)>0:
        ax.plot(x,y,style,color=color,label=label)
            
if __name__=="__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='''
    This script plots the estimated trajectory. 
    ''')
    parser.add_argument('trajectory', help='trajectory output file (format: timestamp tx ty tz qx qy qz qw)')
    args = parser.parse_args()
    # read output and get timestamps
    output_list = associate.read_file_list(args.trajectory, False)
    output_stamps = sorted(output_list.keys())
    #print (output_stamps)
    #output_stamps.sort()
    # get xyz position.
    output_xyz_full = numpy.matrix([[float(value) for value in output_list[b][0:3]] for b in output_stamps]).transpose()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_traj(ax,output_stamps,output_xyz_full.transpose().A,'-',"black", "estimated")
    plt.savefig('output.png')


