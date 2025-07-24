import os
import ssl
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO

# --- KUNCI PERBAIKAN SSL ---
# Baris ini untuk menonaktifkan verifikasi sertifikat SSL secara global untuk aplikasi ini.
# Ini adalah workaround untuk error [SSL: CERTIFICATE_VERIFY_FAILED].
ssl._create_default_https_context = ssl._create_unverified_context

# --- Konfigurasi Aplikasi ---
UPLOAD_FOLDER = 'uploads'
# Menambahkan ekstensi lain yang umum untuk file FASTA
ALLOWED_EXTENSIONS = {'fasta', 'fa', 'txt', 'fna', 'faa'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Menambahkan secret_key untuk mengaktifkan session (diperlukan oleh flash()).
# Di lingkungan produksi, ini harus berupa string yang kompleks dan acak.
app.secret_key = 'ganti-dengan-kunci-rahasia-anda' 

# --- Fungsi Bantuan ---
def allowed_file(filename):
    """Memeriksa apakah ekstensi file diizinkan."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rute Aplikasi ---
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Menangani logika untuk halaman utama dan unggahan file."""
    if request.method == 'POST':
        # Periksa apakah ada file dalam request
        if 'file' not in request.files:
            flash('Tidak ada bagian file dalam request.')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Periksa apakah pengguna memilih file
        if file.filename == '':
            flash('Tidak ada file yang dipilih.')
            return redirect(request.url)
        
        # Jika file valid, simpan dan lanjutkan ke BLAST
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Pastikan direktori 'uploads' ada
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            return redirect(url_for('run_blast', filename=filename))
        else:
            flash('Format file tidak valid. Gunakan .fasta, .fa, .fna, .faa, atau .txt')
            return redirect(request.url)
            
    return render_template('index.html')


@app.route('/blast/<filename>')
def run_blast(filename):
    """Menjalankan query BLAST dan menampilkan hasilnya."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        flash('File tidak ditemukan.')
        return redirect(url_for('upload_file'))

    try:
        record = SeqIO.read(filepath, format="fasta")
        sequence_str = str(record.seq).upper()

        # --- KUNCI PERBAIKAN ---
        # Deteksi otomatis tipe sekuens (DNA/Protein)
        dna_alphabet = set("ACGTUN") # A,C,G,T untuk DNA, U untuk RNA, N untuk unknown
        is_protein = any(char not in dna_alphabet for char in sequence_str)

        if is_protein:
            blast_program = "blastp"  # Protein-Protein BLAST
            database = "nr"           # Non-Redundant Protein Sequences
        else:
            blast_program = "blastn"  # Nucleotide-Nucleotide BLAST
            database = "nt"           # Nucleotide collection

        # Kirim sekuens ke NCBI BLAST dengan program yang sesuai
        result_handle = NCBIWWW.qblast(blast_program, database, record.seq)
        
        blast_record = NCBIXML.read(result_handle)
        
        if blast_record.alignments:
            top_hit = blast_record.alignments[0]
            species_info = top_hit.title
            
            # Coba ekstrak nama spesies dari judul
            try:
                species_name = species_info.split('[')[-1].split(']')[0]
            except IndexError:
                parts = species_info.split('|')[-1].strip().split(' ')
                species_name = f"{parts[0]} {parts[1]}" if len(parts) > 1 else parts[0]

            best_alignment = top_hit.hsps[0]

            hasil = {
                'species': species_name,
                'accession': top_hit.accession,
                'score': best_alignment.score,
                'e_value': best_alignment.expect,
                'identity': (best_alignment.identities / best_alignment.align_length) * 100
            }
            return render_template('hasil.html', hasil=hasil)
        else:
            return render_template('hasil.html', hasil=None)
            
    except Exception as e:
        flash(f"Terjadi kesalahan saat proses BLAST: {e}")
        return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(debug=True)
