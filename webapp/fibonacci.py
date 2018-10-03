
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

if __name__ == '__main__': # TODO: add benchmarking for cache
  pass