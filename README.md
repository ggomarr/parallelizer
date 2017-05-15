# parallelizer
The function makes using the module multiprocessing easier. It is called with the following arguments:
- func: the function to be applied
- lst: the list of items to apply the function to
- args=(): any additional args for the function. This should be a tuple; if there is only one, it should look like this (lonely_arg,) and not (lonely_arg)
- cores=2\*multiprocessing.cpu_count(): number of cores to use
- timer_step=300: how often to report progress, in seconds
- max_time_stuck=900: how long to wait without progress until the execution is terminated, in seconds
- Any additional kwargs to the function

The function will then set up and launch the multiprocessing pool, start the timer, report the progress, and finall return a list with the output.

The function to be parallelized needs to be defined in the same file where the parallelizer lives (a multiprocessing requirement, me thinks). A wrapper function is available not to have to change this file when launching it from a different place.

The function to be applied needs to return something in order to know that it is done (either successfully or not). The recommendation is to wrap the function into the following pseudo-structure:
```
def my_func(*args,**kwargs):
  try:
    output=do_my_thing(*args,**kwargs)
    if output:
      return output
    else:
      return True
  except:
    log_an_error(error)
    return False
```
Running the file directly from the command line will launch a simulated usage of the parallelizer that will launch sleep orders to the different cores using different syntaxes. The last job will take long enough to trigger the forced termination of the pool.
- Parallelizing the function directly, with no additional arguments
```
out=parallelize(my_sleep,sleep_time_lst,cores=2,timer_step=5,max_time_stuck=10)
```
- Parallelizing the function directly, with additional args
```
out=parallelize(my_sleep,sleep_time_lst,('Args!',),cores=2,timer_step=5,max_time_stuck=10)
```
- Parallelizing the function directly, with additional kwargs
```
out=parallelize(my_sleep,sleep_time_lst,msg='Kwargs!',cores=2,timer_step=5,max_time_stuck=10)
```
- Parallelizing the function through the wrapper, with no additional arguments
```
out=parallelize(function_wrapper,sleep_time_lst,(my_sleep,),cores=2,timer_step=5,max_time_stuck=10)
```
- Parallelizing the function through the wrapper, with additional args
```
out=parallelize(function_wrapper,sleep_time_lst,(my_sleep,'Args!'),cores=2,timer_step=5,max_time_stuck=10)
```
- Parallelizing the function through the wrapper, with additional kwargs
```
out=parallelize(function_wrapper,sleep_time_lst,(my_sleep,),msg='Kwargs!',cores=2,timer_step=5,max_time_stuck=10)
```
The output of this last example would be the following:
```
05/14/2017 07:24:17 PM timer        INFO     0 items processed [0:00:06]. 6 items left [0:00:40]
05/14/2017 07:24:17 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
05/14/2017 07:24:17 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
05/14/2017 07:24:22 PM timer        INFO     2 items processed [0:00:11]. 4 items left [0:00:23]
05/14/2017 07:24:24 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
05/14/2017 07:24:24 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
05/14/2017 07:24:27 PM timer        INFO     4 items processed [0:00:16]. 2 items left [0:00:08]
05/14/2017 07:24:31 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
05/14/2017 07:24:32 PM timer        INFO     5 items processed [0:00:21]. 1 items left [0:00:04]
05/14/2017 07:24:36 PM timer        INFO     5 items processed [0:00:26]. 1 items left [0:00:05]
05/14/2017 07:24:41 PM timer        INFO     5 items processed [0:00:31]. 1 items left [0:00:06]
05/14/2017 07:24:46 PM timer        INFO     5 items processed [0:00:36]. 1 items left [0:00:07]
05/14/2017 07:24:46 PM parallelize  WARNING  Terminating the job pool: 1 out of 6 jobs got stuck!
```
Enjoy, and let me know if you find it useful!
