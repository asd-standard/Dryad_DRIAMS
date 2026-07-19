Federated AMR Analysis — DRIAMS Dataset
========================================

Analysis of antimicrobial resistance prediction from MALDI-TOF mass spectra
across four hospital sites (DRIAMS A/B/C/D). Models range from logistic regression
to federated learning with Flower, covering 10 drugs and multiple bacterial species.

.. toctree::
   :maxdepth: 2
   :caption: Analyses

   01. Logistic Regression <01-LogisticAnalysis-Aggregated/Docs/index>
   02. MLP Classifier <02-MLPClassifier-Aggregated/Docs/index>
   03. Cross-Site Classifier <03-CrossSite-Classifier/Docs/index>
   04. Multi-Label MLP <04-Multi-Label-mlp/Docs/index>
   05. Random Forest <05-RandomForest-Ceftazidime-Ecoli/Docs/index>
    06a. Ceftazidime x E. coli <06a-Ceftazidime-E-coli/Docs/index>
   06b. Ceftriaxone x E. coli (Federated) <06b-Ceftriaxone-E-coli/Docs/index>
   07. Dedicated Per-Drug Models <07-Dedicated-MLP-Aggregated/Docs/index>
   08. Federated MLP / LR / RF <08-Federated-mlp-lr-rf/Docs/index>
   Glossary <glossary>
