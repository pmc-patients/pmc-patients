# PMC-Patients

PMC-Patients is a first-of-its-kind dataset consisting of 167k patient summaries extracted from case reports in PubMed Central (PMC), 3.1M patient-article relevance and 293k patient-patient similarity annotations defined by PubMed citation graph.

Based on PMC-Patients, we define two tasks to benchmark Retrieval-based Clinical Decision Support (ReCDS) systems: Patient-to-Article Retrieval (PAR) and Patient-to-Patient Retrieval (PPR).
For details, please refer to [our paper](https://arxiv.org/abs/2202.13876).

## Download Data & Data Format

You are free to download the dataset via either [Figshare](https://figshare.com/collections/PMC-Patients/6723465) or [Hugginface](https://huggingface.co/zhengyun21) (including patient summaries and training/dev/test data for ReCDS benchmark) without any data usage agreement. 

After downloading, please unzip the data and keep the `datasets` folder in this root directory if you are using the provided evaluation code. Here are some details about data format:

## PMC-Patients Dataset

The core file of our dataset, containing the patient summaries, demographics, and relational annotations.

### PMC-Patients.json
Patient summaries are presented as a `json` file, which is a list of dictionaries with the following keys:
- `patient_id`: string. A continuous id of patients, starting from 0.
- `patient_uid`: string. Unique ID for each patient, with format PMID-x, where PMID is the PubMed Identifier of source article of the note and x denotes index of the note in source article.
- `PMID`: string. PMID for source article.
- `file_path`: string. File path of xml file of source article.
- `title`: string. Source article title.
- `patient`: string. Patient note.
- `age`: list of tuples. Each entry is in format `(value, unit)` where value is a float number and unit is in 'year', 'month', 'week', 'day' and 'hour' indicating age unit. For example, `[[1.0, 'year'], [2.0, 'month']]` indicating the patient is a one-year- and two-month-old infant.
- `gender`: 'M' or 'F'. Male or Female.
- `relevant_articles`: dict. The key is PMID of the relevant articles and the corresponding value is its relevance score (2 or 1 as defined in the ``Methods'' section).
- `similar_patients`: dict. The key is patient_uid of the similar patients and the corresponding value is its similarity score (2 or 1 as defined in the ``Methods'' section).


## PMC-Patients ReCDS Benchmark

The PMC-Patients ReCDS benchmark is presented as retrieval tasks and the data format is the same as [BEIR](https://github.com/beir-cellar/beir) benchmark. 
To be specific, there are queries, corpus, and qrels (annotations).

### Queries

ReCDS-PAR and ReCDS-PPR tasks share the same query patient set and dataset split.
For each split (train, dev, and test), queries are stored a `jsonl` file that contains a list of dictionaries, each with two fields: 
- `_id`: unique query identifier represented by patient_uid.
- `text`: query text represented by patient summary text.

### Corpus

Corpus is shared by different splits. For ReCDS-PAR, the corpus contains 11.7M PubMed articles, and for ReCDS-PPR, the corpus contains 155.2k reference patients from PMC-Patients. The corpus is also presented by a `jsonl` file that contains a list of dictionaries with three fields:
- `_id`:  unique document identifier represented by PMID of the PubMed article in ReCDS-PAR, and patient_uid of the candidate patient in ReCDS-PPR.
- `title`: : title of the article in ReCDS-PAR, and empty string in ReCDS-PPR.
- `text`: abstract of the article in ReCDS-PAR, and patient summary text in ReCDS-PPR.

### Qrels

Qrels are TREC-style retrieval annotation files in `tsv` format.
A qrels file contains three tab-separated columns, i.e. the query identifier, corpus identifier, and score in this order. The scores (2 or 1) indicate the relevance level in ReCDS-PAR or similarity level in ReCDS-PPR.

Note that the qrels may not be the same as `relevant_articles` and `similar_patients` in `PMC-Patients.json` due to dataset split (see our manuscript for details).


## Evaluation & Submission

We provide evaluation code based on BEIR, so you can simply run your model and dump the retrieval results as a `json` file.
The results should be stored as:
```
{
    "q1":{
        "doc1": score1,
        "doc2": score2,
        ...
    },
    "q2":{
        "doc3": score3,
        "doc4": score4,
        ...
    },
    ...
}
```
where `q1` is the query id, `doc1` is the document id, and `score1` is the relevance score returned by any model which doesn't need to be normalized. A real example of PAR results in such format looks like:
```
{
    "3996084-1":{
        "8821503": 360.56292724609375,
        "15793714": 359.9751892089844,
        ...
    },
    "6250493-1":{
        "27524922": 340.984375,
        "16650177": 340.9232177734375,
        ...
    },
    ...
}
```

Then simply run the following code to get metrics for your model:
```
python evaluation.py --task PPR --split test --result_path YOUR_RESULT_PATH
```
where `task` parameter should be "PAR" or "PPR" and `split` parameter indicates running evaluation for "train", "dev", or "test" split.

You can also copy the code in `evaluation.py` and integrate the evaluation process into your training pipeline since it can be tedious and a waste of disk space to store retrieval results every time.
Just make sure you load the correct data and keep your results in the above format.

To submit to our [leaderboard](https://pmc-patients.github.io/), please send an email that contains the retrieval scores and a brief description of the system to Zhengyun Zhao via zhengyun21@mails.tsinghua.edu.cn.

## Dataset Collection & Baseline Retrievers
If you are interested in the dataset collection process or reproducing the baseline retrievers in our paper, please refer to our [code repo](https://github.com/zhao-zy15/PMC-Patients).


## Citation
If you find PMC-Patients helpful in your research, please cite our work by:
```
@misc{zhao2023pmcpatients,
      title={PMC-Patients: A Large-scale Dataset of Patient Summaries and Relations for Benchmarking Retrieval-based Clinical Decision Support Systems}, 
      author={Zhengyun Zhao and Qiao Jin and Fangyuan Chen and Tuorui Peng and Sheng Yu},
      year={2023},
      eprint={2202.13876},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
