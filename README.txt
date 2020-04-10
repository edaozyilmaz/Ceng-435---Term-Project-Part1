Eda Özyılmaz 2171882
Hilal Ünal 2172112

STEPS:

1. Connect each node with ssh using commands:
    for node d: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2172112@pc2.instageni.nps.edu -p 26610
    for node r1: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2172112@pc2.instageni.nps.edu -p 26611
    for node r2: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2172112@pc2.instageni.nps.edu -p 26612
    for node r3: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2172112@pc2.instageni.nps.edu -p 26613
    for node s: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2172112@pc2.instageni.nps.edu -p 26614

2. For each node, copy the corresponding files to machines. Also for node s, d and r2 copy deneme.txt to machines.

3. Synchronize each node using:
    $ sudo service ntp stop
    $ sudo ntpdate -s ops.instageni.nps.edu
    $ sudo service ntp start

4. For "discovery" part run the scripts on following order:
     $ python s.py
     $ python d.py
     $ python r2.py
     $ python r1.py
     $ python r3.py

5. After discovery part is over, it created text that contains link cost for r1, r2 and r3:
      for r1: linkCost1.txt
      for r2: linkCost2.txt
      for r3: linkCost3.txt

6. For all the parts of the "experiment" first do:
    a. For experiment 1:
     for node s:
		   $ sudo tc qdisc add dev eth2 root netem delay 40ms 5ms distribution normal  #conection between s-r3
     for node r3:
			 $ sudo tc qdisc add dev eth2 root netem delay 40ms 5ms distribution normal  #conection between s-r3
       $ sudo tc qdisc add dev eth3 root netem delay 40ms 5ms distribution normal  #conection between r3-d
     for node d:
			 $ sudo tc qdisc add dev eth3 root netem delay 40ms 5ms distribution normal  #conection between r3-d
    b. For experiment 2:
     for node s:
  		 $ sudo tc qdisc add dev eth2 root netem delay 40ms 5ms distribution normal  #conection between s-r3
     for node r3:
  		 $ sudo tc qdisc add dev eth2 root netem delay 40ms 5ms distribution normal  #conection between s-r3
       $ sudo tc qdisc add dev eth3 root netem delay 40ms 5ms distribution normal  #conection between r3-d
     for node d:
  		 $ sudo tc qdisc add dev eth3 root netem delay 40ms 5ms distribution normal  #conection between r3-d
    c. For experiment 3:
     for node s:
  		 $ sudo tc qdisc add dev eth2 root netem delay 50ms 5ms distribution normal  #conection between s-r3
     for node r3:
  		 $ sudo tc qdisc add dev eth2 root netem delay 50ms 5ms distribution normal  #conection between s-r3
       $ sudo tc qdisc add dev eth3 root netem delay 50ms 5ms distribution normal  #conection between r3-d
     for node d:
  		 $ sudo tc qdisc add dev eth3 root netem delay 50ms 5ms distribution normal  #conection between r3-d

7. After all experiments to reset the existing delay before entering new delay do:
     for node s:
       $ sudo tc qdisc del dev eth2 root netem
     for node r3:
       $ sudo tc qdisc del dev eth2 root netem
       $ sudo tc qdisc del dev eth3 root netem
     for node d:
       $ sudo tc qdisc del dev eth3 root netem

8. For "experiment" part run the scripts on following order:
     $ python s_exp.py
     $ python d_exp.py
     $ python r3_exp.py

9. After the codes stop, d_exp.py prints the end-to-end delay.
