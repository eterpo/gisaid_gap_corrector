# GISAID Gap Corrector

**GISAID Gap Corrector** is a Python-based tool designed for editing genomic FASTA sequences by handling nucleotide insertions, deletions, and replacements. It provides sequence validation, allows precise modifications, and generates an HTML report that highlights changes. The tool is ideal for bioinformatics workflows, particularly for genomic data analysis and reporting.

## Features

- **Insertion, Deletion, and Replacement**: Supports nucleotide changes at specified positions in the sequence.
- **Sequence Validation**: Verifies if the sequence matches before applying deletions.
- **HTML Report**: Generates an HTML file visualizing the differences between original and edited sequences.
- **Automatic Filenames**: Creates output FASTA and HTML files with names derived from sequence headers.
- **Error Handling**: Detects errors such as invalid formats or unmatched sequences for deletion.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gisaid_gap_corrector.git
   cd gisaid_gap_corrector
   ```

2. Install the required dependencies:
   ```bash
   pip install biopython
   ```

## Usage

To run the tool, execute the following command:

```bash
python3 gisaid_gap.py -f "path/to/your.fasta" -p <position> -ct <change_type> -cn <change_nucleotides> -mp "path/to/output"
```

### Arguments:

- `-f, --fasta_file`: Path to the FASTA file.
- `-p, --position`: Position in the sequence (1-based index) where the change will occur.
- `-ct, --change_type`: Type of change (`insertion`, `deletion`, or `replacement`).
- `-cn, --change_nucleotides`: Nucleotide(s) to be inserted, deleted, or replaced.
- `-mp, --main_path`: Path to the output directory where edited files will be saved.

### Example:

```bash
python3 gisaid_gap.py -f "/path/to/sequence.fasta" -p 345 -ct "insertion" -cn "AGTC" -mp "/path/to/output_folder"
```

This command will insert the nucleotides "AGTC" at position 345 in the specified FASTA file and generate both an edited FASTA file and an HTML report in the output folder.

## File Structure

The following output files are generated:

- **Edited FASTA file**: The modified sequence is saved with a name based on the original sequence header.
- **HTML Report**: A comprehensive HTML report visualizing the original and modified sequences with changes highlighted.

## Code Overview

The main functionality is provided by the `gisaid_gap_correct` function:

### Key Functions:

- `edit_fasta(fasta_file, position, change_type, change_nucleotides, fasta_path)`: 
  - Edits the FASTA sequence based on the specified change type (insertion, deletion, replacement).
  - Returns the original and modified sequences for HTML report generation.

- `generate_html_report(original_seq, edited_seq, position, change_type, change_nucleotides, fasta_name)`: 
  - Generates an HTML report highlighting changes in the sequence.
  
- `get_fasta_filename_from_header(fasta_file)`: 
  - Extracts a meaningful filename from the FASTA file header for the edited files.

### Error Handling:

- **Invalid Format**: If the FASTA file is empty or not in the correct format, an error will be raised.
- **Deletion Mismatch**: If the sequence at the specified position does not match the provided nucleotides for deletion, an error will occur, preventing incorrect deletions.

## Requirements

- Python 3.6+
- Biopython (`pip install biopython`)

## Contribution

Feel free to open issues and contribute to this project by forking the repository and submitting a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

### Acknowledgments

Special thanks to the open-source community and developers of Biopython.

