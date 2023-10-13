To run code, use the following command:
```
python roundtriproadtrip.py
```
The program will then prompt you for the starting location, location file, edge file, maximum time, speed, and output file. 

For our test runs, we tested some cases where we should definitely be returning no solution (e.g. having speed = 1, max time = 98 should return no solution because nothing is within 100 miles round trip from any other point). Our solutions did not monitonically decrease strictly between each solution, but generally it seemed to decrease, and it would always lead to solutions that met the hard time constraint. We utilized a heap to be able to quickly find the next best solution.