
try:
    xrange
except NameError:
    xrange = range

class Fibonacci(object):

    def __init__(self):
        self._results = [0, 1]

    def __compute(self, n):
        for i in xrange(len(self._results), n+1):
            self._results.append(self._results[i-1] + self._results[i-2])

    def sequence(self, start_idx, end_idx):
        self.__compute(end_idx)
        return self._results[start_idx:end_idx+1]

if __name__ == '__main__': 
  from time import time

  def timeit(foo):
    def func():
      start = time()
      foo()
      end = time()
      t = (end - start) * 1000
      print ("execution in ms: {}".format(t))
    return func
  
  @timeit
  def cached():
    fib = Fibonacci()
    fib.sequence(1, 10000)
    fib.sequence(1, 10001)

  @timeit
  def not_cached():
    fib = Fibonacci()
    fib.sequence(1, 10000)
    # we remove the cached values
    fib._results = [0, 1]
    fib.sequence(1, 10001)

  print("with cache")
  cached()
  print("without cache")
  not_cached()