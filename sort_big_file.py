#!/usr/bin/python2
# coding=utf-8
#
# Opens file "data.csv" and sorts data by price
# By Samuel
# 02/09/2018
# Due to the input file could be very big, this code is based on https://github.com/ActiveState/code/blob/3b27230f418b714bc9a0f897cb8ea189c3515e99/recipes/Python/576755_Sorting_big_files_Pyth26/recipe-576755.py and made some changes
# Usage: python sort_big_file.py Intro_Test-sample_data.csv sort.result

from heapq import heapify, heappop, heappush
from itertools import islice, cycle
from tempfile import gettempdir
import os



def merge(chunks):
    values = []

    for index, chunk in enumerate(chunks):
        try:
            iterator = iter(chunk)
            value = iterator.next()
        except StopIteration:
            try:
                chunk.close()
                os.remove(chunk.name)
                chunks.remove(chunk)
            except:
                pass
        else:
            heappush(values,(index,value,iterator,chunk))

    while values:
        index, value, iterator, chunk = heappop(values)
	print value.strip()
        yield value
        try:
            value = iterator.next()
        except StopIteration:
            try:
                chunk.close()
                os.remove(chunk.name)
                chunks.remove(chunk)
            except:
                pass
        else:
            heappush(values,(index,value,iterator,chunk))

'''
   compare number is bigger or smaller
'''
def sort_cmp(x, y):
    try:
        temp = float(y.split(',')[3]) - float(x.split(',')[3])
        if temp > 0.0:
            return 1
        elif temp == 0.0:
            return 0
        else:
            return -1
    except ValueError:
        #print 'Please check the fourth column is  a number'
        '''
	if it's the headline, make it at the first line
	'''
	return 1

def batch_sort(input,output,buffer_size=32000,tempdirs=[]):
    if not tempdirs:
        tempdirs.append(gettempdir())
    
    input_file = file(input,'rb',64*1024)
    try:
        input_iterator = iter(input_file)
        
        chunks = []
        try:
            for tempdir in cycle(tempdirs):
                current_chunk = list(islice(input_iterator,buffer_size))
                if current_chunk:
                    current_chunk.sort(cmp=sort_cmp)
                    output_chunk = file(os.path.join(tempdir,'%06i'%len(chunks)),'w+b',64*1024)
                    output_chunk.writelines(current_chunk)
                    output_chunk.flush()
                    output_chunk.seek(0)
                    chunks.append(output_chunk)
                else:
                    break
        except:
            for chunk in chunks:
                try:
                    chunk.close()
                    os.remove(chunk.name)
                except:
                    pass
            if output_chunk not in chunks:
                try:
                    output_chunk.close()
                    os.remove(output_chunk.name)
                except:
                    pass
            return
    finally:
        input_file.close()
       
    output_file = file(output,'wb',64*1024)
    try:
        output_file.writelines(merge(chunks))
    finally:
        for chunk in chunks:
            try:
                chunk.close()
                os.remove(chunk.name)
            except:
                pass
        output_file.close()
    
if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option(
        '-b','--buffer',
        dest='buffer_size',
        type='int',default=32000,
        help='''Size of the line buffer. The file to sort is
            divided into chunks of that many lines. Default : 32,000 lines.'''
    )
    parser.add_option(
        '-t','--tempdir',
        dest='tempdirs',
        action='append',
        default=[],
        help='''Temporary directory to use. You might get performance
            improvements if the temporary directory is not on the same physical
            disk than the input and output directories. You can even try
            providing multiples directories on differents physical disks.
            Use multiple -t options to do that.'''
    )
    
    options,args = parser.parse_args()
    
    batch_sort(args[0],args[1],options.buffer_size,options.tempdirs) 
