# How you can read graphs:

## 1. Theory

![graph](https://github.com/george0st/qgate-graph/blob/main/assets/sample00.png?raw=true)

### 1.1 The main graph (performance/througput per second)
 - The graph with red label 1.
 - The axe Y, amount of calls per second
 - The axe X, amount of executors (= amount of processes * amount of threads)
 - Different curves specify amount of processes, typically
   - one process with e.g. 1, 2, 3, 4, 8, 16, 32 threads (executors 1, 2, 3, 4,
     8, 16, 32)
   - two processes with e.g. 1, 2, 4, 8, 16, 32 threads (executors 2, 4, 8, 16,
     32, 64)
   - three processes with e.g. 1, 2, 4, 8, 16 threads (executors 3, 6, 12, 24,
     48, 96)
 - You can see in graph performance/throughput for specific amount of 
   executors (combination of processes * threads)  
   
### 1.2 The small graphs (response time in milliseconds)
 - The graphs with red label 2., 3. and 4.
 - The axe Y, response time in milliseconds
 - The axe X, amount of executors for specific amount of process(three charts, one process, two processes and three processes)
 - You can see response time for specific amount of executors, each graph is for specific amount of process (1, 2, 3).

You can typically see different throughput in case of different amount of 
process with relation to response time. In case of system overloading, 
the throughput go down and the response time is growing.

## 2. Practical explanation

![graph](https://github.com/george0st/qgate-graph/blob/main/assets/sample01.png?raw=true)

You can see in the main graph the throughput per second for three different
curves with one (green curve), two (purple curve) and three (red curve)
processes.

About one process (green curve):
 - The throughput for one process 
   - go linear up till 4 threads/executors and max value is 130.4 calls/second
   - the growing is stopping in case of 4 threads/executors and the 
     throughput remained the same in case of add other threads 8, 16 and 32
 - The response time is relatively small till 4 threads and dramatically 
   grows in case of more than 4 threads, 8 threads have response time 61.4 ms, 
   16 threads have value 124 ms and 32 threads have value 251.5 ms
 - Summary
   - The testing code can reach for one process maximal throughput
     130.3 calls/sec for 4 threads

About two process (purple curve):
 - The throughput for two process (2 processes with 1, 2, 3, 4, 8, 16, 32 threads)
   - go linear up till 8 executors and max value is 230.28 calls/sec
   - the growing is stopping in case of 8 executors and the 
     throughput remained the similar in case of add other executors 16, 32 and 64
 - The response time is relatively small till 8 executors and dramatically 
   grows in case of more than 8 executors, 16 executors have response time
   69.5 ms, 32 executors have value 139.9 ms and 64 executirs have 
   value 288.8 ms
 - The summary
   - The testing code can reach for two processes maximal throughput
     230.28 calls/sec for 8 executors
   - In case of compare performance between one and two processes, the
     throughput grow +76.6% (from value 130.4 calls/sec to 230.28 calls/sec)

About three process (red curve):
 - The throughput for three process (3 processes with 1, 2, 3, 4, 8, 16, 32 threads)
   - the curve seems very similar as for two processes and the maximal
     throughput value is 233.98 calls/sec
   - it is possible to see the performance go down in higher amount of
     executors (the curve go down) and the response time growing, see 
     96 executors have response time 440.5 ms 
 - The summary
   - The testing code in case to three processes does not improve
     performance and you can see system overloading, it means lower
     performance in case of more executors together with growing 
     response time till value 440.5 ms for 96 executors

Total summary for testing code
 - It makes sense to scale the code till two processes (each with 4 threads),
   higher value for amount of processes/threads does not bring more
   efficiency, only consume more sources
 - You can predicate systems crash based on the reaching the response time
   or based on catching free RAM 
