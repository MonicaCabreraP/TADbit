Compartments and TADs detection
===============================



Here, we present the analysis to detect the compartments in Mouse B and
iPS cells. In this example, we will use the GC-content (guanine-cytosine
content) to identify which bins belong to the A or B compartments. The
percentage of bases that are either guanine or cytosine on a DNA strand
correlates directly with gene density and is a good measure to identify
open and close chromatine.

**Note**\ *: Compartments are detected on the full genome matrix.*

.. code:: ipython3

    from pytadbit.parsers.hic_parser import load_hic_data_from_bam
    from pytadbit.parsers.genome_parser import get_gc_content, parse_fasta
    from pickle import load

.. code:: ipython3

    reso = 200000
    base_path = 'results/fragment/{0}_both/03_filtering/valid_reads12_{0}.bam'
    bias_path = 'results/fragment/{0}_both/04_normalizing/biases_{0}_both_{1}kb.biases'

.. code:: ipython3

    rich_in_A = get_gc_content(parse_fasta('genome/Mus_musculus-GRCm38.p6/Mus_musculus-GRCm38.p6.fa'), 
                               by_chrom=True ,resolution=reso, n_cpus=8)


.. ansi-block::

    Loading cached genome


Compartments
------------

Mouse B cells
~~~~~~~~~~~~~

.. code:: ipython3

    cell   = 'mouse_B'

