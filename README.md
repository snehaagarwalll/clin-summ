# Clinical Text Summarization by Adapting LLMs | Nature Medicine

<img src='data/overview.png'/>

---

## 🆕 **Interactive Dashboards & Visualization Tools**

Explore the medical text data with beautiful visualizations:
- 📊 **`dashboard.py`** - Interactive dashboard with medical insights, condition frequencies, and statistics
- 📄 **`view_results.py`** - Simple data browser for radiology reports, health questions, and dialogues
- 🔍 **`compare_results.py`** - Side-by-side comparison of findings vs impressions

**Try it now:** `python dashboard.py` (no setup required!)


---


## Datasets
We use six pre-existing open-source datasets which are publicly accessible at the sources cited in our manuscript. Additionally, for datasets which do not require PhysioNet access, we provide our versions in `data/`: 
- `opi`: Open-i (radiology reports)
- `chq`: MeQSum (patient/consumer health questions)
- `d2n`: ACI-Bench (dialogue)

## Models
In addition to proprietary models GPT-3.5 and GPT-4, we adapt the following open-source models available from HuggingFace:
- [FLAN-T5](https://huggingface.co/google/flan-t5-xl)
- [FLAN-UL2](https://huggingface.co/google/flan-ul2)
- [Alpaca](https://huggingface.co/chavinlo/alpaca-native)
- [Med-Alpaca](https://huggingface.co/medalpaca/medalpaca-7b)
- [Vicuna](https://huggingface.co/AlekseyKorshuk/vicuna-7b)
- [Llama-2](https://huggingface.co/meta-llama/Llama-2-7b-hf)

## Code

### Quick Start

**New to this project? Try the interactive dashboard first!**

```bash
# View beautiful statistics and medical insights (no setup required)
python dashboard.py

# Browse data samples
python view_results.py

# Compare findings vs summaries side-by-side
python compare_results.py
```

---

### Set-up

#### Option 1: Using Conda (Original Method)
```bash
conda env create -f env.yml
conda activate clin-summ 
```

#### Option 2: Using Python venv (Windows/No Conda)
```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or: source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run automated setup
python setup_project.py
```

The setup will:
1. Create a project directory for data and models
2. Copy data to the project directory
3. Configure `src/constants.py` with the correct paths

**Manual Configuration** (if needed):
- Edit `src/constants.py` and set `DIR_PROJECT` to your desired location
- For OpenAI models, add your Azure `RESOURCE` and `API_KEY` in `src/constants.py`

---

### Usage

#### 🎨 **Interactive Tools** (Recommended for exploration)

```bash
# Interactive dashboard with statistics and medical insights
python dashboard.py
# Shows: condition frequencies, normal vs abnormal rates, compression metrics

# Simple data viewer
python view_results.py
# Browse raw medical text and summaries

# Comparison tool
python compare_results.py
# Side-by-side analysis of findings vs impressions
```

#### 🤖 **Run AI Models**

**Open-source models:**
```bash
# Small model (fast download, ~1GB)
python src/run.py --model flan-t5-base --case_id 0 --dataset opi --n_samples 5 --is_demo

# Larger model (better quality, ~3GB)
python src/run.py --model flan-t5-large --case_id 0 --dataset opi --n_samples 5 --is_demo

# With in-context learning (4 examples)
python src/run.py --model flan-t5-base --case_id 12 --dataset chq --n_samples 5 --is_demo
```

**OpenAI models** (requires Azure OpenAI):
```bash
python api/main.py
# Configure Azure credentials in src/constants.py first
```

#### 📊 **Calculate Metrics**

```bash
python src/calc_metrics.py --model flan-t5-base --case_id 0 --dataset opi --n_samples 999
```

#### 🔧 **Advanced Scripts**

- `./main.sh`: Fine-tune open-source models (Linux/Mac/WSL)
- `python src/train.py`: Fine-tune with QLora
- `python src/gen_faiss_idx.py`: Generate nearest neighbor indices for in-context learning
- `src/UMLSScorer.py`: MEDCON metric (requires [UMLS license](https://www.nlm.nih.gov/research/umls/index.html))

---

### Available Models

**Open-source** (via HuggingFace):
- `flan-t5-base` - 250M params (~1GB, fast)
- `flan-t5-large` - 780M params (~3GB, good balance)
- `flan-t5-xl` - 3B params (~11GB, best quality)
- `flan-ul2`, `vicuna-7b`, `alpaca-7b`, `med-alpaca-7b`, `llama2-7b`, `llama2-13b`

**Proprietary** (via Azure OpenAI):
- `gpt-35` (GPT-3.5)
- `gpt-4`

---

### Datasets

Three datasets are included in `data/`:
- **`opi`**: 343 radiology reports (Open-i chest X-rays)
- **`chq`**: 150 consumer health questions (MeQSum)
- **`d2n`**: 100 doctor-patient dialogues (ACI-Bench)

**Dataset Statistics:**
- Radiology: 32 words → 8 words (3.8x compression)
- Questions: 66 words → 11 words (6.2x compression)
- Dialogues: Full conversations → 158-word treatment plans

---

### Key Features

✅ **Interactive dashboards** with medical insights  
✅ **Multiple model sizes** (fast to high-quality)  
✅ **Three medical domains** (radiology, questions, dialogues)  
✅ **In-context learning** support (0-64 examples)  
✅ **Fine-tuning** with QLora  
✅ **Comprehensive metrics** (BLEU, ROUGE, BERTScore)  
✅ **Windows support** without conda  

---

### Quick Reference

| Task | Command |
|------|---------|
| **View dashboard** | `python dashboard.py` |
| **Run small model** | `python src/run.py --model flan-t5-base --case_id 0 --dataset opi --n_samples 5 --is_demo` |
| **Calculate metrics** | `python src/calc_metrics.py --model MODEL --case_id ID --dataset DATASET --n_samples 999` |
| **Setup project** | `python setup_project.py` |

For detailed guides, see:
- [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) - Interactive tools
- [HOW_TO_USE.md](HOW_TO_USE.md) - Complete usage guide
- [QUICKSTART.md](QUICKSTART.md) - Step-by-step instructions

## Citation

```
@article{vanveen2024clinical,
  title={Adapted Large Language Models Can Outperform Medical Experts in Clinical Text Summarization},
  author={Van Veen, Dave and Van Uden, Cara and Blankemeier, Louis and Delbrouck, Jean-Benoit and Aali, Asad and Bluethgen, Christian and Pareek, Anuj and Polacin, Malgorzata and Collins, William and Ahuja, Neera and Langlotz, Curtis P. and Hom, Jason and Gatidis, Sergios and Pauly, John and Chaudhari, Akshay S.},
  journal={Nature Medicine},
  year={2024},
  doi={10.1038/s41591-024-02855-5},
  url={https://doi.org/10.1038/s41591-024-02855-5},
  published={27 February 2024}
}
```

## License

- `src/UMLSScorer.py` requires a [UMLS license](https://www.nlm.nih.gov/research/umls/index.html).
- The remainder of this project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
