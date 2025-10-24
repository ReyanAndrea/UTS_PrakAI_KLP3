# """
# Sistem Pakar Penilaian Kualitas Bibit Sapi Potong
# Berbasis Standar Nasional Indonesia (SNI)
# Kelompok 6 - INF313 Kecerdasan Artifisial
# """
#
# import json
# import os
# from datetime import datetime
# from typing import Dict, List, Tuple, Any
#
# class KnowledgeBase:
#     """Basis Pengetahuan - Menyimpan aturan-aturan pakar"""
#
#     def __init__(self):
#         self.rules = {
#             'R1': {
#                 'IF': ['postur_tegak', 'dada_lebar', 'kaki_kuat'],
#                 'THEN': 'indikator_fisik_baik',
#                 'CF': 0.85,
#                 'description': 'Postur tubuh ideal untuk sapi potong'
#             },
#             'R2': {
#                 'IF': ['mata_cerah', 'hidung_basah', 'bulu_mengkilap'],
#                 'THEN': 'indikator_kesehatan_baik',
#                 'CF': 0.8,
#                 'description': 'Tanda-tanda kesehatan yang baik'
#             },
#             'R3': {
#                 'IF': ['umur_8_12_bulan', 'berat_150_200kg'],
#                 'THEN': 'umur_berat_ideal',
#                 'CF': 0.9,
#                 'description': 'Umur dan berat sesuai standar bibit'
#             },
#             'R4': {
#                 'IF': ['riwayat_vaksin_lengkap', 'tidak_ada_penyakit'],
#                 'THEN': 'riwayat_kesehatan_baik',
#                 'CF': 0.95,
#                 'description': 'Riwayat kesehatan terdokumentasi baik'
#             },
#             'R5': {
#                 'IF': ['indikator_fisik_baik', 'indikator_kesehatan_baik', 'umur_berat_ideal'],
#                 'THEN': 'kualitas_sangat_baik',
#                 'CF': 0.9,
#                 'description': 'Bibit memenuhi kriteria SNI kualitas A'
#             },
#             'R6': {
#                 'IF': ['indikator_fisik_baik', 'indikator_kesehatan_baik'],
#                 'THEN': 'kualitas_baik',
#                 'CF': 0.75,
#                 'description': 'Bibit memenuhi kriteria SNI kualitas B'
#             },
#             'R7': {
#                 'IF': ['punggung_rata', 'perut_tidak_buncit', 'ekor_panjang'],
#                 'THEN': 'konformasi_baik',
#                 'CF': 0.8,
#                 'description': 'Konformasi tubuh sesuai standar'
#             },
#             'R8': {
#                 'IF': ['konformasi_baik', 'indikator_fisik_baik'],
#                 'THEN': 'struktur_tubuh_ideal',
#                 'CF': 0.85,
#                 'description': 'Struktur tubuh memenuhi standar breeding'
#             },
#             'R9': {
#                 'IF': ['nafsu_makan_baik', 'aktif_bergerak', 'tidak_lemas'],
#                 'THEN': 'perilaku_normal',
#                 'CF': 0.8,
#                 'description': 'Perilaku menunjukkan kondisi sehat'
#             },
#             'R10': {
#                 'IF': ['struktur_tubuh_ideal', 'riwayat_kesehatan_baik', 'perilaku_normal'],
#                 'THEN': 'layak_dibeli_premium',
#                 'CF': 0.95,
#                 'description': 'Sangat direkomendasikan untuk pembelian'
#             },
#             'R11': {
#                 'IF': ['kualitas_baik', 'riwayat_kesehatan_baik'],
#                 'THEN': 'layak_dibeli_standar',
#                 'CF': 0.8,
#                 'description': 'Direkomendasikan untuk pembelian'
#             },
#             'R12': {
#                 'IF': ['postur_tegak', 'berat_kurang', 'umur_kurang'],
#                 'THEN': 'perlu_penggemukan',
#                 'CF': 0.7,
#                 'description': 'Bibit potensial namun perlu perawatan intensif'
#             },
#             'R13': {
#                 'IF': ['tanduk_simetris', 'kepala_proporsional'],
#                 'THEN': 'karakteristik_kepala_baik',
#                 'CF': 0.75,
#                 'description': 'Karakteristik kepala sesuai standar'
#             },
#             'R14': {
#                 'IF': ['karakteristik_kepala_baik', 'struktur_tubuh_ideal'],
#                 'THEN': 'konformasi_sempurna',
#                 'CF': 0.88,
#                 'description': 'Konformasi tubuh sempurna untuk breeding'
#             },
#             'R15': {
#                 'IF': ['konformasi_sempurna', 'kualitas_sangat_baik'],
#                 'THEN': 'bibit_unggul',
#                 'CF': 0.92,
#                 'description': 'Bibit unggul kelas premium'
#             }
#         }
#
#         self.symptom_database = {
#             'Postur Fisik': [
#                 {'id': 'postur_tegak', 'label': 'Postur tubuh tegak dan proporsional', 'cf': 0.9},
#                 {'id': 'dada_lebar', 'label': 'Dada lebar dan dalam', 'cf': 0.85},
#                 {'id': 'kaki_kuat', 'label': 'Kaki kuat dan lurus', 'cf': 0.9},
#                 {'id': 'punggung_rata', 'label': 'Punggung rata dan kuat', 'cf': 0.8},
#                 {'id': 'perut_tidak_buncit', 'label': 'Perut tidak buncit', 'cf': 0.75},
#                 {'id': 'ekor_panjang', 'label': 'Ekor panjang hingga tumit', 'cf': 0.7},
#                 {'id': 'tanduk_simetris', 'label': 'Tanduk simetris', 'cf': 0.75},
#                 {'id': 'kepala_proporsional', 'label': 'Kepala proporsional dengan tubuh', 'cf': 0.75}
#             ],
#             'Kondisi Kesehatan': [
#                 {'id': 'mata_cerah', 'label': 'Mata cerah dan bersih', 'cf': 0.85},
#                 {'id': 'hidung_basah', 'label': 'Hidung basah dan bersih', 'cf': 0.8},
#                 {'id': 'bulu_mengkilap', 'label': 'Bulu mengkilap dan rapi', 'cf': 0.75},
#                 {'id': 'tidak_ada_penyakit', 'label': 'Tidak ada riwayat penyakit', 'cf': 0.95},
#                 {'id': 'riwayat_vaksin_lengkap', 'label': 'Vaksinasi lengkap', 'cf': 0.9},
#                 {'id': 'kulit_elastis', 'label': 'Kulit elastis dan tidak kering', 'cf': 0.75}
#             ],
#             'Umur dan Berat': [
#                 {'id': 'umur_8_12_bulan', 'label': 'Umur 8-12 bulan', 'cf': 0.9},
#                 {'id': 'berat_150_200kg', 'label': 'Berat 150-200 kg', 'cf': 0.9},
#                 {'id': 'umur_kurang', 'label': 'Umur kurang dari 8 bulan', 'cf': 0.6},
#                 {'id': 'berat_kurang', 'label': 'Berat kurang dari 150 kg', 'cf': 0.6}
#             ],
#             'Perilaku': [
#                 {'id': 'nafsu_makan_baik', 'label': 'Nafsu makan baik', 'cf': 0.85},
#                 {'id': 'aktif_bergerak', 'label': 'Aktif bergerak', 'cf': 0.8},
#                 {'id': 'tidak_lemas', 'label': 'Tidak tampak lemas', 'cf': 0.85},
#                 {'id': 'responsif', 'label': 'Responsif terhadap rangsangan', 'cf': 0.8}
#             ]
#         }
#
#     def get_all_rules(self) -> Dict:
#         """Mengembalikan semua aturan"""
#         return self.rules
#
#     def add_rule(self, rule_id: str, rule: Dict) -> bool:
#         """Menambah aturan baru"""
#         if rule_id in self.rules:
#             return False
#         self.rules[rule_id] = rule
#         return True
#
#     def update_rule(self, rule_id: str, rule: Dict) -> bool:
#         """Memperbarui aturan"""
#         if rule_id not in self.rules:
#             return False
#         self.rules[rule_id] = rule
#         return True
#
#     def delete_rule(self, rule_id: str) -> bool:
#         """Menghapus aturan"""
#         if rule_id not in self.rules:
#             return False
#         del self.rules[rule_id]
#         return True
#
#     def save_to_file(self, filename: str = 'knowledge_base.json'):
#         """Menyimpan basis pengetahuan ke file"""
#         with open(filename, 'w', encoding='utf-8') as f:
#             json.dump(self.rules, f, indent=2, ensure_ascii=False)
#
#     def load_from_file(self, filename: str = 'knowledge_base.json'):
#         """Memuat basis pengetahuan dari file"""
#         if os.path.exists(filename):
#             with open(filename, 'r', encoding='utf-8') as f:
#                 self.rules = json.load(f)
#
#
# class WorkingMemory:
#     """Memori Kerja - Menyimpan fakta-fakta sementara"""
#
#     def __init__(self):
#         self.facts = {}
#         self.derived_facts = {}
#
#     def add_fact(self, fact: str, cf: float = 1.0):
#         """Menambah fakta dengan certainty factor"""
#         self.facts[fact] = cf
#
#     def get_fact(self, fact: str) -> float:
#         """Mendapatkan certainty factor dari fakta"""
#         return self.facts.get(fact, 0.0)
#
#     def has_fact(self, fact: str) -> bool:
#         """Mengecek apakah fakta ada"""
#         return fact in self.facts
#
#     def add_derived_fact(self, fact: str, cf: float):
#         """Menambah fakta yang diturunkan dari inferensi"""
#         if fact in self.derived_facts:
#             # Kombinasi CF jika fakta sudah ada
#             self.derived_facts[fact] = self.combine_cf(self.derived_facts[fact], cf)
#         else:
#             self.derived_facts[fact] = cf
#
#         # Update juga di facts utama
#         self.facts[fact] = self.derived_facts[fact]
#
#     def combine_cf(self, cf1: float, cf2: float) -> float:
#         """Menggabungkan dua certainty factor"""
#         return cf1 + cf2 * (1 - cf1)
#
#     def get_all_facts(self) -> Dict:
#         """Mendapatkan semua fakta"""
#         return self.facts
#
#     def clear(self):
#         """Membersihkan memori kerja"""
#         self.facts.clear()
#         self.derived_facts.clear()
#
#
# class InferenceEngine:
#     """Mesin Inferensi - Forward Chaining"""
#
#     def __init__(self, knowledge_base: KnowledgeBase):
#         self.kb = knowledge_base
#         self.reasoning_trace = []
#
#     def forward_chaining(self, working_memory: WorkingMemory) -> Tuple[Dict, List]:
#         """
#         Forward Chaining (Data-Driven Reasoning)
#         Dimulai dari fakta yang diketahui, kemudian mengaplikasikan rules
#         """
#         self.reasoning_trace = []
#         used_rules = []
#         changed = True
#         iteration = 0
#         max_iterations = 20
#
#         while changed and iteration < max_iterations:
#             changed = False
#             iteration += 1
#
#             for rule_id, rule in self.kb.get_all_rules().items():
#                 if rule_id in used_rules:
#                     continue
#
#                 # Cek apakah semua kondisi IF terpenuhi
#                 all_conditions_met = all(
#                     working_memory.has_fact(condition)
#                     for condition in rule['IF']
#                 )
#
#                 if all_conditions_met:
#                     # Hitung CF gabungan
#                     combined_cf = rule['CF']
#                     for condition in rule['IF']:
#                         fact_cf = working_memory.get_fact(condition)
#                         combined_cf = working_memory.combine_cf(combined_cf, fact_cf)
#
#                     # Tambah kesimpulan ke working memory
#                     working_memory.add_derived_fact(rule['THEN'], combined_cf)
#
#                     # Catat reasoning trace
#                     self.reasoning_trace.append({
#                         'rule_id': rule_id,
#                         'description': rule['description'],
#                         'conditions': rule['IF'],
#                         'conclusion': rule['THEN'],
#                         'cf': combined_cf,
#                         'iteration': iteration
#                     })
#
#                     used_rules.append(rule_id)
#                     changed = True
#
#         return working_memory.get_all_facts(), self.reasoning_trace
#
#     def get_reasoning_trace(self) -> List:
#         """Mendapatkan jejak penalaran"""
#         return self.reasoning_trace
#
#
# class ExplanationFacility:
#     """Fasilitas Penjelasan - WHY dan HOW"""
#
#     def __init__(self, inference_engine: InferenceEngine, knowledge_base: KnowledgeBase):
#         self.ie = inference_engine
#         self.kb = knowledge_base
#
#     def explain_how(self, conclusion: str) -> str:
#         """Menjelaskan BAGAIMANA sistem sampai pada kesimpulan"""
#         trace = self.ie.get_reasoning_trace()
#         explanation = f"\n{'='*60}\n"
#         explanation += f"PENJELASAN: Bagaimana sistem sampai pada kesimpulan?\n"
#         explanation += f"{'='*60}\n\n"
#
#         relevant_steps = [step for step in trace if step['conclusion'] == conclusion]
#
#         if not relevant_steps:
#             explanation += "Tidak ada jejak penalaran untuk kesimpulan ini.\n"
#             return explanation
#
#         for i, step in enumerate(relevant_steps, 1):
#             explanation += f"{i}. Rule {step['rule_id']}: {step['description']}\n"
#             explanation += f"   IF: {', '.join(step['conditions'])}\n"
#             explanation += f"   THEN: {step['conclusion']}\n"
#             explanation += f"   Certainty Factor: {step['cf']:.2f}\n"
#             explanation += f"   Iterasi: {step['iteration']}\n\n"
#
#         return explanation
#
#     def explain_why(self, rule_id: str) -> str:
#         """Menjelaskan MENGAPA sistem menanyakan pertanyaan tertentu"""
#         if rule_id not in self.kb.rules:
#             return "Rule tidak ditemukan."
#
#         rule = self.kb.rules[rule_id]
#         explanation = f"\n{'='*60}\n"
#         explanation += f"PENJELASAN: Mengapa pertanyaan ini diajukan?\n"
#         explanation += f"{'='*60}\n\n"
#         explanation += f"Rule {rule_id}: {rule['description']}\n\n"
#         explanation += f"Sistem memerlukan informasi berikut:\n"
#
#         for condition in rule['IF']:
#             explanation += f"  - {condition.replace('_', ' ').title()}\n"
#
#         explanation += f"\nUntuk dapat menyimpulkan: {rule['THEN'].replace('_', ' ').title()}\n"
#         explanation += f"Dengan tingkat kepercayaan: {rule['CF']:.0%}\n"
#
#         return explanation
#
#     def show_full_reasoning(self) -> str:
#         """Menampilkan seluruh alur penalaran"""
#         trace = self.ie.get_reasoning_trace()
#         explanation = f"\n{'='*60}\n"
#         explanation += f"ALUR PENALARAN LENGKAP\n"
#         explanation += f"{'='*60}\n\n"
#
#         for i, step in enumerate(trace, 1):
#             explanation += f"Langkah {i} (Iterasi {step['iteration']}):\n"
#             explanation += f"  Rule: {step['rule_id']} - {step['description']}\n"
#             explanation += f"  Kondisi: {', '.join(step['conditions'])}\n"
#             explanation += f"  Kesimpulan: {step['conclusion']}\n"
#             explanation += f"  CF: {step['cf']:.2f}\n\n"
#
#         return explanation
#
#
# class CattleExpertSystem:
#     """Sistem Pakar Utama"""
#
#     def __init__(self):
#         self.kb = KnowledgeBase()
#         self.wm = WorkingMemory()
#         self.ie = InferenceEngine(self.kb)
#         self.ef = ExplanationFacility(self.ie, self.kb)
#         self.consultation_history = []
#
#     def get_user_input(self):
#         """Mengambil input dari pengguna"""
#         print("\n" + "="*60)
#         print("PEMERIKSAAN BIBIT SAPI POTONG")
#         print("="*60)
#         print("\nPilih kondisi yang sesuai dengan bibit sapi yang diamati:")
#         print("(Tekan Enter untuk melewati, ketik 'selesai' untuk mengakhiri)\n")
#
#         for category, symptoms in self.kb.symptom_database.items():
#             print(f"\n{category}:")
#             for symptom in symptoms:
#                 while True:
#                     response = input(f"  {symptom['label']}? (y/t/selesai): ").lower()
#
#                     if response == 'selesai':
#                         return True
#                     elif response in ['y', 'ya', 'yes']:
#                         self.wm.add_fact(symptom['id'], symptom['cf'])
#                         break
#                     elif response in ['t', 'tidak', 'no', '']:
#                         break
#                     else:
#                         print("    Input tidak valid. Gunakan y/t/selesai")
#
#         return True
#
#     def diagnose(self) -> Dict:
#         """Melakukan diagnosis"""
#         facts, trace = self.ie.forward_chaining(self.wm)
#
#         # Definisi kesimpulan yang mungkin
#         conclusions = {
#             'bibit_unggul': {
#                 'label': 'Bibit Unggul Kelas Premium',
#                 'grade': 'A+',
#                 'recommendation': 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas premium. Sangat cocok untuk breeding atau penggemukan intensif dengan potensi keuntungan tinggi.'
#             },
#             'layak_dibeli_premium': {
#                 'label': 'Layak Dibeli - Grade Premium',
#                 'grade': 'A',
#                 'recommendation': 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.'
#             },
#             'layak_dibeli_standar': {
#                 'label': 'Layak Dibeli - Grade Standar',
#                 'grade': 'B',
#                 'recommendation': 'Bibit direkomendasikan. Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.'
#             },
#             'kualitas_sangat_baik': {
#                 'label': 'Kualitas Sangat Baik',
#                 'grade': 'A',
#                 'recommendation': 'Bibit memenuhi standar SNI Grade A dengan karakteristik fisik dan kesehatan excellent.'
#             },
#             'kualitas_baik': {
#                 'label': 'Kualitas Baik',
#                 'grade': 'B',
#                 'recommendation': 'Bibit memenuhi standar SNI Grade B dengan karakteristik yang baik.'
#             },
#             'perlu_penggemukan': {
#                 'label': 'Potensial dengan Penggemukan',
#                 'grade': 'C',
#                 'recommendation': 'Bibit memiliki potensi namun memerlukan program penggemukan dan perawatan intensif selama 2-3 bulan.'
#             }
#         }
#
#         # Cari kesimpulan dengan CF tertinggi
#         best_conclusion = None
#         best_cf = 0.0
#
#         for conclusion_id, conclusion_data in conclusions.items():
#             if conclusion_id in facts and facts[conclusion_id] > best_cf:
#                 best_cf = facts[conclusion_id]
#                 best_conclusion = {
#                     'id': conclusion_id,
#                     'label': conclusion_data['label'],
#                     'grade': conclusion_data['grade'],
#                     'cf': best_cf,
#                     'score': int(best_cf * 100),
#                     'recommendation': conclusion_data['recommendation']
#                 }
#
#         if best_conclusion is None or best_cf < 0.5:
#             best_conclusion = {
#                 'id': 'unknown',
#                 'label': 'Data Tidak Cukup',
#                 'grade': 'N/A',
#                 'cf': 0.0,
#                 'score': 0,
#                 'recommendation': 'Informasi yang diberikan belum cukup untuk memberikan penilaian. Silakan lengkapi data pemeriksaan bibit sapi.'
#             }
#
#         # Simpan ke history
#         result = {
#             'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'conclusion': best_conclusion,
#             'facts': facts,
#             'reasoning_trace': trace
#         }
#
#         self.consultation_history.append(result)
#
#         return result
#
#     def show_result(self, result: Dict):
#         """Menampilkan hasil diagnosis"""
#         print("\n" + "="*60)
#         print("HASIL PENILAIAN BIBIT SAPI POTONG")
#         print("="*60)
#
#         conclusion = result['conclusion']
#         print(f"\nKesimpulan: {conclusion['label']}")
#         print(f"Grade: {conclusion['grade']}")
#         print(f"Skor Kelayakan: {conclusion['score']}/100")
#         print(f"Tingkat Kepercayaan: {int(conclusion['cf'] * 100)}%")
#
#         # Progress bar
#         bar_length = 40
#         filled = int(bar_length * conclusion['cf'])
#         bar = '█' * filled + '░' * (bar_length - filled)
#         print(f"[{bar}] {int(conclusion['cf'] * 100)}%")
#
#         print(f"\nRekomendasi:")
#         print(f"{conclusion['recommendation']}")
#
#         print("\n" + "-"*60)
#
#     def show_explanation_menu(self, result: Dict):
#         """Menu penjelasan"""
#         while True:
#             print("\n" + "="*60)
#             print("MENU PENJELASAN")
#             print("="*60)
#             print("1. Tampilkan Alur Penalaran Lengkap (HOW)")
#             print("2. Penjelasan Rule Tertentu (WHY)")
#             print("3. Kembali ke Menu Utama")
#
#             choice = input("\nPilih menu (1-3): ")
#
#             if choice == '1':
#                 print(self.ef.show_full_reasoning())
#                 input("\nTekan Enter untuk melanjutkan...")
#             elif choice == '2':
#                 rule_id = input("Masukkan ID Rule (contoh: R1): ").upper()
#                 print(self.ef.explain_why(rule_id))
#                 input("\nTekan Enter untuk melanjutkan...")
#             elif choice == '3':
#                 break
#
#     def export_report(self, result: Dict, filename: str = None):
#         """Export hasil ke file"""
#         if filename is None:
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             filename = f"laporan_penilaian_{timestamp}.txt"
#
#         conclusion = result['conclusion']
#
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write("="*60 + "\n")
#             f.write("LAPORAN PENILAIAN BIBIT SAPI POTONG\n")
#             f.write("Sistem Pakar Berbasis Rule-Based\n")
#             f.write("="*60 + "\n\n")
#
#             f.write(f"Tanggal: {result['timestamp']}\n\n")
#
#             f.write("HASIL PENILAIAN:\n")
#             f.write("-"*60 + "\n")
#             f.write(f"Kesimpulan: {conclusion['label']}\n")
#             f.write(f"Grade: {conclusion['grade']}\n")
#             f.write(f"Skor Kelayakan: {conclusion['score']}/100\n")
#             f.write(f"Tingkat Kepercayaan: {int(conclusion['cf'] * 100)}%\n\n")
#
#             f.write("REKOMENDASI:\n")
#             f.write("-"*60 + "\n")
#             f.write(f"{conclusion['recommendation']}\n\n")
#
#             f.write("KONDISI YANG DIAMATI:\n")
#             f.write("-"*60 + "\n")
#             for fact, cf in result['facts'].items():
#                 if fact in [s['id'] for cat in self.kb.symptom_database.values() for s in cat]:
#                     f.write(f"- {fact.replace('_', ' ').title()} (CF: {cf:.2f})\n")
#
#             f.write("\n" + "="*60 + "\n")
#             f.write("PROSES PENALARAN:\n")
#             f.write("="*60 + "\n\n")
#
#             for i, step in enumerate(result['reasoning_trace'], 1):
#                 f.write(f"Langkah {i}:\n")
#                 f.write(f"  Rule: {step['rule_id']} - {step['description']}\n")
#                 f.write(f"  IF: {', '.join(step['conditions'])}\n")
#                 f.write(f"  THEN: {step['conclusion']}\n")
#                 f.write(f"  CF: {step['cf']:.2f}\n\n")
#
#         print(f"\nLaporan berhasil disimpan ke: {filename}")
#
#     def show_history(self):
#         """Menampilkan riwayat konsultasi"""
#         print("\n" + "="*60)
#         print("RIWAYAT KONSULTASI")
#         print("="*60)
#
#         if not self.consultation_history:
#             print("\nBelum ada riwayat konsultasi.")
#             return
#
#         for i, record in enumerate(self.consultation_history, 1):
#             print(f"\n{i}. {record['timestamp']}")
#             print(f"   Kesimpulan: {record['conclusion']['label']}")
#             print(f"   Grade: {record['conclusion']['grade']}")
#             print(f"   Skor: {record['conclusion']['score']}/100")
#
#     def knowledge_acquisition_menu(self):
#         """Menu akuisisi pengetahuan"""
#         while True:
#             print("\n" + "="*60)
#             print("KELOLA BASIS PENGETAHUAN")
#             print("="*60)
#             print("1. Lihat Semua Rule")
#             print("2. Tambah Rule Baru")
#             print("3. Edit Rule")
#             print("4. Hapus Rule")
#             print("5. Simpan ke File")
#             print("6. Muat dari File")
#             print("7. Kembali")
#
#             choice = input("\nPilih menu (1-7): ")
#
#             if choice == '1':
#                 self.show_all_rules()
#             elif choice == '2':
#                 self.add_new_rule()
#             elif choice == '3':
#                 self.edit_rule()
#             elif choice == '4':
#                 self.delete_rule()
#             elif choice == '5':
#                 filename = input("Nama file (default: knowledge_base.json): ") or 'knowledge_base.json'
#                 self.kb.save_to_file(filename)
#                 print(f"Basis pengetahuan disimpan ke {filename}")
#             elif choice == '6':
#                 filename = input("Nama file (default: knowledge_base.json): ") or 'knowledge_base.json'
#                 self.kb.load_from_file(filename)
#                 print(f"Basis pengetahuan dimuat dari {filename}")
#             elif choice == '7':
#                 break
#
#     def show_all_rules(self):
#         """Menampilkan semua rule"""
#         print("\n" + "="*60)
#         print("DAFTAR RULE")
#         print("="*60)
#
#         for rule_id, rule in self.kb.get_all_rules().items():
#             print(f"\n{rule_id}: {rule['description']}")
#             print(f"  IF: {', '.join(rule['IF'])}")
#             print(f"  THEN: {rule['THEN']}")
#             print(f"  CF: {rule['CF']}")
#
#     def add_new_rule(self):
#         """Menambah rule baru"""
#         print("\n" + "="*60)
#         print("TAMBAH RULE BARU")
#         print("="*60)
#
#         rule_id = input("ID Rule (contoh: R16): ").upper()
#         if rule_id in self.kb.rules:
#             print("Rule ID sudah ada!")
#             return
#
#         description = input("Deskripsi: ")
#
#         print("Kondisi IF (pisahkan dengan koma):")
#         conditions = [c.strip() for c in input().split(',')]
#
#         conclusion = input("Kesimpulan THEN: ")
#
#         cf = float(input("Certainty Factor (0.0-1.0): "))
#
#         new_rule = {
#             'IF': conditions,
#             'THEN': conclusion,
#             'CF': cf,
#             'description': description
#         }
#
#         if self.kb.add_rule(rule_id, new_rule):
#             print(f"Rule {rule_id} berhasil ditambahkan!")
#         else:
#             print("Gagal menambahkan rule.")
#
#     def edit_rule(self):
#         """Edit rule yang ada"""
#         print("\n" + "="*60)
#         print("EDIT RULE")
#         print("="*60)
#
#         rule_id = input("ID Rule yang akan diedit: ").upper()
#         if rule_id not in self.kb.rules:
#             print("Rule tidak ditemukan!")
#             return
#
#         rule = self.kb.rules[rule_id]
#         print(f"\nRule saat ini:")
#         print(f"Deskripsi: {rule['description']}")
#         print(f"IF: {', '.join(rule['IF'])}")
#         print(f"THEN: {rule['THEN']}")
#         print(f"CF: {rule['CF']}")
#
#         print("\n(Tekan Enter untuk mempertahankan nilai lama)")
#
#         description = input(f"Deskripsi baru: ") or rule['description']
#
#         conditions_input = input(f"Kondisi IF baru (pisahkan dengan koma): ")
#         conditions = [c.strip() for c in conditions_input.split(',')] if conditions_input else rule['IF']
#
#         conclusion = input(f"Kesimpulan THEN baru: ") or rule['THEN']
#
#         cf_input = input(f"CF baru (0.0-1.0): ")
#         cf = float(cf_input) if cf_input else rule['CF']
#
#         updated_rule = {
#             'IF': conditions,
#             'THEN': conclusion,
#             'CF': cf,
#             'description': description
#         }
#
#         self.kb.update_rule(rule_id, updated_rule)
#         print(f"Rule {rule_id} berhasil diupdate!")
#
#     def delete_rule(self):
#         """Hapus rule"""
#         print("\n" + "="*60)
#         print("HAPUS RULE")
#         print("="*60)
#
#         rule_id = input("ID Rule yang akan dihapus: ").upper()
#
#         confirm = input(f"Yakin ingin menghapus {rule_id}? (y/n): ")
#         if confirm.lower() == 'y':
#             if self.kb.delete_rule(rule_id):
#                 print(f"Rule {rule_id} berhasil dihapus!")
#             else:
#                 print("Rule tidak ditemukan!")
#
#     def run(self):
#         """Menjalankan sistem pakar"""
#         print("\n" + "="*60)
#         print("SISTEM PAKAR PENILAIAN BIBIT SAPI POTONG")
#         print("Berbasis Standar Nasional Indonesia (SNI)")
#         print("Kelompok 6 - INF313 Kecerdasan Artifisial")
#         print("="*60)
#
#         while True:
#             print("\n" + "="*60)
#             print("MENU UTAMA")
#             print("="*60)
#             print("1. Konsultasi Penilaian Bibit")
#             print("2. Lihat Riwayat Konsultasi")
#             print("3. Kelola Basis Pengetahuan")
#             print("4. Tentang Sistem")
#             print("5. Keluar")
#
#             choice = input("\nPilih menu (1-5): ")
#
#             if choice == '1':
#                 self.wm.clear()
#                 if self.get_user_input():
#                     result = self.diagnose()
#                     self.show_result(result)
#
#                     show_exp = input("\nTampilkan penjelasan? (y/n): ")
#                     if show_exp.lower() == 'y':
#                         self.show_explanation_menu(result)
#
#                     export = input("\nExport laporan ke file? (y/n): ")
#                     if export.lower() == 'y':
#                         self.export_report(result)
#
#             elif choice == '2':
#                 self.show_history()
#                 input("\nTekan Enter untuk melanjutkan...")
#
#             elif choice == '3':
#                 self.knowledge_acquisition_menu()
#
#             elif choice == '4':
#                 self.show_about()
#                 input("\nTekan Enter untuk melanjutkan...")
#
#             elif choice == '5':
#                 print("\nTerima kasih telah menggunakan sistem ini!")
#                 break
#
#             else:
#                 print("\nPilihan tidak valid!")
#
#     def show_about(self):
#         """Menampilkan informasi tentang sistem"""
#         print("\n" + "="*60)
#         print("TENTANG SISTEM")
#         print("="*60)
#         print("\nSistem Pakar Penilaian Kualitas Bibit Sapi Potong")
#         print("Berbasis Rule-Based System dengan Forward Chaining")
#         print("\nKelompok 6:")
#         print("1. YUYUN NAILUFAR")
#         print("2. MUHAMMAD RAZI SIREGAR")
#         print("3. REYAN ANDREA")
#         print("4. FIRAH MAULIDA")
#         print("5. IKRAM AL GHIFFARI")
#         print("6. DIO FERDI JAYA")
#         print("\nMata Kuliah: INF313 - Kecerdasan Artifisial")
#         print("Dosen: [Nama Dosen]")
#         print("\nFitur:")
#         print("- Forward Chaining Inference Engine")
#         print("- Certainty Factor untuk ketidakpastian")
#         print("- Explanation Facility (WHY & HOW)")
#         print("- Knowledge Acquisition Interface")
#         print("- Export laporan konsultasi")
#         print("- Riwayat konsultasi")
#         print("\nStandar Acuan:")
#         print("SNI 7651.6:2015 - Bibit Sapi Potong")
#
#
# def main():
#     """Fungsi utama"""
#     system = CattleExpertSystem()
#     system.run()
#
#
# if __name__ == "__main__":
#     main()

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
    """Basis Pengetahuan - Menyimpan aturan-aturan pakar"""

    def __init__(self):
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
            # R13, R14, R15 dihapus karena berkaitan dengan tanduk dan kepala yang sudah dihapus
        }

        # Definisikan bobot untuk setiap kriteria - SAMA DENGAN STREAMLIT
        self.criteria_weights = {
            'Postur Fisik': {
                'postur_tegak': 15,
                'dada_lebar': 12,
                'kaki_kuat': 13,
                'punggung_rata': 10,
                'perut_tidak_buncit': 8,
                'ekor_panjang': 7
                # tanduk_simetris dan kepala_proporsional dihapus
            },
            'Kondisi Kesehatan': {
                'mata_cerah': 10,
                'hidung_basah': 8,
                'bulu_mengkilap': 7,
                'tidak_ada_penyakit': 15,
                'riwayat_vaksin_lengkap': 12
                # kulit_elastis dihapus
            },
            'Umur dan Berat': {
                'umur_8_12_bulan': 20,
                'berat_150_200kg': 20,
                'umur_kurang': 5,
                'berat_kurang': 5,
                'umur_lebih': 8,  # Ditambahkan
                'berat_lebih': 10  # Ditambahkan
            },
            'Perilaku': {
                'nafsu_makan_baik': 12,
                'aktif_bergerak': 10,
                'tidak_lemas': 11
                # Responsif dihapus
            }
        }

        self.symptom_database = {
            'Postur Fisik': [
                {'id': 'postur_tegak', 'label': 'Postur tubuh tegak dan proporsional', 'cf': 0.9},
                {'id': 'dada_lebar', 'label': 'Dada lebar dan dalam', 'cf': 0.85},
                {'id': 'kaki_kuat', 'label': 'Kaki kuat dan lurus', 'cf': 0.9},
                {'id': 'punggung_rata', 'label': 'Punggung rata dan kuat', 'cf': 0.8},
                {'id': 'perut_tidak_buncit', 'label': 'Perut tidak buncit', 'cf': 0.75},
                {'id': 'ekor_panjang', 'label': 'Ekor panjang hingga tumit', 'cf': 0.7}
                # tanduk_simetris dan kepala_proporsional dihapus
            ],
            'Kondisi Kesehatan': [
                {'id': 'mata_cerah', 'label': 'Mata cerah dan bersih', 'cf': 0.85},
                {'id': 'hidung_basah', 'label': 'Hidung basah dan bersih', 'cf': 0.8},
                {'id': 'bulu_mengkilap', 'label': 'Bulu mengkilap dan rapi', 'cf': 0.75},
                {'id': 'tidak_ada_penyakit', 'label': 'Tidak ada riwayat penyakit', 'cf': 0.95},
                {'id': 'riwayat_vaksin_lengkap', 'label': 'Vaksinasi lengkap', 'cf': 0.9}
                # kulit_elastis dihapus
            ],
            'Umur dan Berat': [
                {'id': 'umur_8_12_bulan', 'label': 'Umur 8-12 bulan', 'cf': 0.9},
                {'id': 'berat_150_200kg', 'label': 'Berat 150-200 kg', 'cf': 0.9},
                {'id': 'umur_kurang', 'label': 'Umur kurang dari 8 bulan', 'cf': 0.6},
                {'id': 'berat_kurang', 'label': 'Berat kurang dari 150 kg', 'cf': 0.6},
                {'id': 'umur_lebih', 'label': 'Umur lebih dari 12 bulan', 'cf': 0.7},  # Ditambahkan
                {'id': 'berat_lebih', 'label': 'Berat lebih dari 200 kg', 'cf': 0.7}  # Ditambahkan
            ],
            'Perilaku': [
                {'id': 'nafsu_makan_baik', 'label': 'Nafsu makan baik', 'cf': 0.85},
                {'id': 'aktif_bergerak', 'label': 'Aktif bergerak', 'cf': 0.8},
                {'id': 'tidak_lemas', 'label': 'Tidak tampak lemas', 'cf': 0.85}
                # Responsif dihapus
            ]
        }

    def get_all_rules(self) -> Dict:
        """Mengembalikan semua aturan"""
        return self.rules

    def calculate_weighted_score(self, symptoms_input):
        """Menghitung skor berbobot berdasarkan kriteria yang dipilih - SAMA DENGAN STREAMLIT"""
        if not symptoms_input:
            return 0

        total_score = 0
        max_possible_score = 0

        # Hitung skor aktual dan skor maksimal
        for symptom_id, symptom_cf in symptoms_input.items():
            # Cari bobot untuk gejala ini
            weight = 0
            for category, weights in self.criteria_weights.items():
                if symptom_id in weights:
                    weight = weights[symptom_id]
                    break

            # Skor = bobot * certainty factor
            symptom_score = weight * symptom_cf
            total_score += symptom_score
            max_possible_score += weight

        # Normalisasi ke skala 0-100
        if max_possible_score > 0:
            normalized_score = (total_score / max_possible_score) * 100
        else:
            normalized_score = 0

        # PENALTI untuk kriteria yang kurang - SAMA DENGAN STREAMLIT
        total_criteria = len(symptoms_input)
        if total_criteria < 3:
            # Penalty besar untuk kriteria yang sangat sedikit
            penalty_factor = max(0.3, total_criteria / 10)  # Minimal 30% dari skor
            normalized_score *= penalty_factor
        elif total_criteria < 5:
            # Penalty sedang
            penalty_factor = max(0.5, total_criteria / 8)
            normalized_score *= penalty_factor
        elif total_criteria < 8:
            # Penalty kecil
            penalty_factor = max(0.7, total_criteria / 10)
            normalized_score *= penalty_factor

        return round(normalized_score)