.. code:: ipython3

    hic_data = load_hic_data_from_bam(base_path.format(cell),
                                      resolution=reso,
                                      biases=bias_path.format(cell, reso // 1000),
                                      ncpus=8)


.. ansi-block::

    
      (Matrix size 13641x13641)                                                    [2020-02-06 12:04:07]
    
      - Parsing BAM (122 chunks)                                                   [2020-02-06 12:04:08]
         .......... .......... .......... .......... ..........     50/122
         .......... .......... .......... .......... ..........    100/122
         .......... .......... ..                                  122/122
    
      - Getting matrices                                                           [2020-02-06 12:06:28]
         .......... .......... .......... .......... ..........     50/122
         .......... .......... .......... .......... ..........    100/122
         .......... .......... ..                                  122/122
    


.. code:: ipython3

    ! mkdir -p results/fragment/$cell\_both/05_segmenting

.. code:: ipython3

    chrname = 'chr3'
    corr = hic_data.find_compartments(show_compartment_labels=True,
            show=True, crms=[chrname], vmin='auto', vmax='auto', rich_in_A=rich_in_A, 
            savedata='results/fragment/{0}_both/05_segmenting/compartments_{1}_{2}.tsv'.format(cell, chrname, reso),
            savedir='results/fragment/{0}_both/05_segmenting/eigenvectors_{1}_{2}'.format(cell, chrname, reso))



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_10_0.png


Mouse iPS cells
~~~~~~~~~~~~~~~

.. code:: ipython3

    cell   = 'mouse_PSC'

.. code:: ipython3

    hic_data = load_hic_data_from_bam(base_path.format(cell),
                                      resolution=reso,
                                      biases=bias_path.format(cell, reso // 1000),
                                      ncpus=8)


.. ansi-block::

    
      (Matrix size 13641x13641)                                                    [2020-02-06 12:20:31]
    
      - Parsing BAM (122 chunks)                                                   [2020-02-06 12:20:32]
         .......... .......... .......... .......... ..........     50/122
         .......... .......... .......... .......... ..........    100/122
         .......... .......... ..                                  122/122
    
      - Getting matrices                                                           [2020-02-06 12:22:08]
         .......... .......... .......... .......... ..........     50/122
         .......... .......... .......... .......... ..........    100/122
         .......... .......... ..                                  122/122
    


.. code:: ipython3

    ! mkdir -p results/fragment/$cell\_both/05_segmenting

.. code:: ipython3

    chrname = 'chr3'
    corr = hic_data.find_compartments(show_compartment_labels=True,
            show=True, crms=[chrname], vmin='auto', vmax='auto', rich_in_A=rich_in_A,
            savedata='results/fragment/{0}_both/05_segmenting/compartments_{1}_{2}.tsv'.format(cell, chrname, reso),
            savedir='results/fragment/{0}_both/05_segmenting/eigenvectors_{1}_{2}'.format(cell, chrname, reso))



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_15_0.png


Compare
~~~~~~~

The assignments of the compartments for the two cell types are stored in
two different files:

.. code:: ipython3

    ! head -n 20 results/fragment/mouse_B_both/05_segmenting/compartments_chr3_200000.tsv


.. ansi-block::

    ## CHR chr3	Eigenvector: 1
    #	start	end	rich in A	type
    chr3	16	44	0.40	B
    chr3	45	52	0.50	A
    chr3	53	72	0.40	B
    chr3	73	76	0.53	A
    chr3	77	96	0.39	B
    chr3	97	98	0.82	A
    chr3	99	100	0.82	B
    chr3	101	101	nan	A
    chr3	102	108	0.46	B
    chr3	109	111	0.62	A
    chr3	112	135	0.40	B
    chr3	136	139	0.59	A
    chr3	140	153	0.44	B
    chr3	154	156	0.64	A
    chr3	157	162	0.51	B
    chr3	163	164	0.87	A
    chr3	165	178	0.46	B
    chr3	179	181	0.61	A


.. code:: ipython3

    ! head -n 20 results/fragment/mouse_PSC_both/05_segmenting/compartments_chr3_200000.tsv


.. ansi-block::

    ## CHR chr3	Eigenvector: 1
    #	start	end	rich in A	type
    chr3	16	42	0.40	B
    chr3	43	52	0.49	A
    chr3	53	75	0.40	B
    chr3	76	76	nan	A
    chr3	77	96	0.39	B
    chr3	97	97	nan	A
    chr3	98	109	0.43	B
    chr3	110	111	0.84	A
    chr3	112	135	0.40	B
    chr3	136	145	0.48	A
    chr3	146	152	0.47	B
    chr3	153	156	0.57	A
    chr3	157	160	0.56	B
    chr3	161	165	0.54	A
    chr3	166	169	0.54	B
    chr3	170	183	0.46	A
    chr3	184	184	nan	B
    chr3	188	189	0.84	A


In another folder, we also saved the coordinates of each computed
eigenvector:

.. code:: ipython3

    ! ls -lh results/fragment/mouse_B_both/05_segmenting/eigenvectors_chr3_200000


.. ansi-block::

    total 52K
    -rw-r--r-- 1 dcastillo dcastillo 49K Feb  6 12:08 chr3_EigVect1.tsv


**Note**\ *: In this file the first line shows the eigenvector index
with it’s corresponding eigenvalue (the first column should always be
the one you selected, even if it is not the first eigenvector).*

Then there are the coordinates of the eigenvectors. In the first column,
the coordinates correspond to the assignment of the A and B
compartments, positive values for A compartments and negative values for
B compartments.

.. code:: ipython3

    ! head -n 20 results/fragment/mouse_B_both/05_segmenting/eigenvectors_chr3_200000/chr3_EigVect1.tsv


.. ansi-block::

    # EV_1 (199.3674)	EV_2 (38.9365)	EV_3 (22.7067)
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    nan	nan	nan
    -0.04705877433867864	0.0008416946845418325	-0.0418514300736033
    -0.04570124930041132	0.004910131406689665	-0.03832275686221951
    -0.04591426453743422	0.002039448345766754	-0.035967872719506695
    -0.044857688854588844	0.003962351416820969	-0.04230275892744377


Load eigenvectors coordinates from files:

.. code:: ipython3

    from builtins   import next
    
    fh = open('results/fragment/mouse_B_both/05_segmenting/eigenvectors_chr3_200000/chr3_EigVect1.tsv')
    
    header = next(fh)
    
    ev1_B = []
    for line in fh:
        evc1, evc2, evc3 = line.split()
        ev1_B.append(float(evc1))
        
    fh = open('results/fragment/mouse_PSC_both/05_segmenting/eigenvectors_chr3_200000/chr3_EigVect1.tsv')
    
    header = next(fh)
    
    ev1_PSC = []
    for line in fh:
        evc1, evc2, evc3 = line.split()
        ev1_PSC.append(float(evc1))
        
    diff = []
    for i in range(len(ev1_B)):
        diff.append(ev1_B[i] - ev1_PSC[i])

Spot changes in activity
~~~~~~~~~~~~~~~~~~~~~~~~

Plot the difference between each eigenvector along chromosome

.. code:: ipython3

    from matplotlib import pyplot as plt

.. code:: ipython3

    plt.figure(figsize=(12, 2))
    plt.text(10, 0.07, 'More active in B cell')
    plt.fill_between(range(len(diff)), diff, 0, where=[i>0 for i in diff])
    plt.text(10, -0.09, 'More active in PSC cell')
    plt.fill_between(range(len(diff)), diff, 0, where=[i<0 for i in diff])
    plt.xlim(0, len(diff))
    plt.ylim(-0.1, 0.1)
    plt.ylabel('difference of EV')
    _ = plt.xlabel('Genomic coordinate (%s kb)' % (reso / 1000))



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_29_0.png


Correlate eigenvectors
~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    plt.figure(figsize=(6, 6))
    for i in range(len(ev1_B)):
        if ev1_B[i] > 0 and ev1_PSC[i] > 0:
            plt.plot(ev1_B[i], ev1_PSC[i], 'ro', alpha=0.5)
        elif ev1_B[i] < 0 and ev1_PSC[i] < 0:
            plt.plot(ev1_B[i], ev1_PSC[i], 'bo', alpha=0.5)
        else:
            plt.plot(ev1_B[i], ev1_PSC[i], 'o', color='grey', alpha=0.5)
    plt.axhline(0, color='k', alpha=0.2)
    plt.axvline(0, color='k', alpha=0.2)
    plt.xlabel('B cell EV1')
    _ = plt.ylabel('PSC cell EV1')



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_31_0.png


TADs
----

Now, we move to the TADs detection. In this notebook we will detect TAD
borders at 100kbp resolution.

.. raw:: html

   <!-- The comparison of TAD borders at high resolutions becomes difficult because the border positions are not as sharply defined as at lower resolutions.

   An example of consistency between TAD borders is shown in the following graph. TAD borders are called at 1 kb resolution (insulation score-based method). We assume that there should be a high ratio of conservation between the 4 replicates and as we see that's true for resolutions lower than approximately 100kbp. If our bin size is for example 50kbp, we only reach the same ratio of consistency if we consider TAD borders found 2 bins away as being the same border in the different replicates.

   <img src="../nbpictures/TAD_calling_resolution.png"> -->

.. code:: ipython3

    from pytadbit import Chromosome
    from pytadbit.parsers.hic_parser import load_hic_data_from_bam

.. code:: ipython3

    base_path = 'results/fragment/{0}_both/03_filtering/valid_reads12_{0}.bam'
    bias_path = 'results/fragment/{0}_both/04_normalizing/biases_{0}_both_{1}kb.biases'
    
    reso = 100000
    
    cel1 = 'mouse_B'
    cel2 = 'mouse_PSC'

.. code:: ipython3

    hic_data1 = load_hic_data_from_bam(base_path.format(cel1),
                                       resolution=reso,
                                       region='chr3',
                                       biases=bias_path.format(cel1, reso // 1000),
                                       ncpus=8)
    hic_data2 = load_hic_data_from_bam(base_path.format(cel2),
                                       resolution=reso,
                                       region='chr3',
                                       biases=bias_path.format(cel2, reso // 1000),
                                       ncpus=8)


.. ansi-block::

    
      (Matrix size 1601x1601)                                                      [2020-02-06 12:36:22]
    
      - Parsing BAM (101 chunks)                                                   [2020-02-06 12:36:24]
         .......... .......... .......... .......... ..........     50/101
         .......... .......... .......... .......... ..........    100/101
         .                                                         101/101
    
      - Getting matrices                                                           [2020-02-06 12:36:28]
         .......... .......... .......... .......... ..........     50/101
         .......... .......... .......... .......... ..........    100/101
         .                                                         101/101
    
    
      (Matrix size 1601x1601)                                                      [2020-02-06 12:36:54]
    
      - Parsing BAM (101 chunks)                                                   [2020-02-06 12:36:55]
         .......... .......... .......... .......... ..........     50/101
         .......... .......... .......... .......... ..........    100/101
         .                                                         101/101
    
      - Getting matrices                                                           [2020-02-06 12:36:59]
         .......... .......... .......... .......... ..........     50/101
         .......... .......... .......... .......... ..........    100/101
         .                                                         101/101
    


.. code:: ipython3

    chrname = 'chr3'
    crm = Chromosome(chrname)
    crm.add_experiment('mouse_B',  
                       hic_data=[hic_data1.get_matrix(focus='chr3')],
                       norm_data=[hic_data1.get_matrix(focus='chr3',normalized=True)],
                       resolution=reso)
    crm.add_experiment('mouse_PSC', 
                       hic_data=[hic_data2.get_matrix(focus='chr3')],
                       norm_data=[hic_data2.get_matrix(focus='chr3',normalized=True)],
                       resolution=reso)

.. code:: ipython3

    crm.visualize([('mouse_B', 'mouse_PSC')])



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_39_0.png


TAD caller algorithms
~~~~~~~~~~~~~~~~~~~~~

TADbit
~~~~~~

TADbit is the original TAD caller algorithm TADbit is a breakpoint
detection algorithm that returns the optimal segmentation of the
chromosome under BIC-penalized likelihood. The model assumes that counts
have a Poisson distribution and that the expected value of the counts
decreases like a power-law with the linear distance on the chromosome.

.. code:: ipython3

    crm.find_tad(['mouse_B', 'mouse_PSC'], n_cpus=8)

.. code:: ipython3

    crm.visualize([('mouse_B', 'mouse_PSC')], normalized=True, paint_tads=True)



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_44_0.png


.. code:: ipython3

    crm.visualize([('mouse_B', 'mouse_PSC')], normalized=True, paint_tads=True, focus=(300, 360))



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_45_0.png


.. code:: ipython3

    B = crm.experiments['mouse_B']
    PSC = crm.experiments['mouse_PSC']

.. code:: ipython3

    crm.experiments




.. ansi-block::

    [Experiment mouse_B (resolution: 100 kb, TADs: 96, Hi-C rows: 1601, normalized: visibility),
     Experiment mouse_PSC (resolution: 100 kb, TADs: 118, Hi-C rows: 1601, normalized: visibility)]



TopDom
~~~~~~

TopDom identifies TAD borders based on the assumption that contact
frequencies between regions upstream and downstream of a border are
lower than those between two regions within a TAD. The algorithm only
depends on a single parameter corresponding to the window size. The
algorithm provides a measure (from 0 to 10) of confidence on the
accuracy of the border detection
(https://www.ncbi.nlm.nih.gov/pubmed/26704975).

.. code:: ipython3

    crm.find_tad(['mouse_B', 'mouse_PSC'], n_cpus=8, use_topdom=True)

.. code:: ipython3

    crm.visualize([('mouse_B', 'mouse_PSC')], normalized=True, paint_tads=True)



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_51_0.png


.. code:: ipython3

    crm.visualize([('mouse_B', 'mouse_PSC')], normalized=True, paint_tads=True, focus=(300, 360))



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_52_0.png


Insulation score
~~~~~~~~~~~~~~~~

Insulation score (Crane et al. 2015 https://doi.org/10.1038/nature14450)
can be used to build an insulation profile of the genome and, with a
simple transformation, to identify TAD borders.



.. code:: ipython3

    from pytadbit.tadbit import insulation_score, insulation_to_borders

First we need to normalize the matrices by visibility and by decay:

.. code:: ipython3

    hic_data1.normalize_hic()
    hic_data1.normalize_expected()
    
    hic_data2.normalize_hic()
    hic_data2.normalize_expected()


.. ansi-block::

    iterative correction
      - copying matrix
      - computing biases
    rescaling to factor 1
      - getting the sum of the matrix
        => 1553.816
      - rescaling biases
    iterative correction
      - copying matrix
      - computing biases
    rescaling to factor 1
      - getting the sum of the matrix
        => 1570.990
      - rescaling biases


The two important parameter to define are the window size, the distance
from the diagonal and the delta. - the square size should be 500 kb as
close as possible from the diagonal - the delta is to look for increases
in insulation around a given bin. Should be around 100 kb (in out case
we define it as 200 kb as we are working at 100 kb resolution, and
working with only one bin is a bit to little)

.. code:: ipython3

    wsize = (1, 4)

.. code:: ipython3

    insc1, delta1 = insulation_score(hic_data1, [wsize], resolution=100000, normalize=True, delta=2)
    insc2, delta2 = insulation_score(hic_data2, [wsize], resolution=100000, normalize=True, delta=2)


.. ansi-block::

     - computing insulation in band 1-4
     - computing insulation in band 1-4


.. ansi-block::

    /home/dcastillo/miniconda2/envs/py3_tadbit/lib/python3.7/site-packages/numpy/core/fromnumeric.py:3335: RuntimeWarning: Mean of empty slice.
      out=out, **kwargs)


Once defined the insulation score and the values of delta can be used to
search for borders.

.. code:: ipython3

    borders1 = insulation_to_borders(insc1[wsize], delta1[wsize], min_strength=0.1)
    borders2 = insulation_to_borders(insc2[wsize], delta2[wsize], min_strength=0.1)

Currently the representation is not available in TADbit as for the other
methods, but we can easily plot it:

.. code:: ipython3

    plt.figure(figsize=(10, 4))
    
    plt.subplot(2, 1, 1)
    plt.title('B cell')
    l1 = plt.plot([insc1[(wsize)].get(i, float('nan')) for i in range(max(insc1[(wsize)]))], label='Insulation score')
    l2 = plt.plot([delta1[(wsize)].get(i, float('nan')) for i in range(max(insc1[(wsize)]))],
             alpha=0.3, label='Delta value')
    for b, c in borders1:
        l3 = plt.plot([b] * 2, [-2, -2.3], color='darkgreen', alpha=c, lw=4, label='Border strength')
        
    plt.grid()
    plt.axhline(0, color='k')
    plt.ylim(-2.5, 2)
    plt.xlim(300, 360)
    
    plt.legend(l1 + l2 + l3, [l.get_label() for l in l1 + l2 + l3], frameon=False, bbox_to_anchor=(1.3, 0.6))
    
    plt.subplot(2, 1, 2)
    plt.title('PSC')
    plt.plot([insc2[(wsize)].get(i, float('nan')) for i in range(max(insc2[(wsize)]))])
    plt.plot([delta2[(wsize)].get(i, float('nan')) for i in range(max(insc2[(wsize)]))], alpha=0.3)
    for b, c in borders2:
        plt.plot([b] * 2, [-2, -2.3], color='darkgreen', alpha=c, lw=4)
    plt.grid()
    plt.axhline(0, color='k')
    plt.ylim(-2.5, 2)
    _ = plt.xlim(300, 360)
    plt.tight_layout()



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_65_0.png


Comparison of TAD borders
-------------------------

The TAD borders can be aligned, using a simple reciprocal best hit
strategy:

.. code:: ipython3

    ali = crm.align_experiments(['mouse_B', 'mouse_PSC'], max_dist=reso)

In the plots below, each arc represents a TAD. Between two consecutive
arcs the triangle mark the border. This triangle is colored depending on
the confidence of the TAD border call.

.. code:: ipython3

    ali.draw(ymax=3)



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_70_0.png


.. code:: ipython3

    ali.draw(focus=(1, 350), ymax=3)



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_71_0.png


Statistical significance of the TAD borders alignments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to asses how well two experiments align, or how conserved are
the TAD borders between two experiments, we can compare the overlap
between our experiments with the overlap of simulated random
distributions of TAD borders.

.. code:: ipython3

    ali, stats = crm.align_experiments(['mouse_B', 'mouse_PSC'], randomize=True)

.. code:: ipython3

    print(ali)


.. ansi-block::

    Alignment shown in 100 Kb (2 experiments) (scores: [34m0[0m [34m1[0m [34m2[0m [36m3[0m [0m4[0m [1m5[0m [33m6[0m [33m7[0m [35m8[0m [35m9[0m [31m10[0m)
      mouse_B:|    [34m31[0m| ---- | ---- |    [33m73[0m|    [33m85[0m|   [1m104[0m|   [35m138[0m| ---- |   [0m155[0m|   [0m158[0m|   [34m160[0m|   [1m178[0m|   [33m191[0m|   [33m206[0m|   [33m224[0m| ---- |   [35m270[0m| ---- |   [1m281[0m|   [0m290[0m|   [33m297[0m|   [1m305[0m|   [1m312[0m|   [34m317[0m|   [1m323[0m|   [1m328[0m|   [1m338[0m| ---- |   [33m356[0m| ---- | ---- | ---- |   [1m382[0m|   [0m389[0m| ---- |   [33m407[0m|   [34m410[0m|   [36m419[0m|   [33m454[0m| ---- |   [35m508[0m|   [34m510[0m|   [34m512[0m| ---- |   [36m522[0m|   [36m530[0m|   [1m535[0m|   [1m543[0m| ---- |   [34m552[0m|   [36m561[0m| ---- |   [33m574[0m| ---- |   [0m591[0m|   [33m600[0m|   [1m608[0m|   [0m612[0m|   [33m625[0m|   [33m635[0m| ---- | ---- | ---- |   [1m660[0m| ---- |   [1m673[0m| ---- | ---- | ---- |   [36m692[0m|   [0m700[0m|   [35m731[0m|   [35m751[0m|   [0m761[0m|   [35m789[0m|   [0m798[0m|   [34m801[0m| ---- |   [35m819[0m|   [33m830[0m|   [1m837[0m|   [0m849[0m| ---- |   [1m861[0m| ---- |   [1m870[0m|   [1m877[0m|   [34m880[0m|   [34m883[0m|   [34m889[0m| ---- |   [34m895[0m|   [34m900[0m| ---- |   [34m908[0m| ---- | ---- | ---- | ---- | ---- |   [0m949[0m|   [34m959[0m|   [34m963[0m| ---- |   [34m967[0m|   [0m976[0m| ---- |   [34m986[0m| ---- |  [33m1020[0m|  [1m1027[0m| ---- |  [0m1047[0m|  [34m1051[0m| ---- | ---- | ---- |  [33m1075[0m| ---- |  [34m1084[0m|  [34m1093[0m|  [34m1097[0m| ---- |  [33m1134[0m|  [34m1136[0m|  [33m1154[0m| ---- | ---- |  [0m1169[0m|  [0m1175[0m| ---- |  [33m1211[0m| ---- |  [0m1221[0m|  [1m1228[0m|  [34m1235[0m| ---- |  [33m1257[0m|  [0m1264[0m|  [33m1270[0m|  [34m1275[0m|  [1m1280[0m|  [0m1291[0m|  [0m1298[0m|  [34m1301[0m|  [1m1307[0m|  [33m1314[0m|  [34m1316[0m| ---- |  [1m1326[0m|  [33m1333[0m| ---- | ---- |  [33m1352[0m|  [36m1359[0m|  [33m1369[0m|  [33m1378[0m|  [1m1384[0m|  [33m1393[0m|  [35m1418[0m| ---- |  [34m1428[0m| ---- |  [33m1444[0m|  [34m1448[0m|  [36m1452[0m|  [0m1459[0m| ---- |  [0m1470[0m|  [35m1490[0m| ---- | ---- |  [33m1521[0m|  [1m1528[0m|  [1m1540[0m|  [1m1546[0m| ---- |  [35m1575[0m|  [33m1581[0m| ---- |  [33m1602[0m
    mouse_PSC:|    [34m31[0m|    [33m63[0m|    [33m71[0m|    [34m73[0m|    [1m85[0m|   [36m104[0m|   [33m139[0m|   [1m145[0m| ---- |   [36m158[0m|   [34m160[0m|   [1m179[0m|   [0m192[0m|   [1m206[0m|   [33m223[0m|   [33m256[0m|   [1m270[0m|   [34m273[0m|   [36m281[0m|   [36m290[0m|   [0m297[0m|   [1m305[0m|   [34m311[0m|   [34m317[0m|   [33m323[0m|   [34m329[0m|   [36m338[0m|   [33m344[0m|   [1m356[0m|   [0m362[0m|   [34m370[0m|   [34m376[0m|   [1m382[0m|   [0m389[0m|   [33m405[0m|   [35m407[0m|   [34m410[0m|   [34m418[0m|   [33m454[0m|   [33m489[0m|   [33m508[0m|   [34m510[0m|   [34m512[0m|   [34m514[0m|   [0m522[0m|   [0m530[0m|   [0m535[0m| ---- |   [34m547[0m|   [34m552[0m|   [34m560[0m|   [33m572[0m| ---- |   [36m585[0m|   [34m591[0m| ---- |   [33m607[0m|   [33m612[0m|   [33m625[0m|   [1m635[0m|   [36m640[0m|   [0m648[0m|   [36m653[0m|   [0m660[0m|   [34m663[0m|   [33m674[0m|   [0m681[0m|   [1m687[0m|   [34m690[0m| ---- |   [36m700[0m|   [33m731[0m|   [33m752[0m|   [0m760[0m|   [33m789[0m|   [34m799[0m|   [34m801[0m|   [33m808[0m|   [1m820[0m|   [1m831[0m|   [36m838[0m|   [34m849[0m|   [1m856[0m|   [36m862[0m|   [1m868[0m|   [34m870[0m| ---- |   [34m880[0m|   [34m883[0m|   [34m888[0m|   [34m891[0m| ---- | ---- |   [34m905[0m|   [34m907[0m|   [34m914[0m|   [33m921[0m|   [0m931[0m|   [36m936[0m|   [33m943[0m|   [0m949[0m|   [34m959[0m|   [34m962[0m|   [34m965[0m|   [34m967[0m|   [36m976[0m|   [34m979[0m| ---- |   [34m988[0m|  [33m1019[0m| ---- |  [36m1030[0m|  [34m1047[0m|  [34m1051[0m|  [0m1057[0m|  [34m1060[0m|  [1m1069[0m|  [34m1076[0m|  [34m1082[0m| ---- |  [34m1093[0m| ---- |  [34m1099[0m|  [33m1134[0m|  [34m1136[0m| ---- |  [33m1156[0m|  [36m1163[0m|  [0m1169[0m| ---- |  [34m1177[0m|  [33m1211[0m|  [36m1218[0m| ---- | ---- |  [34m1235[0m|  [1m1243[0m|  [33m1258[0m| ---- |  [1m1271[0m| ---- |  [34m1280[0m|  [1m1292[0m|  [0m1298[0m|  [34m1301[0m|  [33m1307[0m|  [33m1314[0m|  [34m1316[0m|  [0m1319[0m|  [36m1327[0m|  [0m1333[0m|  [33m1339[0m|  [33m1346[0m|  [0m1352[0m|  [0m1358[0m| ---- |  [1m1377[0m|  [36m1385[0m|  [0m1392[0m|  [35m1418[0m|  [36m1425[0m| ---- |  [34m1430[0m|  [1m1444[0m| ---- |  [36m1453[0m| ---- |  [34m1462[0m|  [0m1470[0m| ---- |  [33m1496[0m|  [33m1516[0m|  [34m1521[0m|  [34m1528[0m|  [0m1539[0m|  [36m1546[0m|  [33m1566[0m|  [33m1575[0m| ---- |  [34m1583[0m|  [33m1602[0m
    


This analysis returns an alignment score between 0 and 1 (0: no match,
1: all borders aligned), a p-value (usually equal zero), the proportion
of borders conserved in the second experiment, and the proportion of
borders conserved in the first experiment:

.. code:: ipython3

    stats


.. ansi-block::

    The history saving thread hit an unexpected error (OperationalError('database is locked')).History will not be written to the database.




.. ansi-block::

    (0.4696132596685082, 0.0, 0.872, 0.8980891719745223)



.. code:: ipython3

    print('Alignment score: %.3f, p-value: %.4f\n  proportion of borders of T0 found in T60: %.3f, of T60 in T0 %.3f' % stats)


.. ansi-block::

    Alignment score: 0.470, p-value: 0.0000
      proportion of borders of T0 found in T60: 0.872, of T60 in T0 0.898


Save Chromosome object (with TAD definition)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    crm.save_chromosome('results/fragment/chr3.tdb')

Extra: choosing the best resolution to call TAD borders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TopDom and the methodology based on insulation score are relatively fast
computationally and allow to call TAD borders at very high resolution.
**However** being able to call TAD borders at high resolution does not
mean that we should do it. **As the resolution increases, so does the
noise**.

In order to assess which is the best resolution in order to call TAD
borders, a good strategy is to test the consistency of several
resolutions.

In the example below, we use the methodology based on the insulation
score as it is the fastest (tadbit strategy is almost not usable bellow
20 kb). We compare the number of TAD borders that are shared (plus-minus
one bin) between the two replicates (iPS and B cells).

.. code:: ipython3

    from pytadbit.parsers.hic_parser import load_hic_data_from_bam
    from pytadbit.tadbit import insulation_score, insulation_to_borders

.. code:: ipython3

    base_path = 'results/fragment/{0}_both/03_filtering/valid_reads12_{0}.bam'
    cel1 = 'mouse_B'
    cel2 = 'mouse_PSC'
    borders = {}
    resos = [5000, 10000, 20000, 30000, 40000, 50000, 60000, 80000, 100000, 150000, 200000]

.. code:: ipython3

    for c in ['chr%d' % cs for cs in range(1, 20)] + ['chrX']:
        borders[c] = {}
        for reso in resos:
            hic_data1 = load_hic_data_from_bam(base_path.format(cel1),
                                               resolution=reso,
                                               region=c,
                                               ncpus=8, verbose=False)
            hic_data2 = load_hic_data_from_bam(base_path.format(cel2),
                                               resolution=reso,
                                               region=c,
                                               ncpus=8, verbose=False)
            hic_data1.normalize_hic(silent=True)
            hic_data1.normalize_expected()
            hic_data2.normalize_hic(silent=True)
            hic_data2.normalize_expected()
            wsize = (1, max(2, 500000 // reso))
            delta = max(1, 100000 // reso)
            insc1, delta1 = insulation_score(hic_data1, [wsize], resolution=100000, normalize=True, delta=delta)
            insc2, delta2 = insulation_score(hic_data2, [wsize], resolution=100000, normalize=True, delta=delta)
            borders1 = insulation_to_borders(insc1[wsize], delta1[wsize], min_strength=0.1)
            borders2 = insulation_to_borders(insc2[wsize], delta2[wsize], min_strength=0.1)
            borders[c][reso] = borders1, borders2


.. ansi-block::

     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2
     - computing insulation in band 1-100
     - computing insulation in band 1-100
     - computing insulation in band 1-50
     - computing insulation in band 1-50
     - computing insulation in band 1-25
     - computing insulation in band 1-25
     - computing insulation in band 1-16
     - computing insulation in band 1-16
     - computing insulation in band 1-12
     - computing insulation in band 1-12
     - computing insulation in band 1-10
     - computing insulation in band 1-10
     - computing insulation in band 1-8
     - computing insulation in band 1-8
     - computing insulation in band 1-6
     - computing insulation in band 1-6
     - computing insulation in band 1-5
     - computing insulation in band 1-5
     - computing insulation in band 1-3
     - computing insulation in band 1-3
     - computing insulation in band 1-2
     - computing insulation in band 1-2


We align TAD borders and keep the proportion of borders aligned between
cell types

.. code:: ipython3

    from pytadbit.alignment import align

.. code:: ipython3

    scores = {}
    props1 = {}
    props2 = {}
    for c in borders:
        scores[c] = []
        props1[c] = []
        props2[c] = []
        for reso in resos:
            ali = align([[t[0] for t in b] for b in borders[c][reso]], max_dist=1)
            props1[c].append(ali[0][2])
            props2[c].append(ali[0][3])
            scores[c].append(ali[0][1])

We plot the results, as boxplots to group the values of each
chromosomes:

.. code:: ipython3

    from functools import reduce
    
    plt.figure(figsize=(12, 5))
    bp = plt.boxplot([reduce(lambda x, y: x+ y, 
                     [(props1[c][i], props2[c][i]) for c in props1])
                      for i in range(len(resos))], positions=resos, widths=2000)
    
    plt.plot([sum(m.get_xdata()) / 2 for m in bp['medians']], 
             [0m.get_ydata()[0] for m in bp['medians']], color='grey', alpha=0.5)
    
    plt.xlim(0, 205000)
    plt.xticks(resos, [str(reso / 1000) + 'kb'  for reso in resos], rotation=90)
    plt.ylabel('Proportion of aligned borders\nPSC vs B cell (all chromosomes)')
    plt.xlabel('Resolution at which TAD borders are called')
    plt.grid()
    plt.tight_layout()
    plt.show()



.. image:: ../nbpictures//tutorial_8-Compartments_and_TADs_detection_90_0.png


In the case of these experiments it seems that looking for TAD borders
bellow 50 kb is dangerous, as very few are reproducible. Calling TAD
borders at 100 kb resolution might be here a good idea.
