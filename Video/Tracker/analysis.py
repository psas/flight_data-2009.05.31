#!/usr/bin/env python
import matplotlib.pyplot as plt
import scipy.signal as signal

# Read in data and put in list
datafile = open("video_Track.dat",'r')
time      = []
altitude  = []
for line in datafile:
  if line[0] != '#':
    li = line.split(',')
    
    t = float(li[0])
    x = float(li[1])
    y = float(li[2])
    
    time.append(t)
    altitude.append(y)

# Smoothing
def avg(l):
  window = []
  for i in range(l):
    window.append(1/float(l))
  return window

alt_smooth = signal.lfilter(avg(8), [1.0], altitude)

# calculate velocity and acceleration
velocity      = []
acceleration  = []
# prime the pump
velocity.append(0)
acceleration.append(0)
for i in range(1, len(time)):
  t0 = time[i-1]
  t1 = time[i]
  
  x0 = alt_smooth[i-1]
  x1 = alt_smooth[i]
  
  dx = x0 - x1
  dt = t0 - t1
  v  = dx/dt
  velocity.append(v)
  
  v0 = velocity[i-1]
  dv = v0 - v
  a  = dv/dt
  acceleration.append(a)
  
  #print t1, x1, v


vel_smooth = signal.lfilter(avg(10), [1.0], velocity)
acc_smooth  = signal.lfilter(avg(10), [1.0], acceleration)
acc_smooth  = signal.lfilter(avg(10), [1.0], acc_smooth)

# printing
def plot(y, y_label, title, filename):
  fig = plt.figure(figsize=(7, 3.5))
  fig.subplots_adjust(bottom=0.12, top=0.91, left=0.12, right=0.95)
  ax = fig.add_subplot(111)
  ax.plot(time, y, ".-r")
  
  plt.xlabel("Time ($\mathrm{s}$)", fontsize=10)
  plt.ylabel(y_label, fontsize=10)
  plt.title(title, fontsize=12)
  
  for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(8)
  for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(8)

  plt.savefig(filename, dpi=100)

plot(altitude,   r"Altitude ($\mathrm{m}$)", "Video Analysis: Altitude",                                    "alt.png")
plot(velocity,   r"Velocity ($\mathrm{m\cdot\ s^{-1}}$)",    "Video Analysis: Vertical Velocity",           "vel.png")
plot(acc_smooth, r"Altitude ($\mathrm{m\cdot\ s^{-2}}$)", "Video Analysis: Smoothed Vertical Acceleration", "acc.png")
