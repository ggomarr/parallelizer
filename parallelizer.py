import logging
import time, datetime
import multiprocessing
import tiny_timer

def parallelize(func,lst,args=(),cores=2*multiprocessing.cpu_count(),
                timer_step=300,max_time_stuck=900,log_level=logging.DEBUG,
                **kwargs):
    logger=logging.getLogger('parallelize')
    logger.setLevel(log_level)
    pool=multiprocessing.Pool(processes=cores)
    output=[]
    tot=len(lst)
    timer=tiny_timer.tiny_timer(tot,timer_step=timer_step,max_time_stuck=max_time_stuck)
    for i in lst:
        pool.apply_async(func,(i,)+args,kwargs,callback=output.append)
    pool.close()
    time_stuck=0
    cnt=0
    while cnt<tot:
        seconds_left,very_stuck=timer.check_timer(cnt=cnt)
        if very_stuck:
            logger.warning('Terminating the job pool: {} out of {} jobs got stuck!'.format(tot-cnt,tot))
            pool.terminate()
            break
        time.sleep(min(timer_step,seconds_left))
        cnt=len(output)
    return output

def function_wrapper(x,func,*args,**kwargs):
    try:
        return func(x,*args,**kwargs)
    except:
        return False

if __name__ == '__main__':
    def setup_logger(log_level=logging.DEBUG):
        logger=logging.getLogger()
        formatter=logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s','%m/%d/%Y %I:%M:%S %p')
        handler_stream=logging.StreamHandler()
        handler_stream.setLevel(log_level)
        handler_stream.setFormatter(formatter)
        logger.addHandler(handler_stream)
        return logger
    setup_logger()
    logger=logging.getLogger('sample_run')
    logger.setLevel(logging.DEBUG)
    def my_sleep(t,msg='Hey!',log_level=logging.DEBUG):
        logger=logging.getLogger('my_sleep')
        logger.setLevel(logging.DEBUG)
        try:
            time.sleep(t)
            logger.debug('[{}] Slept for {}s!'.format(msg,t))
            return True
        except:
            return False
    sleep_time_lst=[7,7,7,7,7,100]
    logger.info('Function: my_sleep - sleeps for t, displays msg when done')
    logger.info('List of sleep times: {}'.format(sleep_time_lst))
    logger.info('Progress is reported every (aprox.) timer_step seconds')
    logger.info('Execution is interrupted if no progress is detected for (aprox.) max_time_stuck seconds')
    logger.info('===== LAUNCHING PARALLELIZER ====='.format(sleep_time_lst))
    logger.info('Parallelizing the function directly, no additional arguments')
    out=parallelize(my_sleep,sleep_time_lst,cores=2,timer_step=5,max_time_stuck=10)
# Expected output
# 05/14/2017 07:20:53 PM timer        INFO     0 items processed [0:00:06]. 6 items left [0:00:36]
# 05/14/2017 07:20:53 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:20:53 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:20:58 PM timer        INFO     2 items processed [0:00:11]. 4 items left [0:00:22]
# 05/14/2017 07:21:01 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:21:01 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:21:03 PM timer        INFO     4 items processed [0:00:16]. 2 items left [0:00:08]
# 05/14/2017 07:21:08 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:21:08 PM timer        INFO     5 items processed [0:00:21]. 1 items left [0:00:04]
# 05/14/2017 07:21:12 PM timer        INFO     5 items processed [0:00:25]. 1 items left [0:00:05]
# 05/14/2017 07:21:17 PM timer        INFO     5 items processed [0:00:30]. 1 items left [0:00:06]
# 05/14/2017 07:21:22 PM timer        INFO     5 items processed [0:00:35]. 1 items left [0:00:07]
# 05/14/2017 07:21:22 PM parallelize  WARNING  Terminating the job pool: 1 out of 6 jobs got stuck!
    logger.info('Parallelizing the function directly, with additional args')
    out=parallelize(my_sleep,sleep_time_lst,('Args!',),cores=2,timer_step=5,max_time_stuck=10)
# Expected output
# 05/14/2017 07:21:53 PM timer        INFO     0 items processed [0:00:05]. 6 items left [0:00:34]
# 05/14/2017 07:21:55 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:21:55 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:21:58 PM timer        INFO     2 items processed [0:00:10]. 4 items left [0:00:21]
# 05/14/2017 07:22:02 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:22:02 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:22:03 PM timer        INFO     4 items processed [0:00:15]. 2 items left [0:00:07]
# 05/14/2017 07:22:08 PM timer        INFO     4 items processed [0:00:20]. 2 items left [0:00:10]
# 05/14/2017 07:22:09 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:22:13 PM timer        INFO     5 items processed [0:00:25]. 1 items left [0:00:05]
# 05/14/2017 07:22:18 PM timer        INFO     5 items processed [0:00:30]. 1 items left [0:00:06]
# 05/14/2017 07:22:23 PM timer        INFO     5 items processed [0:00:35]. 1 items left [0:00:07]
# 05/14/2017 07:22:23 PM parallelize  WARNING  Terminating the job pool: 1 out of 6 jobs got stuck!
    logger.info('Parallelizing the function directly, with additional kwargs')
    out=parallelize(my_sleep,sleep_time_lst,msg='Kwargs!',cores=2,timer_step=5,max_time_stuck=10)
