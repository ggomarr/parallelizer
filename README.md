# parallelizer
The function facilitates parallelizing tasks over multiple cores using the module multiprocessing. It sets up and launches the multiprocessing pool, starts the timer, reports the progress, and finally returns a list with the concatenated output of applying a function to the target list. If too long time goes by without making any progress, the function logs a warning, terminates the pool, and returns whatever output was collected until the multiprocessing pool got stuck.

The function requires the tiny_timer class, which it uses to log the progress of the pool. The class can be found in the tiny_timer repository, and needs to be made available for the parallelizer to import. Adding the code that defines the tiny_timer class manually would also work.

The parallelizer is called with the following arguments:
- func: the function to be applied
- lst: the list of items to apply the function to
- args=(): any additional args for the function. This should be a tuple; if there is only one, it should look like this (lonely_arg,) and not (lonely_arg)
- cores=2\*multiprocessing.cpu_count(): number of threads to launch
- timer_step=300: how often to report progress, in seconds
- max_time_stuck=900: how long to wait without progress until the execution is terminated, in seconds
- Any additional kwargs for the function

The function to be parallelized needs to be defined in the same file where the parallelizer lives (a multiprocessing requirement, me thinks). A wrapper function is available not to have to change this file when launching it from a different place.

The function to be applied needs to return something in order for the pool to know that it is done (either successfully or not). The recommendation is to wrap the function into the following pseudo-structure (meaning, making sure that it always returns a value that can be added to the output list and counted):
```
def my_func(*args,**kwargs):
  try:
    output=do_my_thing(*args,**kwargs)
    if output!=None:
      return output
    else:
      return True
  except:
    log_an_error(error)
    return False
```
Running the file directly from the command line will launch a few simulated parallelizer runs, each of which unfolds into several sleep threads. The last job in each batch will take long enough to trigger the forced termination of the pool. Each simulation uses a slightly different syntax to pass the function and the addtional arguments:
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
The log of this last example would be the following:
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
The output would just be a list containing one ```True``` for each of the 5 completed tasks:
```
[True, True, True, True, True]
```
Enjoy, and let me know if you find it useful!
