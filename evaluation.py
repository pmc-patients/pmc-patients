import json
import argparse
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.datasets.data_loader import GenericDataLoader


parser = argparse.ArgumentParser()
parser.add_argument(
    "--task",
    choices = ["PPR", "PAR"],
    type = str,
    required = True,
    help = "Which task to evaluate, PAR or PPR."
)
parser.add_argument(
    "--split",
    choices = ["train", "dev", "test"],
    type = str,
    required = True,
    help = "Which split to evaluate, train, dev, or test."
)
parser.add_argument(
    "--result_path",
    type = str,
    required = True,
    help = "The path to store results to be evaluated."
)
args = parser.parse_args()

corpus_path = f"./datasets/{args.task}/{args.task}_corpus.jsonl"
query_path = f"./datasets/queries/{args.split}_queries.jsonl"
qrels_path = f"./datasets/{args.task}/{args.task}_{args.split}_qrels.tsv"
corpus, queries, qrels = GenericDataLoader(
    corpus_file=corpus_path, 
    query_file=query_path, 
    qrels_file=qrels_path).load_custom()

results = json.load(open(args.result_path, "r"))

evaluation = EvaluateRetrieval()
metrics = evaluation.evaluate(qrels, results, [10, 1000])
mrr = evaluation.evaluate_custom(qrels, results, [len(corpus)], metric="mrr")
scores = {'MRR': mrr[f'MRR@{len(corpus)}'], 'P@10': metrics[3]['P@10'], \
    'NDCG@10': metrics[0]['NDCG@10'], "R@1k": metrics[2]['Recall@1000']}
print(scores)