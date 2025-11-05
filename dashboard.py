"""
Interactive Dashboard for Clinical Text Summarization
Shows beautiful visualizations, metrics, and patient report analysis
"""
import json
import os
from pathlib import Path
from collections import Counter
import re

# Try to import rich for beautiful output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.progress import Progress
    from rich import box
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

console = Console() if HAS_RICH else None


def extract_medical_terms(text):
    """Extract key medical terms from text"""
    # Common medical findings
    conditions = [
        'pneumonia', 'edema', 'effusion', 'consolidation', 'atelectasis',
        'cardiomegaly', 'pneumothorax', 'nodule', 'mass', 'fracture',
        'infiltrate', 'opacity', 'calcification', 'granuloma', 'emphysema',
        'hypertension', 'diabetes', 'asthma', 'copd', 'cancer'
    ]
    
    # Anatomy terms
    anatomy = [
        'heart', 'lung', 'chest', 'cardiac', 'pulmonary', 'mediastinal',
        'pleural', 'thorax', 'right', 'left', 'upper', 'lower', 'lobe'
    ]
    
    # Status terms
    status = ['normal', 'abnormal', 'acute', 'chronic', 'stable', 'improved', 
              'worsened', 'negative', 'positive', 'clear', 'unremarkable']
    
    text_lower = text.lower()
    
    found = {
        'conditions': [c for c in conditions if c in text_lower],
        'anatomy': [a for a in anatomy if a in text_lower],
        'status': [s for s in status if s in text_lower]
    }
    
    return found


def analyze_radiology_reports(samples):
    """Analyze radiology reports for insights"""
    all_findings = []
    all_impressions = []
    all_conditions = []
    all_anatomy = []
    all_status = []
    
    for sample in samples:
        findings = sample.get('inputs', '')
        impression = sample.get('target', '')
        
        all_findings.append(findings)
        all_impressions.append(impression)
        
        # Extract medical terms
        terms = extract_medical_terms(findings + ' ' + impression)
        all_conditions.extend(terms['conditions'])
        all_anatomy.extend(terms['anatomy'])
        all_status.extend(terms['status'])
    
    # Count frequencies
    condition_freq = Counter(all_conditions).most_common(10)
    anatomy_freq = Counter(all_anatomy).most_common(10)
    status_freq = Counter(all_status).most_common(5)
    
    # Check for normal vs abnormal
    normal_count = sum(1 for imp in all_impressions if 'no acute' in imp.lower() or 'normal' in imp.lower() or 'negative' in imp.lower())
    abnormal_count = len(all_impressions) - normal_count
    
    return {
        'total': len(samples),
        'normal': normal_count,
        'abnormal': abnormal_count,
        'conditions': condition_freq,
        'anatomy': anatomy_freq,
        'status': status_freq,
        'avg_finding_len': sum(len(f.split()) for f in all_findings) / len(all_findings),
        'avg_impression_len': sum(len(i.split()) for i in all_impressions) / len(all_impressions),
    }


def analyze_health_questions(samples):
    """Analyze health questions for insights"""
    all_questions = []
    all_summaries = []
    topics = []
    
    for sample in samples:
        question = sample.get('inputs', '')
        summary = sample.get('target', '')
        
        all_questions.append(question)
        all_summaries.append(summary)
        
        # Extract topics (simple keyword extraction)
        question_lower = question.lower()
        if any(word in question_lower for word in ['medication', 'drug', 'pill', 'prescription']):
            topics.append('Medication')
        if any(word in question_lower for word in ['pain', 'hurt', 'ache']):
            topics.append('Pain')
        if any(word in question_lower for word in ['treatment', 'therapy', 'cure']):
            topics.append('Treatment')
        if any(word in question_lower for word in ['side effect', 'adverse', 'reaction']):
            topics.append('Side Effects')
        if any(word in question_lower for word in ['test', 'diagnosis', 'screen']):
            topics.append('Diagnosis')
    
    topic_freq = Counter(topics).most_common(5)
    
    return {
        'total': len(samples),
        'topics': topic_freq,
        'avg_question_len': sum(len(q.split()) for q in all_questions) / len(all_questions),
        'avg_summary_len': sum(len(s.split()) for s in all_summaries) / len(all_summaries),
    }


