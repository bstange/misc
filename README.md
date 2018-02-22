# misc

### FHIR-HL7-Codesets.py
- reads FHIR and HL7 codesets and flattens for use or DBs

### PPT_Dendrogram.py
- Reads all powerpoints in a directory, recursively and stores content in a dict
- Runs a BOW, TFIDF distance matrix and applies hierarchical clustering.  Dendrogram png is output.

### SAA.r
- Standardizes jaggad timeseries to a defined length
- Clusters individual timeseries together for further analysis/modelling

#### sparse_svd_class.py
- Python class that takes in *long*, triplet data and performs dimensionality reduction without ever fully specifying the matrix
- some helper methods for investigating the original components that are aggregated into the new features
