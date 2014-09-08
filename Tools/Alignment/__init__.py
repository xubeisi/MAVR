__author__ = 'mahajrod'

from Tools.Alignment.Bowtie2 import Bowtie2
from Tools.Alignment.BWA import BWA
from Tools.Alignment.Novoalign import Novoalign
from Tools.Alignment.TMAP import TMAP

max_threads = 4
bowtie2_path = ""
bwa_path = ""
novoalign_path = ""
tmap_path = ""
Bowtie2 = Bowtie2(path=bowtie2_path, max_threads=max_threads)
BWA = BWA(path=bwa_path, max_threads=max_threads)
Novoalign = Novoalign(path=novoalign_path, max_threads=max_threads)
TMAP = TMAP(path=novoalign_path, max_threads=max_threads)