"""
Simple script to view clinical text summarization results
"""
import json
import os
from pathlib import Path

def main():
    # Path to the data
    data_dir = Path("C:/Users/sneha/clin-summ-data/data")
    
    # Available datasets
    datasets = {
        '1': ('opi', 'Open-i Radiology Reports'),
        '2': ('d2n', 'Doctor-Patient Dialogues'),
        '3': ('chq', 'Consumer Health Questions')
    }
    
    print("=" * 70)
    print("Clinical Text Summarization - View Results")
    print("=" * 70)
    print("\nAvailable datasets:")
    for key, (code, name) in datasets.items():
        print(f"  {key}. {name} ({code})")
    
    choice = input("\nChoose a dataset (1-3): ").strip()
    
    if choice not in datasets:
        print("Invalid choice!")
        return
    
    dataset_code, dataset_name = datasets[choice]
    
    # Load test data
    test_file = data_dir / dataset_code / "test.jsonl"
    
    if not test_file.exists():
        print(f"\nError: {test_file} not found!")
        return
    
    print(f"\n{'=' * 70}")
    print(f"Dataset: {dataset_name}")
    print(f"{'=' * 70}\n")
    
    # Read and display samples
    with open(test_file, 'r', encoding='utf-8') as f:
        samples = [json.loads(line) for line in f]
    
    print(f"Total samples: {len(samples)}\n")
    
    num_to_show = min(5, len(samples))
    print(f"Showing first {num_to_show} samples:\n")
    
    for i, sample in enumerate(samples[:num_to_show], 1):
        print(f"\n{'─' * 70}")
        print(f"Sample #{i}")
        print(f"{'─' * 70}")
        
        # Display based on dataset type
        input_text = sample.get('inputs', sample.get('input', 'N/A'))
        target_text = sample.get('target', 'N/A')
        
        if dataset_code == 'opi':
            print(f"\n📋 RADIOLOGY FINDINGS (Input):")
            print(f"{input_text[:400]}")
            if len(input_text) > 400:
                print("...")
            print(f"\n💡 IMPRESSION (Summary):")
            print(f"{target_text}")
            
        elif dataset_code == 'd2n':
            print(f"\n💬 DOCTOR-PATIENT DIALOGUE (Input):")
            print(f"{input_text[:400]}")
            if len(input_text) > 400:
                print("...")
            print(f"\n📝 ASSESSMENT & PLAN (Summary):")
            if len(target_text) > 300:
                print(f"{target_text[:300]}...")
            else:
                print(f"{target_text}")
            
        elif dataset_code == 'chq':
            print(f"\n❓ PATIENT QUESTION (Input):")
            print(f"{input_text}")
            print(f"\n✅ SUMMARIZED QUESTION:")
            print(f"{target_text}")
    
    # Show basic statistics
    print(f"\n\n{'=' * 70}")
    print("Basic Statistics")
    print(f"{'=' * 70}")
    
    # Calculate average lengths using 'inputs' and 'target' keys
    input_lengths = [len(s.get('inputs', s.get('input', '')).split()) for s in samples]
    target_lengths = [len(s.get('target', '').split()) for s in samples]
    
    print(f"\nTotal Samples: {len(samples)}")
    print(f"Average Input Length: {sum(input_lengths)/len(input_lengths):.1f} words")
    print(f"Average Summary Length: {sum(target_lengths)/len(target_lengths):.1f} words")
    
    if sum(target_lengths) > 0:
        print(f"Compression Ratio: {sum(input_lengths)/sum(target_lengths):.1f}x")
    else:
        print(f"Compression Ratio: N/A")
    
    print("\n" + "=" * 70)
    print("Done!")
    print("=" * 70)

if __name__ == "__main__":
    main()