def print_with_rich(data_dir, dataset_code, dataset_name):
    """Print beautiful dashboard with rich library"""
    # Load data
    test_file = data_dir / dataset_code / "test.jsonl"
    with open(test_file, 'r', encoding='utf-8') as f:
        samples = [json.loads(line) for line in f]
    
    # Clear screen
    console.clear()
    
    # Title
    console.print("\n")
    console.print(Panel.fit(
        f"[bold cyan]Clinical Text Summarization Dashboard[/bold cyan]\n"
        f"[yellow]{dataset_name}[/yellow]",
        border_style="cyan"
    ))
    
    # Statistics
    if dataset_code == 'opi':
        stats = analyze_radiology_reports(samples)
        
        # Overview table
        table = Table(title="📊 Overview Statistics", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Reports", str(stats['total']))
        table.add_row("Normal Findings", f"{stats['normal']} ({stats['normal']/stats['total']*100:.1f}%)")
        table.add_row("Abnormal Findings", f"{stats['abnormal']} ({stats['abnormal']/stats['total']*100:.1f}%)")
        table.add_row("Avg Finding Length", f"{stats['avg_finding_len']:.1f} words")
        table.add_row("Avg Impression Length", f"{stats['avg_impression_len']:.1f} words")
        table.add_row("Compression Ratio", f"{stats['avg_finding_len']/stats['avg_impression_len']:.1f}x")
        
        console.print(table)
        console.print()
        
        # Top conditions
        if stats['conditions']:
            table2 = Table(title="🏥 Most Common Conditions", box=box.ROUNDED)
            table2.add_column("Condition", style="yellow")
            table2.add_column("Count", style="green", justify="right")
            table2.add_column("Percentage", style="cyan", justify="right")
            
            for condition, count in stats['conditions'][:5]:
                pct = (count / stats['total']) * 100
                table2.add_row(condition.title(), str(count), f"{pct:.1f}%")
            
            console.print(table2)
            console.print()
        
        # Anatomy
        if stats['anatomy']:
            table3 = Table(title="🫁 Most Referenced Anatomy", box=box.ROUNDED)
            table3.add_column("Body Part", style="yellow")
            table3.add_column("Mentions", style="green", justify="right")
            
            for anatomy, count in stats['anatomy'][:5]:
                table3.add_row(anatomy.title(), str(count))
            
            console.print(table3)
            console.print()
    
    elif dataset_code == 'chq':
        stats = analyze_health_questions(samples)
        
        table = Table(title="📊 Overview Statistics", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Questions", str(stats['total']))
        table.add_row("Avg Question Length", f"{stats['avg_question_len']:.1f} words")
        table.add_row("Avg Summary Length", f"{stats['avg_summary_len']:.1f} words")
        table.add_row("Compression Ratio", f"{stats['avg_question_len']/stats['avg_summary_len']:.1f}x")
        
        console.print(table)
        console.print()
        
        # Topics
        if stats['topics']:
            table2 = Table(title="📋 Question Topics", box=box.ROUNDED)
            table2.add_column("Topic", style="yellow")
            table2.add_column("Count", style="green", justify="right")
            table2.add_column("Percentage", style="cyan", justify="right")
            
            for topic, count in stats['topics']:
                pct = (count / stats['total']) * 100
                table2.add_row(topic, str(count), f"{pct:.1f}%")
            
            console.print(table2)
            console.print()
    
    # Sample reports
    console.print(Panel("[bold]Sample Reports[/bold]", style="magenta"))
    
    for i, sample in enumerate(samples[:3], 1):
        console.print(f"\n[bold cyan]Sample #{i}[/bold cyan]")
        console.print(Panel(
            f"[yellow]Input:[/yellow]\n{sample.get('inputs', 'N/A')[:200]}...\n\n"
            f"[green]Summary:[/green]\n{sample.get('target', 'N/A')}",
            border_style="blue"
        ))


def print_simple(data_dir, dataset_code, dataset_name):
    """Print simple dashboard without rich library"""
    test_file = data_dir / dataset_code / "test.jsonl"
    with open(test_file, 'r', encoding='utf-8') as f:
        samples = [json.loads(line) for line in f]
    
    print("\n" + "="*70)
    print(f"  CLINICAL TEXT SUMMARIZATION DASHBOARD")
    print(f"  {dataset_name}")
    print("="*70 + "\n")
    
    if dataset_code == 'opi':
        stats = analyze_radiology_reports(samples)
        
        print("📊 OVERVIEW STATISTICS")
        print("-" * 70)
        print(f"  Total Reports:         {stats['total']}")
        print(f"  Normal Findings:       {stats['normal']} ({stats['normal']/stats['total']*100:.1f}%)")
        print(f"  Abnormal Findings:     {stats['abnormal']} ({stats['abnormal']/stats['total']*100:.1f}%)")
        print(f"  Avg Finding Length:    {stats['avg_finding_len']:.1f} words")
        print(f"  Avg Impression Length: {stats['avg_impression_len']:.1f} words")
        print(f"  Compression Ratio:     {stats['avg_finding_len']/stats['avg_impression_len']:.1f}x")
        print()
        
        if stats['conditions']:
            print("🏥 MOST COMMON CONDITIONS")
            print("-" * 70)
            for i, (condition, count) in enumerate(stats['conditions'][:5], 1):
                pct = (count / stats['total']) * 100
                print(f"  {i}. {condition.title():.<40} {count:>3} ({pct:.1f}%)")
            print()
        
        if stats['anatomy']:
            print("🫁 MOST REFERENCED ANATOMY")
            print("-" * 70)
            for i, (anatomy, count) in enumerate(stats['anatomy'][:5], 1):
                print(f"  {i}. {anatomy.title():.<40} {count:>3}")
            print()
    
    elif dataset_code == 'chq':
        stats = analyze_health_questions(samples)
        
        print("📊 OVERVIEW STATISTICS")
        print("-" * 70)
        print(f"  Total Questions:       {stats['total']}")
        print(f"  Avg Question Length:   {stats['avg_question_len']:.1f} words")
        print(f"  Avg Summary Length:    {stats['avg_summary_len']:.1f} words")
        print(f"  Compression Ratio:     {stats['avg_question_len']/stats['avg_summary_len']:.1f}x")
        print()
        
        if stats['topics']:
            print("📋 QUESTION TOPICS")
            print("-" * 70)
            for i, (topic, count) in enumerate(stats['topics'], 1):
                pct = (count / stats['total']) * 100
                print(f"  {i}. {topic:.<40} {count:>3} ({pct:.1f}%)")
            print()
    
    print("📄 SAMPLE REPORTS")
    print("=" * 70)
    
    for i, sample in enumerate(samples[:3], 1):
        print(f"\n  Sample #{i}")
        print("  " + "-" * 68)
        print(f"  INPUT: {sample.get('inputs', 'N/A')[:150]}...")
        print(f"  SUMMARY: {sample.get('target', 'N/A')}")
        print()


def main():
    data_dir = Path("C:/Users/sneha/clin-summ-data/data")
    
    datasets = {
        '1': ('opi', 'Open-i Radiology Reports'),
        '2': ('chq', 'Consumer Health Questions'),
        '3': ('d2n', 'Doctor-Patient Dialogues')
    }
    
    if HAS_RICH:
        console.print("\n[bold cyan]Clinical Text Summarization - Interactive Dashboard[/bold cyan]\n")
        console.print("Available datasets:")
        for key, (code, name) in datasets.items():
            console.print(f"  [yellow]{key}[/yellow]. {name} ({code})")
    else:
        print("\n" + "="*70)
        print("Clinical Text Summarization - Interactive Dashboard")
        print("="*70)
        print("\nAvailable datasets:")
        for key, (code, name) in datasets.items():
            print(f"  {key}. {name} ({code})")
    
    choice = input("\nChoose a dataset (1-3): ").strip()
    
    if choice not in datasets:
        print("Invalid choice!")
        return
    
    dataset_code, dataset_name = datasets[choice]
    test_file = data_dir / dataset_code / "test.jsonl"
    
    if not test_file.exists():
        print(f"\nError: {test_file} not found!")
        return
    
    if HAS_RICH:
        print_with_rich(data_dir, dataset_code, dataset_name)
    else:
        print_simple(data_dir, dataset_code, dataset_name)
    
    print("\n" + "="*70)
    print("Dashboard complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
