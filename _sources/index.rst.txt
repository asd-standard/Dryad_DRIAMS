Federated AMR Analysis — DRIAMS Dataset
========================================

Analysis of antimicrobial resistance prediction from MALDI-TOF mass spectra
across four hospital sites (DRIAMS A/B/C/D). Models range from logistic regression
to federated learning with Flower, covering 10 drugs and multiple bacterial species.

.. toctree::
   :maxdepth: 2
   :caption: Analyses

   01. Logistic Regression <01-LogisticAnalysis-Aggregated/index>
   02. MLP Classifier <02-MLPClassifier-Aggregated/index>
   03. Cross-Site Classifier <03-CrossSite-Classifier/index>
   04. Multi-Label MLP <04-Multi-Label-mlp/index>
   05. Random Forest <05-RandomForest-Ceftazidime-Ecoli/index>
    06a. Ceftazidime x E. coli <06a-Ceftazidime-E-coli/index>
   06b. Ceftriaxone x E. coli (Federated) <06b-Ceftriaxone-E-coli/index>
   07. Dedicated Per-Drug Models <07-Dedicated-MLP-Aggregated/index>
   08. Federated MLP / LR / RF <08-Federated-mlp-lr-rf/index>
   Glossary <glossary>