class WorkingMemory:
    """Memori Kerja - Menyimpan fakta-fakta sementara"""

    def __init__(self):
        self.facts = {}
        self.derived_facts = {}

    def add_fact(self, fact: str, cf: float = 1.0):
        """Menambah fakta dengan certainty factor"""
        self.facts[fact] = cf

    def get_fact(self, fact: str) -> float:
        """Mendapatkan certainty factor dari fakta"""
        return self.facts.get(fact, 0.0)

    def has_fact(self, fact: str) -> bool:
        """Mengecek apakah fakta ada"""
        return fact in self.facts

    def add_derived_fact(self, fact: str, cf: float):
        """Menambah fakta yang diturunkan dari inferensi"""
        if fact in self.derived_facts:
            # Kombinasi CF jika fakta sudah ada
            self.derived_facts[fact] = self.combine_cf(self.derived_facts[fact], cf)
        else:
            self.derived_facts[fact] = cf

        # Update juga di facts utama
        self.facts[fact] = self.derived_facts[fact]

    def combine_cf(self, cf1: float, cf2: float) -> float:
        """Menggabungkan dua certainty factor"""
        return cf1 + cf2 * (1 - cf1)

    def get_all_facts(self) -> Dict:
        """Mendapatkan semua fakta"""
        return self.facts

    def clear(self):
        """Membersihkan memori kerja"""
        self.facts.clear()
        self.derived_facts.clear()


