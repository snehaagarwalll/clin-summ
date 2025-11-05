"""
Simple script to calculate metrics on pre-existing result files
in the data directory (not requiring model generation)
"""

import json
import os
import sys
from evaluate import load
from bert_score import score as bert_score_fn
from rouge_score import rouge_scorer
import nltk

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def calculate_metrics_from_file(result_file):
    """Calculate metrics from a result.jsonl file"""
    
    print(f"\nLoading results from: {result_file}")
    
    # Load data
    with open(result_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    
    print(f"Found {len(data)} samples")
    
    # Extract references and predictions
    references = [item['target'] for item in data]
    predictions = [item['output'] for item in data]
    
    print("\nCalculating metrics...")
    metrics = {}
    
    # 1. BLEU Score
    try:
        print("  - Calculating BLEU...")
        bleu = load("bleu")
        bleu_results = bleu.compute(predictions=predictions, references=references)
        metrics['BLEU'] = bleu_results['bleu']
        print(f"    BLEU: {metrics['BLEU']:.4f}")
    except Exception as e:
        print(f"    BLEU calculation failed: {e}")
    
    # 2. ROUGE Scores
    try:
        print("  - Calculating ROUGE...")
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        rouge_scores = {'rouge1': [], 'rouge2': [], 'rougeL': []}
        
        for ref, pred in zip(references, predictions):
            scores = scorer.score(ref, pred)
            rouge_scores['rouge1'].append(scores['rouge1'].fmeasure)
            rouge_scores['rouge2'].append(scores['rouge2'].fmeasure)
            rouge_scores['rougeL'].append(scores['rougeL'].fmeasure)
        
        metrics['ROUGE-1'] = sum(rouge_scores['rouge1']) / len(rouge_scores['rouge1'])
        metrics['ROUGE-2'] = sum(rouge_scores['rouge2']) / len(rouge_scores['rouge2'])
        metrics['ROUGE-L'] = sum(rouge_scores['rougeL']) / len(rouge_scores['rougeL'])
        
        print(f"    ROUGE-1: {metrics['ROUGE-1']:.4f}")
        print(f"    ROUGE-2: {metrics['ROUGE-2']:.4f}")
        print(f"    ROUGE-L: {metrics['ROUGE-L']:.4f}")
    except Exception as e:
        print(f"    ROUGE calculation failed: {e}")
    
    # 3. BERTScore
    try:
        print("  - Calculating BERTScore (this may take a minute)...")
        P, R, F1 = bert_score_fn(predictions, references, lang='en', rescale_with_baseline=True)
        metrics['BERTScore'] = F1.mean().item()
        print(f"    BERTScore: {metrics['BERTScore']:.4f}")
    except Exception as e:
        print(f"    BERTScore calculation failed: {e}")
    
    return metrics

def main():
    # Check for command line argument
    if len(sys.argv) > 1:
        result_file = sys.argv[1]
    else:
        # Default to the opi result file
        result_file = r"C:\Users\sneha\clin-summ-data\data\opi\result.jsonl"
    
    if not os.path.exists(result_file):
        print(f"Error: File not found: {result_file}")
        print(f"\nUsage: python {sys.argv[0]} <path_to_result.jsonl>")
        print(f"\nAvailable result files:")
        data_dir = r"C:\Users\sneha\clin-summ-data\data"
        for dataset in ['opi', 'chq', 'd2n']:
            dataset_result = os.path.join(data_dir, dataset, 'result.jsonl')
            if os.path.exists(dataset_result):
                print(f"  - {dataset_result}")
        return
    
    # Calculate metrics
    metrics = calculate_metrics_from_file(result_file)
    
    # Print summary
    print("\n" + "="*60)
    print("METRICS SUMMARY")
    print("="*60)
    for metric_name, metric_value in metrics.items():
        print(f"{metric_name:15s}: {metric_value:.4f}")
    print("="*60)

if __name__ == "__main__":
    main()
