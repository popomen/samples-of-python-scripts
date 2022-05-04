import time
import datetime
import argparse
import sys
import os
import random
import signal

parser = argparse.ArgumentParser(description='sleep xxx seconds')
parser.add_argument('--exit_code', type=int, default=0)
parser.add_argument('--seconds', type=int, default=60)
parser.add_argument('--graceful_exit_seconds', type=int, default=3)
parser.add_argument('--data_url', type=str, default='/home/ma-user/modelarts/inputs/data_url_0')
parser.add_argument('--train_url', type=str, default='/home/ma-user/modelarts/outputs/output_url_0')
parser.add_argument('--train_size', type=int, default=16*1024*1024)
args=parser.parse_args()

def main():
    signal.signal(signal.SIGTERM, handleTerm)
    signal.signal(signal.SIGINT, handleTerm)

    log("The training job will exit with ", args.exit_code, " after sleeping for ", args.seconds, " seconds")

    for i in range(1, args.seconds):
        log("The training job has been running for ", i, " seconds")
        time.sleep(1)
    
    # 生成模型
    genMockTrainingFile()

    log("The training job will exit with ", args.exit_code)
    sys.exit(args.exit_code)

# 模拟优雅推出后处理动作。
def handleTerm(sigNum, stack):
    s = 60
    log("Received terminate signal ", sigNum, " try to graceful exit, need ", args.graceful_exit_seconds, " seconds")
    for i in range(1, args.graceful_exit_seconds):
        log("Waiting for ", i, " seconds")
        time.sleep(1)
    
    # 以 exit_code 参数作为退出码退出。
    log("The training job will exit with ", args.exit_code)
    sys.exit(args.exit_code)

# 模拟一次生成模型文件。
def genMockTrainingFile():
    train_url = args.train_url
    train_size = args.train_size

    file_path = os.path.join(train_url, 'mock_ckpt_' + str(train_size) + 'B_' + str(int(time.time())))
    log("Generating mock training output file, file name: ", file_path, ", size: ", train_size)

    ds = 0
    with open(file_path, "w", encoding="utf-8") as f:
        while ds < train_size:
            f.write(str(round(random.uniform(-1000, 1000), 2)))
            f.write("\n")
            ds=os.path.getsize(file_path)

# 打印带有时间戳的日志。
def log(*msg_list):
    new_msg_list = [str(x) for x in msg_list]
    s = ''
    print("[", datetime.datetime.now(), "] ", s.join(new_msg_list), sep='')

if __name__ == '__main__':
    main()