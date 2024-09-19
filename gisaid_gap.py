from Bio import SeqIO
from Bio.Seq import Seq
import html
import re
import os

def gisaid_gap_correct(fasta_file, position, change_type, change_nucleotides, main_path):
    # Function to edit the fasta sequence based on user input
    def edit_fasta(fasta_file, position, change_type, change_nucleotides, fasta_path):
        # Load the sequence from the FASTA file
        records = list(SeqIO.parse(fasta_file, "fasta"))
        if not records:
            raise ValueError("FASTA file is empty or not in the correct format.")
        
        for record in records:
            seq = str(record.seq)
            original_seq = seq  # Save the original sequence for later comparison

            # Adjust the position (IGV is 1-based, Python is 0-based)
            position -= 1

            # Apply the requested change
            if change_type == "insertion":
                seq = seq[:position] + change_nucleotides + seq[position:]
            elif change_type == "deletion":
                # Check if the sequence matches before attempting deletion
                if seq[position:position + len(change_nucleotides)] == change_nucleotides:
                    seq = seq[:position] + seq[position + len(change_nucleotides):]
                else:
                    raise ValueError("The sequence at the specified position does not match the provided nucleotides for deletion.")
            elif change_type == "replacement":
                seq = seq[:position] + change_nucleotides + seq[position + len(change_nucleotides):]
            else:
                raise ValueError("Invalid change type. Must be 'insertion', 'deletion', or 'replacement'.")

            # Update the sequence
            record.seq = Seq(seq)

        # Save the edited sequence to a new FASTA file
        with open(fasta_path, "w") as output_handle:
            SeqIO.write(records, output_handle, "fasta")

        # Return original and edited sequences for HTML generation
        return original_seq, str(record.seq)

    # Function to format the numbering row for HTML
    def format_numbering_for_html(length):
        return ''.join(str(i % 10) for i in range(1, length + 1))

    # Function to format the numbering row with spaces for every 10 nucleotides
    def format_numbering_with_spaces(length):
        numbering = "1" + ' ' * 9
        for i in range(10, length + 1, 10):
            numbering += f"{i}{' ' * (10 - len(str(i)))}"
        return numbering

    # Function to generate the HTML report
    def generate_html_report(original_seq, edited_seq, position, change_type, change_nucleotides, fasta_name):
        html_content = "<html><head><title>FASTA Sequence Edit Report</title></head><body>"
        html_content += "<h1>FASTA Sequence Edit Report</h1>"
        html_content += "<table border='1'><tr><th>Type</th><th>Sequence</th></tr>"
        html_content += "<tr><td>Numbering (spaced)</td><td><pre>{}</pre></td></tr>".format(format_numbering_with_spaces(len(original_seq)))
        html_content += "<tr><td>Numbering</td><td><pre>{}</pre></td></tr>".format(format_numbering_for_html(len(original_seq)))
        html_content += "<tr><td>Original Sequence</td><td><pre>{}</pre></td></tr>".format(format_sequence_for_html(original_seq))
        html_content += "<tr><td>Edited Sequence</td><td><pre>{}</pre></td></tr>".format(format_sequence_for_html(edited_seq, position, change_type, change_nucleotides))
        html_content += "</table></body></html>"

        with open(fasta_name, "w") as html_file:
            html_file.write(html_content)

    # Function to format sequences for HTML with special visualization for changes
    def format_sequence_for_html(sequence, position=None, change_type=None, change_nucleotides=None):
        formatted_seq = ""
        for i, nucleotide in enumerate(sequence):
            if position is not None and i+1 >= position and i < position + len(change_nucleotides)-1:
                if change_type == "insertion":
                    formatted_seq += f"<span style='color: black; font-size: larger; background-color: green;'>{html.escape(nucleotide)}</span>"
                elif change_type == "deletion":
                    formatted_seq += f"<span style='color: black; font-size: larger; background-color: red;'>{html.escape(nucleotide)}</span>"
                elif change_type == "replacement":
                    formatted_seq += f"<span style='color: black; font-size: larger; background-color: #800080;'>{html.escape(nucleotide)}</span>"
            else:
                formatted_seq += html.escape(nucleotide)
        return formatted_seq

    # Function to generate a valid FASTA filename from the header
    def get_fasta_filename_from_header(fasta_file):
        records = list(SeqIO.parse(fasta_file, "fasta"))
        if not records:
            raise ValueError("FASTA file is empty or not in the correct format.")
        
        header = records[0].description
        match = re.search(r'/(\d{4}-\d{3})_', header)
        if match:
            return f"{match.group(1)}_edited.fasta"
        else:
            raise ValueError("Header does not match expected format.")

    # Main execution
    output_folder = f'{main_path}/edited_sequences'
    os.makedirs(output_folder, exist_ok=True)
    fasta_name = get_fasta_filename_from_header(fasta_file)
    fasta_path = f'{output_folder}/{fasta_name}.fasta'
    html_path = f'{output_folder}/{fasta_name}.html'

    # Edit the FASTA file
    original_seq, edited_seq = edit_fasta(fasta_file, position, change_type, change_nucleotides, fasta_path)

    # Generate the HTML report
    generate_html_report(original_seq, edited_seq, position, change_type, change_nucleotides, html_path)

    print(f"FASTA file edited and {fasta_name} generated.")
