"""
Compare different summarization approaches
"""
import json
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False


def compare_summaries():
    """Show side-by-side comparison of original findings and summaries"""
    data_dir = Path("C:/Users/sneha/clin-summ-data/data")
    
    # Load radiology data
    test_file = data_dir / "opi" / "test.jsonl"
    with open(test_file, 'r', encoding='utf-8') as f:
        samples = [json.loads(line) for line in f]
    
    if HAS_RICH:
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]Clinical Text Summarization - Comparison View[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
    else:
        print("\n" + "="*80)
        print("Clinical Text Summarization - Comparison View")
        print("="*80 + "\n")
    
    # Show 5 examples with detailed comparison
    for i, sample in enumerate(samples[:5], 1):
        findings = sample.get('inputs', '')
        impression = sample.get('target', '')
        
        # Calculate metrics
        finding_words = findings.split()
        impression_words = impression.split()
        compression = len(finding_words) / max(len(impression_words), 1)
        
        # Extract key terms
        key_terms = []
        for word in impression_words:
            word_clean = word.lower().strip('.,;:')
            if word_clean in findings.lower() and len(word_clean) > 3:
                key_terms.append(word)
        
        if HAS_RICH:
            console.print(f"[bold yellow]Report #{i}[/bold yellow]")
            console.print()
            
            # Create comparison table
            table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
            table.add_column("", style="cyan", width=15)
            table.add_column("Content", style="white", width=60)
            
            table.add_row("[yellow]FINDINGS[/yellow]", findings)
            table.add_row("", "")
            table.add_row("[green]IMPRESSION[/green]", impression)
            table.add_row("", "")
            table.add_row("[cyan]STATS[/cyan]", 
                f"Input: {len(finding_words)} words\n"
                f"Output: {len(impression_words)} words\n"
                f"Compression: {compression:.1f}x\n"
                f"Key terms preserved: {len(key_terms)}")
            
            console.print(table)
            console.print()
            
        else:
            print(f"\n{'─'*80}")
            print(f"REPORT #{i}")
            print('─'*80)
            print(f"\n📋 FINDINGS ({len(finding_words)} words):")
            print(f"   {findings}")
            print(f"\n💡 IMPRESSION ({len(impression_words)} words):")
            print(f"   {impression}")
            print(f"\n📊 METRICS:")
            print(f"   Compression: {compression:.1f}x")
            print(f"   Key terms preserved: {len(key_terms)}")
            print()
    
    # Summary statistics
    total_finding_words = sum(len(s.get('inputs', '').split()) for s in samples)
    total_impression_words = sum(len(s.get('target', '').split()) for s in samples)
    avg_compression = total_finding_words / total_impression_words
    
    if HAS_RICH:
        console.print(Panel(
            f"[bold]Dataset Summary[/bold]\n\n"
            f"Total reports: {len(samples)}\n"
            f"Average compression: {avg_compression:.1f}x\n"
            f"Average finding: {total_finding_words/len(samples):.1f} words\n"
            f"Average impression: {total_impression_words/len(samples):.1f} words",
            title="Overall Statistics",
            border_style="green"
        ))
    else:
        print("="*80)
        print("OVERALL STATISTICS")
        print("="*80)
        print(f"Total reports: {len(samples)}")
        print(f"Average compression: {avg_compression:.1f}x")
        print(f"Average finding: {total_finding_words/len(samples):.1f} words")
        print(f"Average impression: {total_impression_words/len(samples):.1f} words")
        print()


if __name__ == "__main__":
    compare_summaries()