# Expected output
# 05/14/2017 07:22:29 PM timer        INFO     0 items processed [0:00:06]. 6 items left [0:00:36]
# 05/14/2017 07:22:30 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:22:30 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:22:35 PM timer        INFO     2 items processed [0:00:11]. 4 items left [0:00:22]
# 05/14/2017 07:22:37 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:22:37 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:22:40 PM timer        INFO     4 items processed [0:00:16]. 2 items left [0:00:08]
# 05/14/2017 07:22:44 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:22:45 PM timer        INFO     5 items processed [0:00:21]. 1 items left [0:00:04]
# 05/14/2017 07:22:49 PM timer        INFO     5 items processed [0:00:25]. 1 items left [0:00:05]
# 05/14/2017 07:22:54 PM timer        INFO     5 items processed [0:00:30]. 1 items left [0:00:06]
# 05/14/2017 07:22:59 PM timer        INFO     5 items processed [0:00:35]. 1 items left [0:00:07]
# 05/14/2017 07:22:59 PM parallelize  WARNING  Terminating the job pool: 1 out of 6 jobs got stuck!
    logger.info('Parallelizing the function through the wrapper, no additional arguments')
    out=parallelize(function_wrapper,sleep_time_lst,(my_sleep,),cores=2,timer_step=5,max_time_stuck=10)
# Expected output
# 05/14/2017 07:23:05 PM timer        INFO     0 items processed [0:00:06]. 6 items left [0:00:36]
# 05/14/2017 07:23:06 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:23:06 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:23:10 PM timer        INFO     2 items processed [0:00:11]. 4 items left [0:00:22]
# 05/14/2017 07:23:13 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:23:13 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:23:15 PM timer        INFO     4 items processed [0:00:16]. 2 items left [0:00:08]
# 05/14/2017 07:23:20 PM my_sleep     DEBUG    [Hey!] Slept for 7s!
# 05/14/2017 07:23:20 PM timer        INFO     5 items processed [0:00:21]. 1 items left [0:00:04]
# 05/14/2017 07:23:24 PM timer        INFO     5 items processed [0:00:25]. 1 items left [0:00:05]
# 05/14/2017 07:23:29 PM timer        INFO     5 items processed [0:00:30]. 1 items left [0:00:06]
# 05/14/2017 07:23:34 PM timer        INFO     5 items processed [0:00:35]. 1 items left [0:00:07]
# 05/14/2017 07:23:34 PM parallelize  WARNING  Terminating the job pool: 1 out of 6 jobs got stuck!
    logger.info('Parallelizing the function through the wrapper, with additional args')
    out=parallelize(function_wrapper,sleep_time_lst,(my_sleep,'Args!'),cores=2,timer_step=5,max_time_stuck=10)
# Expected output
# 05/14/2017 07:23:41 PM timer        INFO     0 items processed [0:00:06]. 6 items left [0:00:37]
# 05/14/2017 07:23:41 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:23:41 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:23:46 PM timer        INFO     2 items processed [0:00:11]. 4 items left [0:00:22]
# 05/14/2017 07:23:48 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:23:48 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:23:51 PM timer        INFO     4 items processed [0:00:16]. 2 items left [0:00:08]
# 05/14/2017 07:23:55 PM my_sleep     DEBUG    [Args!] Slept for 7s!
# 05/14/2017 07:23:56 PM timer        INFO     5 items processed [0:00:21]. 1 items left [0:00:04]
# 05/14/2017 07:24:00 PM timer        INFO     5 items processed [0:00:25]. 1 items left [0:00:05]
# 05/14/2017 07:24:05 PM timer        INFO     5 items processed [0:00:30]. 1 items left [0:00:06]
# 05/14/2017 07:24:10 PM timer        INFO     5 items processed [0:00:35]. 1 items left [0:00:07]
# 05/14/2017 07:24:10 PM parallelize  WARNING  Terminating the job pool: 1 out of 6 jobs got stuck!
    logger.info('Parallelizing the function through the wrapper, with additional kwargs')
    out=parallelize(function_wrapper,sleep_time_lst,(my_sleep,),msg='Kwargs!',cores=2,timer_step=5,max_time_stuck=10)
# Expected output
# 05/14/2017 07:24:17 PM timer        INFO     0 items processed [0:00:06]. 6 items left [0:00:40]
# 05/14/2017 07:24:17 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:24:17 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:24:22 PM timer        INFO     2 items processed [0:00:11]. 4 items left [0:00:23]
# 05/14/2017 07:24:24 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:24:24 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:24:27 PM timer        INFO     4 items processed [0:00:16]. 2 items left [0:00:08]
# 05/14/2017 07:24:31 PM my_sleep     DEBUG    [Kwargs!] Slept for 7s!
# 05/14/2017 07:24:32 PM timer        INFO     5 items processed [0:00:21]. 1 items left [0:00:04]
# 05/14/2017 07:24:36 PM timer        INFO     5 items processed [0:00:26]. 1 items left [0:00:05]
# 05/14/2017 07:24:41 PM timer        INFO     5 items processed [0:00:31]. 1 items left [0:00:06]
# 05/14/2017 07:24:46 PM timer        INFO     5 items processed [0:00:36]. 1 items left [0:00:07]
# 05/14/2017 07:24:46 PM parallelize  WARNING  Terminating the job pool: 1 out of 6 jobs got stuck!    
    logger.info('Output of the parallelizer: {}'.format(out))
# Expected output
# 05/14/2017 07:40:09 PM sample_run   INFO     Output of the parallelizer: [True, True, True, True, True]