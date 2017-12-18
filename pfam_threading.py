import os
import threading

def init():
    InputDir = "/home/haidong/PycharmProjects/Anti-crispr/bacteria_sub/subdir_2"
    PfamScanDir = "/home/haidong/huangle/PfamScan"
    chunk_size = 180
    a = []
    a.append(InputDir)
    a.append(PfamScanDir)
    a.append(chunk_size)
    return a
def myfunc(i,InputDir,chunk_size,PfamScanDir):
    crisper_model_path = PfamScanDir + '/crisper_model.hmm'
    hmmscan_parser_path = PfamScanDir+'/hmmscan-parser.sh'
    '''get input files
    '''
    Dirs = os.listdir(InputDir)
    Dir_arr = list(chunks(Dirs,chunk_size))
    Dir_len = len(Dir_arr)
    myDirList = Dir_arr[i]
    dir_len = len(myDirList)
    cnt = 0
    for onedir in myDirList:
        GenDir = InputDir + '/' + onedir
        acaPath = GenDir+'/'+'aca_predict.txt'
        acaHmmPath = GenDir + '/' +'aca_predict_result.txt'
        acaHmmParsePath = GenDir +'/' +'aca_predict_result_parse.txt'
        '''Judge file is empty or not
        '''
        if os.path.getsize(acaPath)==0:
            f = open(acaHmmPath,"w")
            f.close()
            f1 = open(acaHmmParsePath,"w")
            f1.close()
        else:
            os.system("hmmscan --domtblout "+acaHmmPath+" "+crisper_model_path+" "+acaPath+" > /dev/null")
            os.system("bash "+hmmscan_parser_path+" " +acaHmmPath+" > "+acaHmmParsePath)
        i = i+1
        if i%100==0:
            print(i)
        # print ("bash "+hmmscan_parser_path+" " + acaHmmPath+" > "+acaHmmParsePath)
def chunks(l,n):
    """Yield successive n-sized chunks from l.
    """
    for i in range(0,len(l), n):
        yield l[i:i+n]



arr = init()
# print (arr[1])
InputDir = arr[0]
PfamScanDir = arr[1]
chunk_size = arr[2]
# print (PfamScanDir)

''' Create the threads
use threading function to run the chunks
'''
Dirs = os.listdir(InputDir)
Dir_arr = list(chunks(Dirs,chunk_size))
Dir_len = len(Dir_arr)
threads = []
for i in range(Dir_len):
    threads.append(threading.Thread(target=myfunc,args=(i,InputDir,chunk_size,PfamScanDir)))
for t in threads:
    t.start()
