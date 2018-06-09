===============================
RunDMCMC
===============================

.. image:: https://api.codacy.com/project/badge/Grade/8c914b8ed49144e0b68a920beadf89a2
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/msarahan/RunDMCMC?utm_source=github.com&utm_medium=referral&utm_content=gerrymandr/RunDMCMC&utm_campaign=badger


.. image:: https://circleci.com/gh/gerrymandr/RunDMCMC.svg?style=svg
    :target: https://circleci.com/gh/gerrymandr/RunDMCMC
.. image:: https://codecov.io/gh/gerrymandr/RunDMCMC/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/gerrymandr/RunDMCMC
.. image:: https://api.codacy.com/project/badge/Grade/b02dfe3d778b40f3890d228889feee52
   :target: https://www.codacy.com/app/msarahan/RunDMCMC?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=gerrymandr/RunDMCMC&amp;utm_campaign=Badge_Grade


This code implements Monte-Carlo exploration of districting plans, exploring the
space around an initial districting plan to give some idea of the degree of
gerrymandering. It is a Python rewrite of the chain C++ program (https://github.com/gerrymandr/cfp_mcmc), originally by
Maria Chikina, Alan Frieze and Wesley Pegden, for their paper, "Assessing
significance in a Markov chain without mixing" (http://www.pnas.org/content/114/11/2860)
