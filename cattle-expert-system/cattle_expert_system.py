"""
Sistem Pakar Penilaian Kualitas Bibit Sapi Potong
Berbasis Standar Nasional Indonesia (SNI)
Kelompok 6 - INF313 Kecerdasan Artifisial
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any


class KnowledgeBase:
    """
    Basis Pengetahuan - Menyimpan aturan-aturan pakar
    
    Kelas ini berfungsi sebagai knowledge base yang menyimpan:
    - Rules (aturan-aturan inferensi)
    - Bobot kriteria untuk weighted scoring
    - Database gejala/symptom yang dapat diamati
    """

    def __init__(self):
        """
        Inisialisasi basis pengetahuan dengan rules dan kriteria penilaian
        """
        # Dictionary yang menyimpan semua aturan inferensi (IF-THEN rules)
        # Setiap rule memiliki: kondisi IF, kesimpulan THEN, Certainty Factor, dan deskripsi
        self.rules = {
            'R1': {
                'IF': ['postur_tegak', 'dada_lebar', 'kaki_kuat'],
                'THEN': 'indikator_fisik_baik',
                'CF': 0.85,
                'description': 'Postur tubuh ideal untuk sapi potong'
            },
            'R2': {
                'IF': ['mata_cerah', 'hidung_basah', 'bulu_mengkilap'],
                'THEN': 'indikator_kesehatan_baik',
                'CF': 0.8,
                'description': 'Tanda-tanda kesehatan yang baik'
            },
            'R3': {
                'IF': ['umur_8_12_bulan', 'berat_150_200kg'],
                'THEN': 'umur_berat_ideal',
                'CF': 0.9,
                'description': 'Umur dan berat sesuai standar bibit'
            },
            'R4': {
                'IF': ['riwayat_vaksin_lengkap', 'tidak_ada_penyakit'],
                'THEN': 'riwayat_kesehatan_baik',
                'CF': 0.95,
                'description': 'Riwayat kesehatan terdokumentasi baik'
            },
            'R5': {
                'IF': ['indikator_fisik_baik', 'indikator_kesehatan_baik', 'umur_berat_ideal'],
                'THEN': 'kualitas_sangat_baik',
                'CF': 0.9,
                'description': 'Bibit memenuhi kriteria SNI kualitas A'
            },
            'R6': {
                'IF': ['indikator_fisik_baik', 'indikator_kesehatan_baik'],
                'THEN': 'kualitas_baik',
                'CF': 0.75,
                'description': 'Bibit memenuhi kriteria SNI kualitas B'
            },
            'R7': {
                'IF': ['punggung_rata', 'perut_tidak_buncit', 'ekor_panjang'],
                'THEN': 'konformasi_baik',
                'CF': 0.8,
                'description': 'Konformasi tubuh sesuai standar'
            },
            'R8': {
                'IF': ['konformasi_baik', 'indikator_fisik_baik'],
                'THEN': 'struktur_tubuh_ideal',
                'CF': 0.85,
                'description': 'Struktur tubuh memenuhi standar breeding'
            },
            'R9': {
                'IF': ['nafsu_makan_baik', 'aktif_bergerak', 'tidak_lemas'],
                'THEN': 'perilaku_normal',
                'CF': 0.8,
                'description': 'Perilaku menunjukkan kondisi sehat'
            },
            'R10': {
                'IF': ['struktur_tubuh_ideal', 'riwayat_kesehatan_baik', 'perilaku_normal'],
                'THEN': 'layak_dibeli_premium',
                'CF': 0.95,
                'description': 'Sangat direkomendasikan untuk pembelian'
            },
            'R11': {
                'IF': ['kualitas_baik', 'riwayat_kesehatan_baik'],
                'THEN': 'layak_dibeli_standar',
                'CF': 0.8,
                'description': 'Direkomendasikan untuk pembelian'
            },
            'R12': {
                'IF': ['postur_tegak', 'berat_kurang', 'umur_kurang'],
                'THEN': 'perlu_penggemukan',
                'CF': 0.7,
                'description': 'Bibit potensial namun perlu perawatan intensif'
            }
        }

        # Bobot untuk setiap kriteria berdasarkan standar SNI
        # Semakin penting kriteria, semakin tinggi bobotnya
        # SINKRON dengan sistem Streamlit untuk konsistensi penilaian
        self.criteria_weights = {
            'Postur Fisik': {
                'postur_tegak': 15,        # Kriteria sangat penting untuk struktur dasar
                'dada_lebar': 12,          # Penting untuk kapasitas paru-paru
                'kaki_kuat': 13,           # Penting untuk mobilitas dan daya tahan
                'punggung_rata': 10,       # Indikator konformasi yang baik
                'perut_tidak_buncit': 8,   # Indikator kesehatan pencernaan
                'ekor_panjang': 7          # Kriteria pelengkap
            },
            'Kondisi Kesehatan': {
                'mata_cerah': 10,                  # Indikator kesehatan umum
                'hidung_basah': 8,                 # Tanda sistem respirasi sehat
                'bulu_mengkilap': 7,               # Indikator nutrisi yang baik
                'tidak_ada_penyakit': 15,          # Kriteria sangat penting
                'riwayat_vaksin_lengkap': 12       # Penting untuk proteksi jangka panjang
            },
            'Umur dan Berat': {
                'umur_8_12_bulan': 20,     # Umur ideal untuk bibit
                'berat_150_200kg': 20,     # Berat ideal sesuai SNI
                'umur_kurang': 5,          # Penalti untuk umur kurang ideal
                'berat_kurang': 5,         # Penalti untuk berat kurang
                'umur_lebih': 8,           # Berat penalti lebih rendah
                'berat_lebih': 10          # Masih bisa diterima dengan nilai sedang
            },
            'Perilaku': {
                'nafsu_makan_baik': 12,    # Indikator kesehatan metabolisme
                'aktif_bergerak': 10,      # Tanda vitalitas yang baik
                'tidak_lemas': 11          # Indikator kesehatan umum
            }
        }

        # Database gejala/symptom yang dapat diamati pada sapi
        # Setiap gejala memiliki: ID unik, label deskriptif, dan Certainty Factor default
        self.symptom_database = {
            'Postur Fisik': [
                {'id': 'postur_tegak', 'label': 'Postur tubuh tegak dan proporsional', 'cf': 0.9},
                {'id': 'dada_lebar', 'label': 'Dada lebar dan dalam', 'cf': 0.85},
                {'id': 'kaki_kuat', 'label': 'Kaki kuat dan lurus', 'cf': 0.9},
                {'id': 'punggung_rata', 'label': 'Punggung rata dan kuat', 'cf': 0.8},
                {'id': 'perut_tidak_buncit', 'label': 'Perut tidak buncit', 'cf': 0.75},
                {'id': 'ekor_panjang', 'label': 'Ekor panjang hingga tumit', 'cf': 0.7}
            ],
            'Kondisi Kesehatan': [
                {'id': 'mata_cerah', 'label': 'Mata cerah dan bersih', 'cf': 0.85},
                {'id': 'hidung_basah', 'label': 'Hidung basah dan bersih', 'cf': 0.8},
                {'id': 'bulu_mengkilap', 'label': 'Bulu mengkilap dan rapi', 'cf': 0.75},
                {'id': 'tidak_ada_penyakit', 'label': 'Tidak ada riwayat penyakit', 'cf': 0.95},
                {'id': 'riwayat_vaksin_lengkap', 'label': 'Vaksinasi lengkap', 'cf': 0.9}
            ],
            'Umur dan Berat': [
                {'id': 'umur_8_12_bulan', 'label': 'Umur 8-12 bulan', 'cf': 0.9},
                {'id': 'berat_150_200kg', 'label': 'Berat 150-200 kg', 'cf': 0.9},
                {'id': 'umur_kurang', 'label': 'Umur kurang dari 8 bulan', 'cf': 0.6},
                {'id': 'berat_kurang', 'label': 'Berat kurang dari 150 kg', 'cf': 0.6},
                {'id': 'umur_lebih', 'label': 'Umur lebih dari 12 bulan', 'cf': 0.7},
                {'id': 'berat_lebih', 'label': 'Berat lebih dari 200 kg', 'cf': 0.7}
            ],
            'Perilaku': [
                {'id': 'nafsu_makan_baik', 'label': 'Nafsu makan baik', 'cf': 0.85},
                {'id': 'aktif_bergerak', 'label': 'Aktif bergerak', 'cf': 0.8},
                {'id': 'tidak_lemas', 'label': 'Tidak tampak lemas', 'cf': 0.85}
            ]
        }

    def get_all_rules(self) -> Dict:
        """
        Mengembalikan semua aturan dalam knowledge base
        
        Returns:
            Dict: Dictionary berisi semua rules
        """
        return self.rules

    def calculate_weighted_score(self, symptoms_input):
        """
        Menghitung skor berbobot berdasarkan kriteria yang dipilih
        Menggunakan metode weighted scoring yang sama dengan Streamlit
        
        Args:
            symptoms_input: Dictionary berisi symptom_id dan certainty factor-nya
            
        Returns:
            int: Skor ternormalisasi (0-100) dengan penalti untuk kriteria yang kurang
        """
        # Validasi input - kembalikan 0 jika tidak ada input
        if not symptoms_input:
            return 0

        # Inisialisasi variabel untuk perhitungan
        total_score = 0           # Akumulasi skor yang diperoleh
        max_possible_score = 0    # Total skor maksimal yang mungkin

        # Hitung skor aktual dan skor maksimal berdasarkan kriteria yang dipilih
        for symptom_id, symptom_cf in symptoms_input.items():
            # Cari bobot untuk gejala ini dari criteria_weights
            weight = 0
            for category, weights in self.criteria_weights.items():
                if symptom_id in weights:
                    weight = weights[symptom_id]
                    break

            # Formula: Skor = Bobot × Certainty Factor
            # Ini memberikan skor proporsional terhadap kepercayaan kita pada gejala tersebut
            symptom_score = weight * symptom_cf
            total_score += symptom_score
            max_possible_score += weight

        # Normalisasi skor ke skala 0-100
        # Rumus: (skor_aktual / skor_maksimal) × 100
        if max_possible_score > 0:
            normalized_score = (total_score / max_possible_score) * 100
        else:
            normalized_score = 0

        # SISTEM PENALTI untuk mendorong input kriteria yang lebih lengkap
        # Semakin sedikit kriteria, semakin besar penalti
        # Ini penting untuk menghindari kesimpulan prematur dengan data terbatas
        total_criteria = len(symptoms_input)
        
        if total_criteria < 3:
            # Penalti sangat besar: hanya 30% dari skor untuk ≤2 kriteria
            # Contoh: Jika skor 80, akan menjadi 24-80 tergantung jumlah kriteria
            penalty_factor = max(0.3, total_criteria / 10)
            normalized_score *= penalty_factor
        elif total_criteria < 5:
            # Penalti sedang: 50-62.5% untuk 3-4 kriteria
            penalty_factor = max(0.5, total_criteria / 8)
            normalized_score *= penalty_factor
        elif total_criteria < 8:
            # Penalti ringan: 70-87.5% untuk 5-7 kriteria
            penalty_factor = max(0.7, total_criteria / 10)
            normalized_score *= penalty_factor
        # Kriteria ≥8 tidak mendapat penalti

        # Pembulatan ke angka bulat untuk kemudahan interpretasi
        return round(normalized_score)


class WorkingMemory:
    """
    Memori Kerja - Menyimpan fakta-fakta sementara
    
    Kelas ini berfungsi sebagai working memory dalam sistem pakar:
    - Menyimpan fakta yang diketahui dari user (facts)
    - Menyimpan fakta yang diturunkan dari inferensi (derived_facts)
    - Mengelola Certainty Factor untuk setiap fakta
    """

    def __init__(self):
        """
        Inisialisasi working memory kosong
        """
        self.facts = {}          # Dictionary untuk menyimpan semua fakta
        self.derived_facts = {}  # Dictionary khusus untuk fakta hasil inferensi

    def add_fact(self, fact: str, cf: float = 1.0):
        """
        Menambahkan fakta baru ke working memory dengan certainty factor
        
        Args:
            fact: String identifikasi fakta (misalnya: 'postur_tegak')
            cf: Certainty Factor (0.0-1.0), default 1.0 untuk kepastian penuh
        """
        self.facts[fact] = cf

    def get_fact(self, fact: str) -> float:
        """
        Mendapatkan certainty factor dari sebuah fakta
        
        Args:
            fact: String identifikasi fakta
            
        Returns:
            float: Certainty Factor fakta, atau 0.0 jika fakta tidak ada
        """
        return self.facts.get(fact, 0.0)

    def has_fact(self, fact: str) -> bool:
        """
        Mengecek apakah sebuah fakta ada dalam working memory
        
        Args:
            fact: String identifikasi fakta
            
        Returns:
            bool: True jika fakta ada, False jika tidak
        """
        return fact in self.facts

    def add_derived_fact(self, fact: str, cf: float):
        """
        Menambahkan fakta yang diturunkan dari proses inferensi
        
        Jika fakta sudah ada, CF akan digabungkan menggunakan formula kombinasi CF.
        Ini penting untuk menangani multiple evidence untuk fakta yang sama.
        
        Args:
            fact: String identifikasi fakta hasil inferensi
            cf: Certainty Factor dari inferensi
        """
        if fact in self.derived_facts:
            # Jika fakta sudah ada, gabungkan CF-nya
            # Ini menangani situasi dimana multiple rules menghasilkan kesimpulan yang sama
            self.derived_facts[fact] = self.combine_cf(self.derived_facts[fact], cf)
        else:
            # Fakta baru, langsung simpan
            self.derived_facts[fact] = cf

        # Sinkronisasi dengan facts utama
        # Ini memastikan derived facts juga tersedia untuk rules lain
        self.facts[fact] = self.derived_facts[fact]

    def combine_cf(self, cf1: float, cf2: float) -> float:
        """
        Menggabungkan dua certainty factor menggunakan formula standar
        
        Formula: CF_combined = CF1 + CF2 × (1 - CF1)
        
        Ini adalah formula standar untuk menggabungkan evidence yang mendukung
        kesimpulan yang sama dari sumber berbeda.
        
        Args:
            cf1: Certainty Factor pertama
            cf2: Certainty Factor kedua
            
        Returns:
            float: Certainty Factor gabungan
            
        Contoh:
            combine_cf(0.8, 0.7) = 0.8 + 0.7 × (1 - 0.8) = 0.94
        """
        return cf1 + cf2 * (1 - cf1)

    def get_all_facts(self) -> Dict:
        """
        Mendapatkan semua fakta yang ada di working memory
        
        Returns:
            Dict: Dictionary berisi semua fakta dan CF-nya
        """
        return self.facts

    def clear(self):
        """
        Membersihkan semua fakta dari working memory
        
        Biasanya dipanggil sebelum memulai konsultasi baru untuk
        memastikan tidak ada data dari konsultasi sebelumnya.
        """
        self.facts.clear()
        self.derived_facts.clear()


class InferenceEngine:
    """
    Mesin Inferensi - Implementasi Forward Chaining
    
    Kelas ini mengimplementasikan forward chaining algorithm untuk
    melakukan reasoning berdasarkan fakta yang ada dan rules di knowledge base.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Inisialisasi inference engine dengan knowledge base
        
        Args:
            knowledge_base: Instance dari KnowledgeBase yang berisi rules
        """
        self.kb = knowledge_base          # Reference ke knowledge base
        self.reasoning_trace = []         # List untuk menyimpan jejak penalaran

    def forward_chaining(self, working_memory: WorkingMemory) -> Tuple[Dict, List]:
        """
        Implementasi algoritma Forward Chaining (Data-Driven Reasoning)
        
        Proses:
        1. Dimulai dari fakta yang sudah diketahui
        2. Cari rules yang kondisinya terpenuhi
        3. Eksekusi rule dan tambahkan kesimpulan ke working memory
        4. Ulangi sampai tidak ada rule baru yang bisa dieksekusi
        
        Args:
            working_memory: WorkingMemory yang berisi fakta awal
            
        Returns:
            Tuple[Dict, List]: (semua_fakta, jejak_penalaran)
        """
        # Reset reasoning trace untuk konsultasi baru
        self.reasoning_trace = []
        
        # List untuk tracking rules yang sudah digunakan
        # Ini mencegah rule yang sama dieksekusi berulang kali
        used_rules = []
        
        # Flag untuk mengecek apakah ada perubahan di working memory
        changed = True
        
        # Counter iterasi
        iteration = 0
        
        # Batas maksimal iterasi untuk mencegah infinite loop
        max_iterations = 20

        # Loop utama forward chaining
        # Berhenti jika: tidak ada perubahan ATAU mencapai max_iterations
        while changed and iteration < max_iterations:
            changed = False  # Reset flag di awal setiap iterasi
            iteration += 1

            # Iterasi melalui semua rules di knowledge base
            for rule_id, rule in self.kb.get_all_rules().items():
                # Skip rule yang sudah pernah digunakan
                if rule_id in used_rules:
                    continue

                # Cek apakah SEMUA kondisi IF dalam rule terpenuhi
                # all() akan return True hanya jika semua kondisi ada di working memory
                all_conditions_met = all(
                    working_memory.has_fact(condition)
                    for condition in rule['IF']
                )

                # Jika semua kondisi terpenuhi, eksekusi rule
                if all_conditions_met:
                    # Hitung CF gabungan dari rule dan semua kondisinya
                    # Mulai dengan CF rule itu sendiri
                    combined_cf = rule['CF']
                    
                    # Gabungkan dengan CF dari setiap kondisi
                    for condition in rule['IF']:
                        fact_cf = working_memory.get_fact(condition)
                        combined_cf = working_memory.combine_cf(combined_cf, fact_cf)

                    # Tambahkan kesimpulan ke working memory sebagai derived fact
                    working_memory.add_derived_fact(rule['THEN'], combined_cf)

                    # Catat langkah reasoning untuk explanation facility
                    self.reasoning_trace.append({
                        'rule_id': rule_id,
                        'description': rule['description'],
                        'conditions': rule['IF'],
                        'conclusion': rule['THEN'],
                        'cf': combined_cf,
                        'iteration': iteration
                    })

                    # Tandai rule sebagai sudah digunakan
                    used_rules.append(rule_id)
                    
                    # Set flag bahwa ada perubahan (rule baru dieksekusi)
                    changed = True

        # Return semua fakta (termasuk derived facts) dan jejak penalaran
        return working_memory.get_all_facts(), self.reasoning_trace

    def get_reasoning_trace(self) -> List:
        """
        Mendapatkan jejak penalaran lengkap
        
        Returns:
            List: List berisi langkah-langkah penalaran yang dilakukan
        """
        return self.reasoning_trace


class CattleExpertSystem:
    """
    Sistem Pakar Utama untuk Penilaian Bibit Sapi Potong
    
    Kelas ini mengintegrasikan semua komponen sistem pakar:
    - Knowledge Base (basis pengetahuan)
    - Working Memory (memori kerja)
    - Inference Engine (mesin inferensi)
    - User Interface (antarmuka pengguna)
    """

    def __init__(self):
        """
        Inisialisasi sistem pakar dengan semua komponennya
        """
        self.kb = KnowledgeBase()              # Basis pengetahuan
        self.wm = WorkingMemory()              # Memori kerja
        self.ie = InferenceEngine(self.kb)    # Mesin inferensi
        self.consultation_history = []         # Riwayat konsultasi
        self.current_symptoms = {}             # Gejala yang dipilih di konsultasi saat ini

    def get_user_input(self):
        """
        Mengambil input gejala/kriteria dari pengguna melalui console
        
        Proses:
        1. Menampilkan kategori gejala satu per satu
        2. Untuk Umur dan Berat: pilihan eksklusif (hanya bisa pilih satu)
        3. Untuk kategori lain: pilihan multiple (bisa pilih banyak)
        4. Menyimpan pilihan ke current_symptoms
        
        Returns:
            bool: True jika input berhasil, False jika dibatalkan
        """
        # Header untuk pemeriksaan
        print("\n" + "=" * 60)
        print("PEMERIKSAAN BIBIT SAPI POTONG")
        print("=" * 60)
        print("\nPilih kondisi yang sesuai dengan bibit sapi yang diamati:")
        print("(Tekan Enter untuk melewati, ketik 'selesai' untuk mengakhiri)\n")

        # Reset gejala untuk konsultasi baru
        self.current_symptoms = {}

        # Definisi pilihan eksklusif untuk Umur dan Berat
        # Hanya boleh memilih SATU dari setiap kategori ini
        umur_options = ['umur_8_12_bulan', 'umur_kurang', 'umur_lebih']
        berat_options = ['berat_150_200kg', 'berat_kurang', 'berat_lebih']
        selected_umur = None   # Tracking pilihan umur
        selected_berat = None  # Tracking pilihan berat

        # Iterasi melalui setiap kategori gejala
        for category, symptoms in self.kb.symptom_database.items():
            print(f"\n{category}:")

            # Handling khusus untuk kategori Umur dan Berat
            if category == 'Umur dan Berat':
                # ===== INPUT UMUR (Pilihan Eksklusif) =====
                print("  Pilih salah satu untuk Umur:")
                
                # Filter hanya gejala terkait umur
                umur_symptoms = [s for s in symptoms if s['id'] in umur_options]
                
                # Tampilkan pilihan umur
                for i, symptom in enumerate(umur_symptoms, 1):
                    print(f"    {i}. {symptom['label']}")

                # Loop untuk validasi input
                while True:
                    try:
                        umur_choice = input(f"    Pilih umur (1-{len(umur_symptoms)} atau Enter untuk skip): ")
                        
                        # User menekan Enter = skip
                        if umur_choice == '':
                            break
                            
                        # Convert ke integer untuk validasi
                        umur_choice = int(umur_choice)
                        
                        # Validasi range pilihan
                        if 1 <= umur_choice <= len(umur_symptoms):
                            selected_symptom = umur_symptoms[umur_choice - 1]
                            
                            # Hapus pilihan umur sebelumnya jika ada (ensure eksklusif)
                            for umur_id in umur_options:
                                if umur_id in self.current_symptoms:
                                    del self.current_symptoms[umur_id]
                            
                            # Simpan pilihan baru
                            self.current_symptoms[selected_symptom['id']] = selected_symptom['cf']
                            selected_umur = selected_symptom['id']
                            break
                        else:
                            print("    Pilihan tidak valid!")
                    except ValueError:
                        print("    Masukkan angka yang valid!")

                # ===== INPUT BERAT (Pilihan Eksklusif) =====
                print("  Pilih salah satu untuk Berat:")
                
                # Filter hanya gejala terkait berat
                berat_symptoms = [s for s in symptoms if s['id'] in berat_options]
                
                # Tampilkan pilihan berat
                for i, symptom in enumerate(berat_symptoms, 1):
                    print(f"    {i}. {symptom['label']}")

                # Loop untuk validasi input
                while True:
                    try:
                        berat_choice = input(f"    Pilih berat (1-{len(berat_symptoms)} atau Enter untuk skip): ")
                        
                        # User menekan Enter = skip
                        if berat_choice == '':
                            break
                            
                        # Convert ke integer untuk validasi
                        berat_choice = int(berat_choice)
                        
                        # Validasi range pilihan
                        if 1 <= berat_choice <= len(berat_symptoms):
                            selected_symptom = berat_symptoms[berat_choice - 1]
                            
                            # Hapus pilihan berat sebelumnya jika ada (ensure eksklusif)
                            for berat_id in berat_options:
                                if berat_id in self.current_symptoms:
                                    del self.current_symptoms[berat_id]
                            
                            # Simpan pilihan baru
                            self.current_symptoms[selected_symptom['id']] = selected_symptom['cf']
                            selected_berat = selected_symptom['id']
                            break
                        else:
                            print("    Pilihan tidak valid!")
                    except ValueError:
                        print("    Masukkan angka yang valid!")

            else:
                # ===== INPUT KATEGORI LAINNYA (Multiple Choice) =====
                # Untuk Postur Fisik, Kondisi Kesehatan, dan Perilaku
                for symptom in symptoms:
                    # Loop validasi untuk setiap gejala
                    while True:
                        response = input(f"  {symptom['label']}? (y/t/selesai): ").lower()

                        # User ketik 'selesai' = akhiri input
                        if response == 'selesai':
                            return True
                            
                        # User jawab 'ya' = simpan gejala
                        elif response in ['y', 'ya', 'yes']:
                            self.current_symptoms[symptom['id']] = symptom['cf']
                            break
                            
                        # User jawab 'tidak' atau Enter = skip gejala ini
                        elif response in ['t', 'tidak', 'no', '']:
                            break
                            
                        # Input tidak valid
                        else:
                            print("    Input tidak valid. Gunakan y/t/selesai")

        return True

    def diagnose(self) -> Dict:
        """
        Melakukan diagnosis menggunakan weighted scoring
        
        Metode ini adalah inti dari sistem penilaian yang:
        1. Menghitung weighted score berdasarkan kriteria yang dipilih
        2. Melakukan forward chaining untuk reasoning
        3. Menentukan grade dan rekomendasi berdasarkan skor
        4. Menyimpan hasil ke riwayat konsultasi
        
        Returns:
            Dict: Hasil diagnosis lengkap dengan kesimpulan, skor, dan reasoning trace
        """
        # Validasi: jika tidak ada gejala yang dipilih
        if not self.current_symptoms:
            return {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'conclusion': {
                    'id': 'unknown',
                    'label': 'Data Tidak Cukup',
                    'grade': 'N/A',
                    'cf': 0.0,
                    'score': 0,
                    'recommendation': 'Informasi yang diberikan belum cukup untuk memberikan penilaian. Silakan lengkapi data pemeriksaan bibit sapi.'
                },
                'facts': {},
                'reasoning_trace': [],
                'weighted_score': 0
            }

        # Hitung weighted score menggunakan metode yang sama dengan Streamlit
        # Ini adalah metode utama untuk menentukan kualitas bibit
        weighted_score = self.kb.calculate_weighted_score(self.current_symptoms)

        # Lakukan forward chaining untuk mendapatkan reasoning trace
        # Ini memberikan penjelasan HOW sistem sampai pada kesimpulan
        for symptom_id, cf in self.current_symptoms.items():
            self.wm.add_fact(symptom_id, cf)

        facts, trace = self.ie.forward_chaining(self.wm)

        # ===== MAPPING SKOR KE GRADE DAN REKOMENDASI =====
        # Sistem grading berdasarkan weighted score yang sudah dinormalisasi
        # Threshold disesuaikan dengan standar SNI untuk bibit sapi potong
        
        if weighted_score >= 85:
            # Grade A: Kualitas Premium
            conclusion_label = 'Layak Dibeli - Grade Premium (A)'
            recommendation = 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.'
            grade = 'A'
            certainty = weighted_score / 100
            
        elif weighted_score >= 70:
            # Grade B: Kualitas Standar yang baik
            conclusion_label = 'Layak Dibeli - Grade Standar (B)'
            recommendation = 'Bibit direkomendasikan. Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.'
            grade = 'B'
            certainty = weighted_score / 100
            
        elif weighted_score >= 60:
            # Grade B: Kualitas Baik
            conclusion_label = 'Kualitas Baik (B)'
            recommendation = 'Bibit menunjukkan kualitas yang baik.'
            grade = 'B'
            certainty = weighted_score / 100
            
        elif weighted_score >= 50:
            # Grade C: Potensial dengan perawatan
            conclusion_label = 'Potensial dengan Penggemukan (C)'
            recommendation = 'Bibit memiliki potensi namun perlu program penggemukan dan perawatan intensif selama 2-3 bulan.'
            grade = 'C'
            certainty = weighted_score / 100
            
        elif weighted_score >= 40:
            # Grade C: Kualitas Cukup
            conclusion_label = 'Kualitas Cukup (C)'
            recommendation = 'Bibit menunjukkan kualitas cukup, perlu observasi lebih lanjut.'
            grade = 'C'
            certainty = weighted_score / 100
            
        elif weighted_score >= 30:
            # Grade D: Perlu perhatian khusus
            conclusion_label = 'Perlu Perhatian Khusus (D)'
            recommendation = 'Bibit memerlukan perhatian dan perawatan khusus.'
            grade = 'D'
            certainty = weighted_score / 100
            
        else:
            # Grade E: Tidak direkomendasikan
            conclusion_label = 'Tidak Direkomendasikan (E)'
            recommendation = 'Bibit tidak direkomendasikan untuk dibeli.'
            grade = 'E'
            certainty = weighted_score / 100

        # Compile kesimpulan final
        best_conclusion = {
            'id': 'weighted_conclusion',
            'label': conclusion_label,
            'grade': grade,
            'cf': certainty,
            'score': weighted_score,
            'recommendation': recommendation
        }

        # Compile hasil diagnosis lengkap
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'conclusion': best_conclusion,
            'facts': facts,
            'reasoning_trace': trace,
            'weighted_score': weighted_score,
            'symptoms_used': len(self.current_symptoms)
        }

        # Simpan ke riwayat konsultasi untuk tracking
        self.consultation_history.append(result)

        return result

    def show_result(self, result: Dict):
        """
        Menampilkan hasil diagnosis ke console dengan format yang user-friendly
        
        Args:
            result: Dictionary hasil diagnosis dari metode diagnose()
        """
        # Header hasil
        print("\n" + "=" * 60)
        print("HASIL PENILAIAN BIBIT SAPI POTONG")
        print("=" * 60)

        # Extract data penting dari result
        conclusion = result['conclusion']
        weighted_score = result['weighted_score']
        symptoms_count = result['symptoms_used']

        # Tampilkan informasi utama
        print(f"\nKesimpulan: {conclusion['label']}")
        print(f"Grade: {conclusion['grade']}")
        print(f"Skor Kelayakan: {conclusion['score']}/100")
        print(f"Tingkat Kepercayaan: {int(conclusion['cf'] * 100)}%")
        print(f"Kriteria yang digunakan: {symptoms_count}")

        # Progress bar visual untuk tingkat kepercayaan
        # Memberikan representasi visual yang mudah dipahami
        bar_length = 40
        filled = int(bar_length * conclusion['cf'])
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"[{bar}] {int(conclusion['cf'] * 100)}%")

        # ===== SISTEM PERINGATAN BERDASARKAN JUMLAH KRITERIA =====
        # Warning ini penting untuk menginformasikan tingkat reliabilitas hasil
        # Semakin sedikit kriteria, semakin rendah akurasi penilaian
        
        if symptoms_count == 1:
            # Hanya 1 kriteria: akurasi sangat terbatas
            print(f"⚠️  PERINGATAN: Hasil berdasarkan hanya {symptoms_count} kriteria - Akurasi sangat terbatas")
        elif symptoms_count < 3:
            # 2 kriteria: akurasi rendah
            print(f"⚠️  PERINGATAN: Hasil berdasarkan {symptoms_count} kriteria - Akurasi rendah")
        elif symptoms_count < 5:
            # 3-4 kriteria: perlu tambahan data
            print(f"⚠️  PERINGATAN: Hasil berdasarkan {symptoms_count} kriteria - Disarankan tambah lebih banyak kriteria")
        elif symptoms_count < 8:
            # 5-7 kriteria: tingkat akurasi baik
            print(f"✅ Hasil berdasarkan {symptoms_count} kriteria - Tingkat akurasi baik")
        else:
            # 8+ kriteria: tingkat akurasi optimal
            print(f"✅ Hasil berdasarkan {symptoms_count} kriteria - Tingkat akurasi optimal")

        # Tampilkan rekomendasi
        print(f"\nRekomendasi:")
        print(f"{conclusion['recommendation']}")

        print("\n" + "-" * 60)

    def show_explanation_menu(self, result: Dict):
        """
        Menu interaktif untuk menampilkan penjelasan detail (Explanation Facility)
        
        Fitur WHY dan HOW dalam sistem pakar:
        - WHY: Mengapa sistem sampai pada kesimpulan tertentu
        - HOW: Bagaimana proses reasoning dilakukan
        
        Args:
            result: Dictionary hasil diagnosis
        """
        while True:
            # Menu pilihan penjelasan
            print("\n" + "=" * 60)
            print("MENU PENJELASAN")
            print("=" * 60)
            print("1. Tampilkan Alur Penalaran Lengkap")  # HOW explanation
            print("2. Lihat Kriteria yang Digunakan")     # Input yang digunakan
            print("3. Kembali ke Menu Utama")

            choice = input("\nPilih menu (1-3): ")

            if choice == '1':
                # ===== TAMPILKAN ALUR PENALARAN (HOW) =====
                print("\nALUR PENALARAN LENGKAP:")
                print("-" * 60)
                
                # Cek apakah ada reasoning trace dari forward chaining
                if not result['reasoning_trace']:
                    print("Tidak ada penalaran rule-based yang dijalankan.")
                    print("Sistem menggunakan weighted scoring berdasarkan kriteria SNI.")
                else:
                    # Tampilkan setiap langkah reasoning
                    for i, step in enumerate(result['reasoning_trace'], 1):
                        print(f"{i}. Rule {step['rule_id']}: {step['description']}")
                        print(f"   IF: {', '.join(step['conditions'])}")
                        print(f"   THEN: {step['conclusion']}")
                        print(f"   CF: {step['cf']:.2f}")
                        print()

                # Tampilkan informasi weighted score
                print(f"\nSKOR BERBOBOT (Weighted Score): {result['weighted_score']}/100")
                print("Sistem menggunakan kombinasi bobot SNI untuk setiap kriteria.")
                input("\nTekan Enter untuk melanjutkan...")

            elif choice == '2':
                # ===== TAMPILKAN KRITERIA YANG DIGUNAKAN =====
                print("\nKRITERIA YANG DIGUNAKAN:")
                print("-" * 60)
                
                # Loop melalui semua symptom yang dipilih user
                for symptom_id in self.current_symptoms.keys():
                    # Cari label yang user-friendly dari symptom_database
                    label = next(
                        (item['label'] 
                         for cat in self.kb.symptom_database.values() 
                         for item in cat 
                         if item['id'] == symptom_id), 
                        symptom_id  # Fallback ke ID jika label tidak ditemukan
                    )
                    print(f"- {label}")
                    
                input("\nTekan Enter untuk melanjutkan...")

            elif choice == '3':
                # Kembali ke menu utama
                break

    def export_report(self, result: Dict, filename: str = None):
        """
        Export hasil diagnosis ke file text untuk dokumentasi
        
        Fitur ini penting untuk:
        - Dokumentasi hasil konsultasi
        - Audit trail
        - Sharing hasil dengan pihak lain
        
        Args:
            result: Dictionary hasil diagnosis
            filename: Nama file output (opsional, akan auto-generate jika None)
        """
        # Generate nama file otomatis jika tidak dispesifikasi
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"laporan_penilaian_{timestamp}.txt"

        conclusion = result['conclusion']

        # Tulis laporan ke file
        with open(filename, 'w', encoding='utf-8') as f:
            # Header laporan
            f.write("=" * 60 + "\n")
            f.write("LAPORAN PENILAIAN BIBIT SAPI POTONG\n")
            f.write("Sistem Pakar Berbasis Weighted Scoring\n")
            f.write("=" * 60 + "\n\n")

            # Timestamp
            f.write(f"Tanggal: {result['timestamp']}\n\n")

            # Hasil Penilaian
            f.write("HASIL PENILAIAN:\n")
            f.write("-" * 60 + "\n")
            f.write(f"Kesimpulan: {conclusion['label']}\n")
            f.write(f"Grade: {conclusion['grade']}\n")
            f.write(f"Skor Kelayakan: {conclusion['score']}/100\n")
            f.write(f"Tingkat Kepercayaan: {int(conclusion['cf'] * 100)}%\n")
            f.write(f"Kriteria yang digunakan: {result['symptoms_used']}\n\n")

            # Rekomendasi
            f.write("REKOMENDASI:\n")
            f.write("-" * 60 + "\n")
            f.write(f"{conclusion['recommendation']}\n\n")

            # Kondisi yang diamati
            f.write("KONDISI YANG DIAMATI:\n")
            f.write("-" * 60 + "\n")
            for symptom_id in self.current_symptoms.keys():
                # Cari label yang sesuai
                label = next(
                    (item['label'] 
                     for cat in self.kb.symptom_database.values() 
                     for item in cat 
                     if item['id'] == symptom_id), 
                    symptom_id
                )
                f.write(f"- {label}\n")

            # Metode Penilaian
            f.write("\n" + "=" * 60 + "\n")
            f.write("METODE PENILAIAN:\n")
            f.write("=" * 60 + "\n")
            f.write("Sistem menggunakan weighted scoring berdasarkan Standar Nasional Indonesia (SNI)\n")
            f.write("dengan bobot yang telah ditentukan untuk setiap kriteria.\n")
            f.write(f"Skor akhir: {result['weighted_score']}/100\n")

        print(f"\nLaporan berhasil disimpan ke: {filename}")

    def show_history(self):
        """
        Menampilkan riwayat konsultasi yang telah dilakukan
        
        Berguna untuk:
        - Tracking hasil konsultasi sebelumnya
        - Membandingkan hasil antar konsultasi
        - Audit trail
        """
        print("\n" + "=" * 60)
        print("RIWAYAT KONSULTASI")
        print("=" * 60)

        # Cek apakah ada riwayat
        if not self.consultation_history:
            print("\nBelum ada riwayat konsultasi.")
            return

        # Tampilkan setiap record dalam riwayat
        for i, record in enumerate(self.consultation_history, 1):
            print(f"\n{i}. {record['timestamp']}")
            print(f"   Kesimpulan: {record['conclusion']['label']}")
            print(f"   Grade: {record['conclusion']['grade']}")
            print(f"   Skor: {record['conclusion']['score']}/100")

    def knowledge_acquisition_menu(self):
        """
        Menu untuk Knowledge Acquisition - mengelola basis pengetahuan
        
        Fitur ini memungkinkan pakar domain untuk:
        - Menambah rules baru
        - Mengedit rules yang ada
        - Menghapus rules
        - Menyimpan/memuat knowledge base dari file
        
        Ini adalah komponen penting dalam learning system.
        """
        while True:
            # Menu pengelolaan knowledge base
            print("\n" + "=" * 60)
            print("KELOLA BASIS PENGETAHUAN")
            print("=" * 60)
            print("1. Lihat Semua Rule")
            print("2. Tambah Rule Baru")
            print("3. Edit Rule")
            print("4. Hapus Rule")
            print("5. Simpan ke File")
            print("6. Muat dari File")
            print("7. Kembali")

            choice = input("\nPilih menu (1-7): ")

            if choice == '1':
                self.show_all_rules()
            elif choice == '2':
                self.add_new_rule()
            elif choice == '3':
                self.edit_rule()
            elif choice == '4':
                self.delete_rule()
            elif choice == '5':
                # Simpan knowledge base ke file JSON
                filename = input("Nama file (default: knowledge_base.json): ") or 'knowledge_base.json'
                self.kb.save_to_file(filename)
                print(f"Basis pengetahuan disimpan ke {filename}")
            elif choice == '6':
                # Muat knowledge base dari file JSON
                filename = input("Nama file (default: knowledge_base.json): ") or 'knowledge_base.json'
                self.kb.load_from_file(filename)
                print(f"Basis pengetahuan dimuat dari {filename}")
            elif choice == '7':
                break

    def show_all_rules(self):
        """
        Menampilkan semua rules yang ada di knowledge base
        
        Berguna untuk:
        - Review rules yang ada
        - Identifikasi rules yang perlu diupdate
        - Dokumentasi knowledge base
        """
        print("\n" + "=" * 60)
        print("DAFTAR RULE")
        print("=" * 60)

        # Iterasi dan tampilkan setiap rule
        for rule_id, rule in self.kb.get_all_rules().items():
            print(f"\n{rule_id}: {rule['description']}")
            print(f"  IF: {', '.join(rule['IF'])}")
            print(f"  THEN: {rule['THEN']}")
            print(f"  CF: {rule['CF']}")

    def add_new_rule(self):
        """
        Menambahkan rule baru ke knowledge base
        
        Proses:
        1. Input ID rule
        2. Input deskripsi
        3. Input kondisi IF
        4. Input kesimpulan THEN
        5. Input Certainty Factor
        6. Validasi dan simpan
        """
        print("\n" + "=" * 60)
        print("TAMBAH RULE BARU")
        print("=" * 60)

        # Input ID rule (harus unique)
        rule_id = input("ID Rule (contoh: R16): ").upper()
        if rule_id in self.kb.rules:
            print("Rule ID sudah ada!")
            return

        # Input komponen-komponen rule
        description = input("Deskripsi: ")

        print("Kondisi IF (pisahkan dengan koma):")
        conditions = [c.strip() for c in input().split(',')]

        conclusion = input("Kesimpulan THEN: ")

        cf = float(input("Certainty Factor (0.0-1.0): "))

        # Construct rule object
        new_rule = {
            'IF': conditions,
            'THEN': conclusion,
            'CF': cf,
            'description': description
        }

        # Tambahkan ke knowledge base
        if self.kb.add_rule(rule_id, new_rule):
            print(f"Rule {rule_id} berhasil ditambahkan!")
        else:
            print("Gagal menambahkan rule.")

    def edit_rule(self):
        """
        Mengedit rule yang sudah ada
        
        Proses:
        1. Pilih rule yang akan diedit
        2. Tampilkan nilai saat ini
        3. Input nilai baru (Enter untuk keep nilai lama)
        4. Update rule
        """
        print("\n" + "=" * 60)
        print("EDIT RULE")
        print("=" * 60)

        # Input ID rule yang akan diedit
        rule_id = input("ID Rule yang akan diedit: ").upper()
        if rule_id not in self.kb.rules:
            print("Rule tidak ditemukan!")
            return

        # Tampilkan rule saat ini
        rule = self.kb.rules[rule_id]
        print(f"\nRule saat ini:")
        print(f"Deskripsi: {rule['description']}")
        print(f"IF: {', '.join(rule['IF'])}")
        print(f"THEN: {rule['THEN']}")
        print(f"CF: {rule['CF']}")

        print("\n(Tekan Enter untuk mempertahankan nilai lama)")

        # Input nilai baru (dengan fallback ke nilai lama)
        description = input(f"Deskripsi baru: ") or rule['description']

        conditions_input = input(f"Kondisi IF baru (pisahkan dengan koma): ")
        conditions = [c.strip() for c in conditions_input.split(',')] if conditions_input else rule['IF']

        conclusion = input(f"Kesimpulan THEN baru: ") or rule['THEN']

        cf_input = input(f"CF baru (0.0-1.0): ")
        cf = float(cf_input) if cf_input else rule['CF']

        # Construct updated rule
        updated_rule = {
            'IF': conditions,
            'THEN': conclusion,
            'CF': cf,
            'description': description
        }

        # Update di knowledge base
        self.kb.update_rule(rule_id, updated_rule)
        print(f"Rule {rule_id} berhasil diupdate!")

    def delete_rule(self):
        """
        Menghapus rule dari knowledge base
        
        Perlu konfirmasi untuk mencegah penghapusan tidak sengaja
        """
        print("\n" + "=" * 60)
        print("HAPUS RULE")
        print("=" * 60)

        # Input ID rule yang akan dihapus
        rule_id = input("ID Rule yang akan dihapus: ").upper()

        # Konfirmasi penghapusan
        confirm = input(f"Yakin ingin menghapus {rule_id}? (y/n): ")
        if confirm.lower() == 'y':
            if self.kb.delete_rule(rule_id):
                print(f"Rule {rule_id} berhasil dihapus!")
            else:
                print("Rule tidak ditemukan!")

    def run(self):
        """
        Main loop untuk menjalankan sistem pakar
        
        Ini adalah entry point utama yang mengatur flow aplikasi:
        1. Tampilkan menu utama
        2. Handle pilihan user
        3. Route ke fungsi yang sesuai
        4. Loop sampai user memilih keluar
        """
        # Welcome screen
        print("\n" + "=" * 60)
        print("SISTEM PAKAR PENILAIAN BIBIT SAPI POTONG")
        print("Berbasis Standar Nasional Indonesia (SNI)")
        print("Kelompok 6 - INF313 Kecerdasan Artifisial")
        print("=" * 60)
        print("\nSISTEM TERINTEGRASI DENGAN STREAMLIT")
        print("Menggunakan Weighted Scoring Method")

        # Main application loop
        while True:
            # Menu utama
            print("\n" + "=" * 60)
            print("MENU UTAMA")
            print("=" * 60)
            print("1. Konsultasi Penilaian Bibit")
            print("2. Lihat Riwayat Konsultasi")
            print("3. Kelola Basis Pengetahuan")
            print("4. Tentang Sistem")
            print("5. Keluar")

            choice = input("\nPilih menu (1-5): ")

            if choice == '1':
                # ===== KONSULTASI PENILAIAN BIBIT =====
                # Clear working memory untuk konsultasi baru
                self.wm.clear()
                
                # Ambil input dari user
                if self.get_user_input():
                    # Lakukan diagnosis
                    result = self.diagnose()
                    
                    # Tampilkan hasil
                    self.show_result(result)

                    # Tanya apakah user ingin melihat penjelasan
                    show_exp = input("\nTampilkan penjelasan? (y/n): ")
                    if show_exp.lower() == 'y':
                        self.show_explanation_menu(result)

                    # Tanya apakah user ingin export laporan
                    export = input("\nExport laporan ke file? (y/n): ")
                    if export.lower() == 'y':
                        self.export_report(result)

            elif choice == '2':
                # ===== LIHAT RIWAYAT =====
                self.show_history()
                input("\nTekan Enter untuk melanjutkan...")

            elif choice == '3':
                # ===== KELOLA BASIS PENGETAHUAN =====
                self.knowledge_acquisition_menu()

            elif choice == '4':
                # ===== TENTANG SISTEM =====
                self.show_about()
                input("\nTekan Enter untuk melanjutkan...")

            elif choice == '5':
                # ===== KELUAR =====
                print("\nTerima kasih telah menggunakan sistem ini!")
                break

            else:
                # Input tidak valid
                print("\nPilihan tidak valid!")

    def show_about(self):
        """
        Menampilkan informasi tentang sistem
        
        Berisi:
        - Deskripsi sistem
        - Anggota kelompok
        - Fitur-fitur
        - Standar yang digunakan
        """
        print("\n" + "=" * 60)
        print("TENTANG SISTEM")
        print("=" * 60)
        print("\nSistem Pakar Penilaian Kualitas Bibit Sapi Potong")
        print("Berbasis Rule-Based System dengan Forward Chaining")
        print("\nKelompok 6:")
        print("1. YUYUN NAILUFAR")
        print("2. MUHAMMAD RAZI SIREGAR")
        print("3. REYAN ANDREA")
        print("4. FIRAH MAULIDA")
        print("5. IKRAM AL GHIFFARI")
        print("6. DIO FERDI JAYA")
        print("\nMata Kuliah: INF313 - Kecerdasan Artifisial")
        print("Dosen: [Nama Dosen]")
        print("\nFitur:")
        print("- Forward Chaining Inference Engine")
        print("- Certainty Factor untuk ketidakpastian")
        print("- Explanation Facility (WHY & HOW)")
        print("- Knowledge Acquisition Interface")
        print("- Export laporan konsultasi")
        print("- Riwayat konsultasi")
        print("\nStandar Acuan:")
        print("SNI 7651.6:2015 - Bibit Sapi Potong")


def main():
    """
    Fungsi utama untuk menjalankan aplikasi
    
    Entry point ketika script dijalankan langsung.
    Membuat instance CattleExpertSystem dan menjalankannya.
    """
    # Inisialisasi sistem pakar
    system = CattleExpertSystem()
    
    # Jalankan sistem
    system.run()


# Cek apakah script dijalankan langsung (bukan di-import)
if __name__ == "__main__":
    main()