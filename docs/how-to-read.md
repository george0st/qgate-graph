# How you can read graphs

This description aims to teach you how to read these types of graphs
correctly, extract the maximum amount of information, and draw the 
right conclusions based on them.

## 1. Theory

Let's take a look at what each chart actually shows and focus on
this sample chart.

![graph](https://github.com/george0st/qgate-graph/blob/main/assets/sample00.png?raw=true)

### 1.1 Title

The title contains specification of execution details, in this case:
 - 4 wave, HASH, General, 30000 docs
 - 8 CPU, 8 GB RAM
 - Date time
 - others

### 1.2 The main graph (performance/througput per second)
 - The graph with red label 1.
 - The axe Y, amount of calls per second
 - The axe X, amount of executors (= amount of processes * amount of threads)
 - Different curves specify amount of processes, typically
   - one process with e.g. 1, 2, 3, 4, 8, 16, 32 threads (executors 1, 2, 3, 4,
     8, 16, 32)
   - two processes, each with e.g. 1, 2, 3, 4, 8, 16, 32 threads (executors 2, 4, 6, 8, 16,
     32, 64)
   - three processes, each with e.g. 1, 2, 3, 4, 8, 16, 32 threads (executors 3, 6, 9, 12, 24,
     48, 96)
 - You can see in graph performance/throughput for specific amount of 
   executors (multiplication of processes * threads)  
   
### 1.3 The small graphs (response time in milliseconds)
 - The graphs with red label 2., 3. and 4.
 - The axe Y, response time in milliseconds
 - The axe X, amount of executors for specific amount of process 
   (three charts, one process, two processes and three processes)
 - You can see response time for specific amount of executors, 
   each graph is for specific amount of process (1, 2, 3).

You can typically see different throughput in case of different amount of 
processes with relation to response time. In case of system overloading, 
the throughput go down and the response time speedup growing.

## 2. Practical explanation

Let's break down one sample chart.

![graph](https://github.com/george0st/qgate-graph/blob/main/assets/sample01.png?raw=true)

You can see in the main graph the throughput per second for three different
curves with one (green curve), two (purple curve) and three (red curve)
processes. The graph specify details such as HASH, General, 30000 docs and
important information about HW configuration (8 CPU, 8 GB RAM).

NOTE: In case of e.g. more cores, memory, etc. the outputs/graphs can be
different.

### 2.1 About one process (green curve):
 - The throughput for one process 
   - go linear up till 4 threads/executors and max value is 130.4 calls/second
   - the growing is stopping in case of 4 threads/executors and the 
     throughput remained the same in case of add other threads 8, 16 and 32
 - The response time is relatively small till 4 threads and dramatically 
   grows in case of more than 4 threads, 8 threads have response time 61.4 ms, 
   16 threads have value 124 ms and 32 threads have value 251.5 ms
 - **The summary**
   - The testing code can reach for one process maximal throughput
     130.3 calls/sec for 4 threads

### 2.2 About two processes (purple curve):
 - The throughput for two process (2 processes with 1, 2, 3, 4, 8,
   16, 32 threads)
   - go linear up till 8 executors and max value is 230.28 calls/sec
   - the growing is stopping in case of 8 executors and the 
     throughput remained the similar in case of add other executors 16, 32
     and 64
 - The response time is relatively small till 8 executors and dramatically 
   grows in case of more than 8 executors. The 16 executors have response time
   69.5 ms, 32 executors have value 139.9 ms and 64 executors have 
   value 288.8 ms
 - **The summary**
   - The testing code can reach for two processes maximal throughput
     230.28 calls/sec for 8 executors (it means two processes each
     with 4 threads)
   - In case of performance compare between one and two processes, the
     throughput grow +76.6% (from value 130.4 calls/sec to 230.28 calls/sec)

### 2.3 About three processes (red curve):
 - The throughput for three processes (3 processes with 1, 2, 3, 4, 8, 16,
   32 threads)
   - the curve seems very similar as for two processes and the maximal
     throughput value is 233.98 calls/sec
   - it is possible to see, the performance go down in higher amount of
     executors (the curve go down) and the response time growing, see 
     96 executors have response time 440.5 ms and the performance
     is ~220 calls/sec
 - **The summary**
   - The testing code in case to three processes does not improve
     performance, you can see system overloading, it means lower
     performance in case of more executors, together with growing 
     response time till value 440.5 ms for 96 executors

### 2.4 Final summary
 - It makes sense to scale the code till two processes (each with 
   4 threads, it meas 8 executors as total). The higher values for 
   amount of processes/threads does not bring more efficiency, only
   consumes more sources (efficiency go down).
 - NOTE: You can predicate systems crash based on the reaching 
   the limited the response time or based on out of memory error
   (or performance degradation based on disk swapping).

## 3. The conclusion

I hope this description helped you understand these charts better 
and faster. If you have any suggestions for improvement, please 
contact me 'steuer(dot)j(at)seznam(dot)cz'