class InferenceEngine:
    """Mesin Inferensi - Forward Chaining"""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.reasoning_trace = []

    def forward_chaining(self, working_memory: WorkingMemory) -> Tuple[Dict, List]:
        """
        Forward Chaining (Data-Driven Reasoning)
        Dimulai dari fakta yang diketahui, kemudian mengaplikasikan rules
        """
        self.reasoning_trace = []
        used_rules = []
        changed = True
        iteration = 0
        max_iterations = 20

        while changed and iteration < max_iterations:
            changed = False
            iteration += 1

            for rule_id, rule in self.kb.get_all_rules().items():
                if rule_id in used_rules:
                    continue

                # Cek apakah semua kondisi IF terpenuhi
                all_conditions_met = all(
                    working_memory.has_fact(condition)
                    for condition in rule['IF']
                )

                if all_conditions_met:
                    # Hitung CF gabungan
                    combined_cf = rule['CF']
                    for condition in rule['IF']:
                        fact_cf = working_memory.get_fact(condition)
                        combined_cf = working_memory.combine_cf(combined_cf, fact_cf)

                    # Tambah kesimpulan ke working memory
                    working_memory.add_derived_fact(rule['THEN'], combined_cf)

                    # Catat reasoning trace
                    self.reasoning_trace.append({
                        'rule_id': rule_id,
                        'description': rule['description'],
                        'conditions': rule['IF'],
                        'conclusion': rule['THEN'],
                        'cf': combined_cf,
                        'iteration': iteration
                    })

                    used_rules.append(rule_id)
                    changed = True

        return working_memory.get_all_facts(), self.reasoning_trace

    def get_reasoning_trace(self) -> List:
        """Mendapatkan jejak penalaran"""
        return self.reasoning_trace


