Return a list of related pages between two pdfs.

##### Requirements

Ubuntu >= 14.10 

##### Install

Run as sudo

```
apt-get install python-pythonmagick

pip install pyPdf

apt-get install libpq-dev python-dev

apt-get install libopencv-dev python-opencv

ln /dev/null /dev/raw1394 # disable libdc1394 error (cause by unused opencv coedec )

apt-get install pdftk 
```

Make sure pdf are decompressed before running script

```pdftk doc.pdf output doc.unc.pdf uncompress```

##### Example Usage

``python inspection.py -h``

``python inspection.py data/test/A.pdf data/test/B.pdf``

``python inspection.py --cases example --include Example1 data/test/A.pdf data/test/F.pdf``

``python inspection.py --cases example --include Example2 --exclude DefaultTest data/test/A.pdf data/test/F.pdf``

``python inspection.py --cases example --include Example3 --exclude DefaultTest --check any data/test/A.pdf data/test/F.pdf``

python inspection.py --cases example --include Example1 --check any  data/test/m25.pdf  data/test/m26.pdf 

##### Algorithms

http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.array_equiv.html#numpy.array_equiv

http://docs.opencv.org/2.4/modules/imgproc/doc/histograms.html?highlight=comparehist#comparehist

https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

##### Python Modules

https://docs.python.org/2/library/unittest.html

##### Functionality Tests

``python -m unittest test``

##### Debugging

Use the ``output.log`` file to see STDOUT of the pdf test execution.  To view the output in realtime open a new terminal screen and use the command ``tail -f output.log``. 

Warning: The python debugger will only be useful in the main function of the inspection.py file. The rest of this program is excuted as a different process, with STDOUT being written to file. Meaning there will be no way to directly interact with the debugger at this time.  

##### Starting instructions
vagrant up
vagrant provision
vagrant ssh  #this will open linux terminal
cd /vagrant/development/cnx-inspection-v2/inspections
sudo chown -R vagrant cnx-inspection-v2/
sudo chgrp -R vagrant cnx-inspection-v2/
git pull

then run the tests you want.
