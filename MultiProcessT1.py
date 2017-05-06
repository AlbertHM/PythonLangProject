import multiprocessing as mp
import time
import random

def Pencetak(queue):
	ygBC = 0
	tThr = 30
	t = 0
	
	while t < tThr :
		if queue.empty():
			t += 1
			print("{} menunggu item untuk diproses kosong ke{}".format(mp.current_process().name,t))
		else:
			barang = queue.get()
			print("{} memproses barang {}".format(mp.current_process().name, barang))
			ygBC +=1
		time.sleep(random.random() * 1)
			
	print("Total barang yang dibaca {}".format(str(ygBC)))

def Pengadaan(count, queue):
	jml_p = 0
	
	for i in range(count):
		item = random.choice(Listbarang)
		queue.put(item)
		
		print("Memberikan barang '{}' di list".format(item))
		time.sleep(random.random() * 0.50)
		


if __name__ == '__main__':
	st = time.time()

	count = 30	
	q = mp.Queue()
	Listbarang = ('speaker', 'laptop', 'pc', 'mouse', 'keyboard')
	pencetak_1 = mp.Process(target=Pencetak, name='Pencetak1', args=(q,))
	pencetak_1.daemon = True
	pencetak_1.start()
	pencetak_2 = mp.Process(target=Pencetak, name='Pencetak2', args=(q,))
	pencetak_2.daemon = True
	pencetak_2.start()
	
	Pengadaan(count, q)
	
	et = time.time()
	pencetak_1.join()
	pencetak_2.join()
	print('Total running time {}'.format(et-st))
	