class CattleExpertSystem:
    """Sistem Pakar Utama"""

    def __init__(self):
        self.kb = KnowledgeBase()
        self.wm = WorkingMemory()
        self.ie = InferenceEngine(self.kb)
        self.consultation_history = []
        self.current_symptoms = {}  # Untuk menyimpan gejala yang dipilih

    def get_user_input(self):
        """Mengambil input dari pengguna"""
        print("\n" + "=" * 60)
        print("PEMERIKSAAN BIBIT SAPI POTONG")
        print("=" * 60)
        print("\nPilih kondisi yang sesuai dengan bibit sapi yang diamati:")
        print("(Tekan Enter untuk melewati, ketik 'selesai' untuk mengakhiri)\n")

        self.current_symptoms = {}  # Reset gejala

        # Eksklusif options untuk umur dan berat
        umur_options = ['umur_8_12_bulan', 'umur_kurang', 'umur_lebih']
        berat_options = ['berat_150_200kg', 'berat_kurang', 'berat_lebih']
        selected_umur = None
        selected_berat = None

        for category, symptoms in self.kb.symptom_database.items():
            print(f"\n{category}:")

            if category == 'Umur dan Berat':
                # Handle pilihan eksklusif untuk umur
                print("  Pilih salah satu untuk Umur:")
                umur_symptoms = [s for s in symptoms if s['id'] in umur_options]
                for i, symptom in enumerate(umur_symptoms, 1):
                    print(f"    {i}. {symptom['label']}")

                while True:
                    try:
                        umur_choice = input(f"    Pilih umur (1-{len(umur_symptoms)} atau Enter untuk skip): ")
                        if umur_choice == '':
                            break
                        umur_choice = int(umur_choice)
                        if 1 <= umur_choice <= len(umur_symptoms):
                            selected_symptom = umur_symptoms[umur_choice - 1]
                            # Hapus pilihan umur sebelumnya jika ada
                            for umur_id in umur_options:
                                if umur_id in self.current_symptoms:
                                    del self.current_symptoms[umur_id]
                            self.current_symptoms[selected_symptom['id']] = selected_symptom['cf']
                            selected_umur = selected_symptom['id']
                            break
                        else:
                            print("    Pilihan tidak valid!")
                    except ValueError:
                        print("    Masukkan angka yang valid!")

                # Handle pilihan eksklusif untuk berat
                print("  Pilih salah satu untuk Berat:")
                berat_symptoms = [s for s in symptoms if s['id'] in berat_options]
                for i, symptom in enumerate(berat_symptoms, 1):
                    print(f"    {i}. {symptom['label']}")

                while True:
                    try:
                        berat_choice = input(f"    Pilih berat (1-{len(berat_symptoms)} atau Enter untuk skip): ")
                        if berat_choice == '':
                            break
                        berat_choice = int(berat_choice)
                        if 1 <= berat_choice <= len(berat_symptoms):
                            selected_symptom = berat_symptoms[berat_choice - 1]
                            # Hapus pilihan berat sebelumnya jika ada
                            for berat_id in berat_options:
                                if berat_id in self.current_symptoms:
                                    del self.current_symptoms[berat_id]
                            self.current_symptoms[selected_symptom['id']] = selected_symptom['cf']
                            selected_berat = selected_symptom['id']
                            break
                        else:
                            print("    Pilihan tidak valid!")
                    except ValueError:
                        print("    Masukkan angka yang valid!")

            else:
                # Untuk kategori lainnya, gunakan input biasa
                for symptom in symptoms:
                    while True:
                        response = input(f"  {symptom['label']}? (y/t/selesai): ").lower()

                        if response == 'selesai':
                            return True
                        elif response in ['y', 'ya', 'yes']:
                            self.current_symptoms[symptom['id']] = symptom['cf']
                            break
                        elif response in ['t', 'tidak', 'no', '']:
                            break
                        else:
                            print("    Input tidak valid. Gunakan y/t/selesai")

        return True

    def diagnose(self) -> Dict:
        """Melakukan diagnosis - MENGGUNAKAN WEIGHTED SCORING SEPERTI STREAMLIT"""
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

        # Hitung weighted score seperti di Streamlit
        weighted_score = self.kb.calculate_weighted_score(self.current_symptoms)

        # Juga lakukan forward chaining untuk reasoning
        for symptom_id, cf in self.current_symptoms.items():
            self.wm.add_fact(symptom_id, cf)

        facts, trace = self.ie.forward_chaining(self.wm)

        # Tentukan kesimpulan berdasarkan WEIGHTED SCORE seperti di Streamlit
        if weighted_score >= 85:
            conclusion_label = 'Layak Dibeli - Grade Premium (A)'
            recommendation = 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.'
            grade = 'A'
            certainty = weighted_score / 100
        elif weighted_score >= 70:
            conclusion_label = 'Layak Dibeli - Grade Standar (B)'
            recommendation = 'Bibit direkomendasikan. Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.'
            grade = 'B'
            certainty = weighted_score / 100
        elif weighted_score >= 60:
            conclusion_label = 'Kualitas Baik (B)'
            recommendation = 'Bibit menunjukkan kualitas yang baik.'
            grade = 'B'
            certainty = weighted_score / 100
        elif weighted_score >= 50:
            conclusion_label = 'Potensial dengan Penggemukan (C)'
            recommendation = 'Bibit memiliki potensi namun perlu program penggemukan dan perawatan intensif selama 2-3 bulan.'
            grade = 'C'
            certainty = weighted_score / 100
        elif weighted_score >= 40:
            conclusion_label = 'Kualitas Cukup (C)'
            recommendation = 'Bibit menunjukkan kualitas cukup, perlu observasi lebih lanjut.'
            grade = 'C'
            certainty = weighted_score / 100
        elif weighted_score >= 30:
            conclusion_label = 'Perlu Perhatian Khusus (D)'
            recommendation = 'Bibit memerlukan perhatian dan perawatan khusus.'
            grade = 'D'
            certainty = weighted_score / 100
        else:
            conclusion_label = 'Tidak Direkomendasikan (E)'
            recommendation = 'Bibit tidak direkomendasikan untuk dibeli.'
            grade = 'E'
            certainty = weighted_score / 100

        best_conclusion = {
            'id': 'weighted_conclusion',
            'label': conclusion_label,
            'grade': grade,
            'cf': certainty,
            'score': weighted_score,
            'recommendation': recommendation
        }

        # Simpan ke history
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'conclusion': best_conclusion,
            'facts': facts,
            'reasoning_trace': trace,
            'weighted_score': weighted_score,
            'symptoms_used': len(self.current_symptoms)
        }

        self.consultation_history.append(result)

        return result

    def show_result(self, result: Dict):
        """Menampilkan hasil diagnosis"""
        print("\n" + "=" * 60)
        print("HASIL PENILAIAN BIBIT SAPI POTONG")
        print("=" * 60)

        conclusion = result['conclusion']
        weighted_score = result['weighted_score']
        symptoms_count = result['symptoms_used']

        print(f"\nKesimpulan: {conclusion['label']}")
        print(f"Grade: {conclusion['grade']}")
        print(f"Skor Kelayakan: {conclusion['score']}/100")
        print(f"Tingkat Kepercayaan: {int(conclusion['cf'] * 100)}%")
        print(f"Kriteria yang digunakan: {symptoms_count}")

        # Progress bar
        bar_length = 40
        filled = int(bar_length * conclusion['cf'])
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"[{bar}] {int(conclusion['cf'] * 100)}%")

        # Tampilkan warning berdasarkan jumlah kriteria (sama seperti Streamlit)
        if symptoms_count == 1:
            print(f"⚠️  PERINGATAN: Hasil berdasarkan hanya {symptoms_count} kriteria - Akurasi sangat terbatas")
        elif symptoms_count < 3:
            print(f"⚠️  PERINGATAN: Hasil berdasarkan {symptoms_count} kriteria - Akurasi rendah")
        elif symptoms_count < 5:
            print(
                f"⚠️  PERINGATAN: Hasil berdasarkan {symptoms_count} kriteria - Disarankan tambah lebih banyak kriteria")
        elif symptoms_count < 8:
            print(f"✅ Hasil berdasarkan {symptoms_count} kriteria - Tingkat akurasi baik")
        else:
            print(f"✅ Hasil berdasarkan {symptoms_count} kriteria - Tingkat akurasi optimal")

        print(f"\nRekomendasi:")
        print(f"{conclusion['recommendation']}")

        print("\n" + "-" * 60)

    def show_explanation_menu(self, result: Dict):
        """Menu penjelasan"""
        while True:
            print("\n" + "=" * 60)
            print("MENU PENJELASAN")
            print("=" * 60)
            print("1. Tampilkan Alur Penalaran Lengkap")
            print("2. Lihat Kriteria yang Digunakan")
            print("3. Kembali ke Menu Utama")

            choice = input("\nPilih menu (1-3): ")

            if choice == '1':
                print("\nALUR PENALARAN LENGKAP:")
                print("-" * 60)
                if not result['reasoning_trace']:
                    print("Tidak ada penalaran rule-based yang dijalankan.")
                    print("Sistem menggunakan weighted scoring berdasarkan kriteria SNI.")
                else:
                    for i, step in enumerate(result['reasoning_trace'], 1):
                        print(f"{i}. Rule {step['rule_id']}: {step['description']}")
                        print(f"   IF: {', '.join(step['conditions'])}")
                        print(f"   THEN: {step['conclusion']}")
                        print(f"   CF: {step['cf']:.2f}")
                        print()

                print(f"\nSKOR BERBOOT (Weighted Score): {result['weighted_score']}/100")
                print("Sistem menggunakan kombinasi bobot SNI untuk setiap kriteria.")
                input("\nTekan Enter untuk melanjutkan...")

            elif choice == '2':
                print("\nKRITERIA YANG DIGUNAKAN:")
                print("-" * 60)
                for symptom_id in self.current_symptoms.keys():
                    # Cari label yang sesuai
                    label = next((item['label'] for cat in self.kb.symptom_database.values() for item in cat if
                                  item['id'] == symptom_id), symptom_id)
                    print(f"- {label}")
                input("\nTekan Enter untuk melanjutkan...")

            elif choice == '3':
                break

    def export_report(self, result: Dict, filename: str = None):
        """Export hasil ke file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"laporan_penilaian_{timestamp}.txt"

        conclusion = result['conclusion']

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("LAPORAN PENILAIAN BIBIT SAPI POTONG\n")
            f.write("Sistem Pakar Berbasis Weighted Scoring\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Tanggal: {result['timestamp']}\n\n")

            f.write("HASIL PENILAIAN:\n")
            f.write("-" * 60 + "\n")
            f.write(f"Kesimpulan: {conclusion['label']}\n")
            f.write(f"Grade: {conclusion['grade']}\n")
            f.write(f"Skor Kelayakan: {conclusion['score']}/100\n")
            f.write(f"Tingkat Kepercayaan: {int(conclusion['cf'] * 100)}%\n")
            f.write(f"Kriteria yang digunakan: {result['symptoms_used']}\n\n")

            f.write("REKOMENDASI:\n")
            f.write("-" * 60 + "\n")
            f.write(f"{conclusion['recommendation']}\n\n")

            f.write("KONDISI YANG DIAMATI:\n")
            f.write("-" * 60 + "\n")
            for symptom_id in self.current_symptoms.keys():
                label = next((item['label'] for cat in self.kb.symptom_database.values() for item in cat if
                              item['id'] == symptom_id), symptom_id)
                f.write(f"- {label}\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write("METODE PENILAIAN:\n")
            f.write("=" * 60 + "\n")
            f.write("Sistem menggunakan weighted scoring berdasarkan Standar Nasional Indonesia (SNI)\n")
            f.write("dengan bobot yang telah ditentukan untuk setiap kriteria.\n")
            f.write(f"Skor akhir: {result['weighted_score']}/100\n")

        print(f"\nLaporan berhasil disimpan ke: {filename}")

    def show_history(self):
        """Menampilkan riwayat konsultasi"""
        print("\n" + "=" * 60)
        print("RIWAYAT KONSULTASI")
        print("=" * 60)

        if not self.consultation_history:
            print("\nBelum ada riwayat konsultasi.")
            return

        for i, record in enumerate(self.consultation_history, 1):
            print(f"\n{i}. {record['timestamp']}")
            print(f"   Kesimpulan: {record['conclusion']['label']}")
            print(f"   Grade: {record['conclusion']['grade']}")
            print(f"   Skor: {record['conclusion']['score']}/100")

    def knowledge_acquisition_menu(self):
        """Menu akuisisi pengetahuan"""
        while True:
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
                filename = input("Nama file (default: knowledge_base.json): ") or 'knowledge_base.json'
                self.kb.save_to_file(filename)
                print(f"Basis pengetahuan disimpan ke {filename}")
            elif choice == '6':
                filename = input("Nama file (default: knowledge_base.json): ") or 'knowledge_base.json'
                self.kb.load_from_file(filename)
                print(f"Basis pengetahuan dimuat dari {filename}")
            elif choice == '7':
                break

    def show_all_rules(self):
        """Menampilkan semua rule"""
        print("\n" + "=" * 60)
        print("DAFTAR RULE")
        print("=" * 60)

        for rule_id, rule in self.kb.get_all_rules().items():
            print(f"\n{rule_id}: {rule['description']}")
            print(f"  IF: {', '.join(rule['IF'])}")
            print(f"  THEN: {rule['THEN']}")
            print(f"  CF: {rule['CF']}")

    def add_new_rule(self):
        """Menambah rule baru"""
        print("\n" + "=" * 60)
        print("TAMBAH RULE BARU")
        print("=" * 60)

        rule_id = input("ID Rule (contoh: R16): ").upper()
        if rule_id in self.kb.rules:
            print("Rule ID sudah ada!")
            return

        description = input("Deskripsi: ")

        print("Kondisi IF (pisahkan dengan koma):")
        conditions = [c.strip() for c in input().split(',')]

        conclusion = input("Kesimpulan THEN: ")

        cf = float(input("Certainty Factor (0.0-1.0): "))

        new_rule = {
            'IF': conditions,
            'THEN': conclusion,
            'CF': cf,
            'description': description
        }

        if self.kb.add_rule(rule_id, new_rule):
            print(f"Rule {rule_id} berhasil ditambahkan!")
        else:
            print("Gagal menambahkan rule.")

    def edit_rule(self):
        """Edit rule yang ada"""
        print("\n" + "=" * 60)
        print("EDIT RULE")
        print("=" * 60)

        rule_id = input("ID Rule yang akan diedit: ").upper()
        if rule_id not in self.kb.rules:
            print("Rule tidak ditemukan!")
            return

        rule = self.kb.rules[rule_id]
        print(f"\nRule saat ini:")
        print(f"Deskripsi: {rule['description']}")
        print(f"IF: {', '.join(rule['IF'])}")
        print(f"THEN: {rule['THEN']}")
        print(f"CF: {rule['CF']}")

        print("\n(Tekan Enter untuk mempertahankan nilai lama)")

        description = input(f"Deskripsi baru: ") or rule['description']

        conditions_input = input(f"Kondisi IF baru (pisahkan dengan koma): ")
        conditions = [c.strip() for c in conditions_input.split(',')] if conditions_input else rule['IF']

        conclusion = input(f"Kesimpulan THEN baru: ") or rule['THEN']

        cf_input = input(f"CF baru (0.0-1.0): ")
        cf = float(cf_input) if cf_input else rule['CF']

        updated_rule = {
            'IF': conditions,
            'THEN': conclusion,
            'CF': cf,
            'description': description
        }

        self.kb.update_rule(rule_id, updated_rule)
        print(f"Rule {rule_id} berhasil diupdate!")

    def delete_rule(self):
        """Hapus rule"""
        print("\n" + "=" * 60)
        print("HAPUS RULE")
        print("=" * 60)

        rule_id = input("ID Rule yang akan dihapus: ").upper()

        confirm = input(f"Yakin ingin menghapus {rule_id}? (y/n): ")
        if confirm.lower() == 'y':
            if self.kb.delete_rule(rule_id):
                print(f"Rule {rule_id} berhasil dihapus!")
            else:
                print("Rule tidak ditemukan!")

    def run(self):
        """Menjalankan sistem pakar"""
        print("\n" + "=" * 60)
        print("SISTEM PAKAR PENILAIAN BIBIT SAPI POTONG")
        print("Berbasis Standar Nasional Indonesia (SNI)")
        print("Kelompok 6 - INF313 Kecerdasan Artifisial")
        print("=" * 60)
        print("\nSISTEM TERINTEGRASI DENGAN STREAMLIT")
        print("Menggunakan Weighted Scoring Method")

        while True:
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
                self.wm.clear()
                if self.get_user_input():
                    result = self.diagnose()
                    self.show_result(result)

                    show_exp = input("\nTampilkan penjelasan? (y/n): ")
                    if show_exp.lower() == 'y':
                        self.show_explanation_menu(result)

                    export = input("\nExport laporan ke file? (y/n): ")
                    if export.lower() == 'y':
                        self.export_report(result)

            elif choice == '2':
                self.show_history()
                input("\nTekan Enter untuk melanjutkan...")

            elif choice == '3':
                self.knowledge_acquisition_menu()

            elif choice == '4':
                self.show_about()
                input("\nTekan Enter untuk melanjutkan...")

            elif choice == '5':
                print("\nTerima kasih telah menggunakan sistem ini!")
                break

            else:
                print("\nPilihan tidak valid!")

    def show_about(self):
        """Menampilkan informasi tentang sistem"""
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
        print("- Export laporan konsultasi"
        print("- Riwayat konsultasi")
        print("\nStandar Acuan:")
        print("SNI 7651.6:2015 - Bibit Sapi Potong")


def main():
    """Fungsi utama"""
    system = CattleExpertSystem()
    system.run()


if __name__ == "__main__":
    main()