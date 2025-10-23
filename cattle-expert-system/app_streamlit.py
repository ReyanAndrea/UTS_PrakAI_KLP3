# # """
# # Sistem Pakar Penilaian Kualitas Bibit Sapi Potong
# # Berbasis Standar Nasional Indonesia (SNI)
# # Web Version with Streamlit
# # Kelompok 6 - INF313 Kecerdasan Artifisial
# # """
# #
# import streamlit as st
# import json
# import csv
# import io
# from datetime import datetime
# from typing import Dict, List, Tuple
#
# # Set page config
# st.set_page_config(
#     page_title="Sistem Pakar Bibit Sapi Potong",
#     page_icon="🐄",
#     layout="wide"
# )
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
#                 {'id': 'umur_kurang', 'label': 'Umur kurang dari 8 bulan', 'cf': 0.6},
#                 {'id': 'berat_150_200kg', 'label': 'Berat 150-200 kg', 'cf': 0.9},
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
#             self.derived_facts[fact] = self.combine_cf(self.derived_facts[fact], cf)
#         else:
#             self.derived_facts[fact] = cf
#
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
# class InferenceEngine:
#     """Mesin Inferensi - Forward Chaining"""
#
#     def __init__(self, knowledge_base: KnowledgeBase):
#         self.kb = knowledge_base
#         self.reasoning_trace = []
#
#     def forward_chaining(self, working_memory: WorkingMemory) -> Tuple[Dict, List]:
#         """Forward Chaining (Data-Driven Reasoning)"""
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
#             for rule_id, rule in self.kb.rules.items():
#                 if rule_id in used_rules:
#                     continue
#
#                 all_conditions_met = all(
#                     working_memory.has_fact(condition)
#                     for condition in rule['IF']
#                 )
#
#                 if all_conditions_met:
#                     combined_cf = rule['CF']
#                     for condition in rule['IF']:
#                         fact_cf = working_memory.get_fact(condition)
#                         combined_cf = working_memory.combine_cf(combined_cf, fact_cf)
#
#                     working_memory.add_derived_fact(rule['THEN'], combined_cf)
#
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
# def export_to_txt(result: Dict, kb: KnowledgeBase) -> str:
#     """Export hasil ke format TXT"""
#     output = []
#     output.append("=" * 60)
#     output.append("LAPORAN PENILAIAN BIBIT SAPI POTONG")
#     output.append("Sistem Pakar Berbasis Rule-Based")
#     output.append("=" * 60)
#     output.append("")
#     output.append(f"Tanggal: {result['timestamp']}")
#     output.append("")
#     output.append("HASIL PENILAIAN:")
#     output.append("-" * 60)
#     output.append(f"Kesimpulan: {result['conclusion']['label']}")
#     output.append(f"Grade: {result['conclusion']['grade']}")
#     output.append(f"Skor Kelayakan: {result['conclusion']['score']}/100")
#     output.append(f"Tingkat Kepercayaan: {int(result['conclusion']['cf'] * 100)}%")
#     output.append("")
#     output.append("REKOMENDASI:")
#     output.append("-" * 60)
#     output.append(result['conclusion']['recommendation'])
#     output.append("")
#     output.append("KONDISI YANG DIAMATI:")
#     output.append("-" * 60)
#
#     for fact_id, cf in result['selected_facts'].items():
#         for category, symptoms in kb.symptom_database.items():
#             for symptom in symptoms:
#                 if symptom['id'] == fact_id:
#                     output.append(f"- {symptom['label']} (CF: {cf:.2f})")
#                     break
#
#     if result['trace']:
#         output.append("")
#         output.append("=" * 60)
#         output.append("PROSES PENALARAN:")
#         output.append("=" * 60)
#         output.append("")
#
#         for i, step in enumerate(result['trace'], 1):
#             output.append(f"Langkah {i}:")
#             output.append(f"  Rule: {step['rule_id']} - {step['description']}")
#             output.append(f"  IF: {', '.join(step['conditions'])}")
#             output.append(f"  THEN: {step['conclusion']}")
#             output.append(f"  CF: {step['cf']:.2f}")
#             output.append("")
#
#     return "\n".join(output)
#
# def export_to_json(result: Dict) -> str:
#     """Export hasil ke format JSON"""
#     export_data = {
#         'timestamp': result['timestamp'],
#         'conclusion': {
#             'label': result['conclusion']['label'],
#             'grade': result['conclusion']['grade'],
#             'score': result['conclusion']['score'],
#             'cf': result['conclusion']['cf'],
#             'recommendation': result['conclusion']['recommendation']
#         },
#         'selected_conditions': [
#             {'id': fact_id, 'cf': cf}
#             for fact_id, cf in result['selected_facts'].items()
#         ],
#         'reasoning_trace': result['trace']
#     }
#     return json.dumps(export_data, indent=2, ensure_ascii=False)
#
# def export_to_csv(result: Dict, kb: KnowledgeBase) -> str:
#     """Export hasil ke format CSV"""
#     output = io.StringIO()
#     writer = csv.writer(output)
#
#     # Header
#     writer.writerow(['LAPORAN PENILAIAN BIBIT SAPI POTONG'])
#     writer.writerow(['Tanggal', result['timestamp']])
#     writer.writerow([])
#
#     # Hasil Penilaian
#     writer.writerow(['HASIL PENILAIAN'])
#     writer.writerow(['Kesimpulan', result['conclusion']['label']])
#     writer.writerow(['Grade', result['conclusion']['grade']])
#     writer.writerow(['Skor', result['conclusion']['score']])
#     writer.writerow(['Tingkat Kepercayaan (%)', int(result['conclusion']['cf'] * 100)])
#     writer.writerow(['Rekomendasi', result['conclusion']['recommendation']])
#     writer.writerow([])
#
#     # Kondisi yang diamati
#     writer.writerow(['KONDISI YANG DIAMATI'])
#     writer.writerow(['Kondisi', 'Certainty Factor'])
#
#     for fact_id, cf in result['selected_facts'].items():
#         for category, symptoms in kb.symptom_database.items():
#             for symptom in symptoms:
#                 if symptom['id'] == fact_id:
#                     writer.writerow([symptom['label'], f"{cf:.2f}"])
#                     break
#
#     writer.writerow([])
#
#     # Proses Penalaran
#     if result['trace']:
#         writer.writerow(['PROSES PENALARAN'])
#         writer.writerow(['Step', 'Rule ID', 'Description', 'Conclusion', 'CF'])
#
#         for i, step in enumerate(result['trace'], 1):
#             writer.writerow([
#                 i,
#                 step['rule_id'],
#                 step['description'],
#                 step['conclusion'],
#                 f"{step['cf']:.2f}"
#             ])
#
#     return output.getvalue()
#
# def determine_conclusion(facts: Dict, trace: List, selected_count: int) -> Dict:
#     """Menentukan kesimpulan dengan logic yang lebih baik"""
#
#     conclusions = {
#         'bibit_unggul': {
#             'label': 'Bibit Unggul Kelas Premium',
#             'grade': 'A+',
#             'recommendation': 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas premium. Sangat cocok untuk breeding atau penggemukan intensif dengan potensi keuntungan tinggi.'
#         },
#         'layak_dibeli_premium': {
#             'label': 'Layak Dibeli - Grade Premium',
#             'grade': 'A',
#             'recommendation': 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.'
#         },
#         'kualitas_sangat_baik': {
#             'label': 'Kualitas Sangat Baik',
#             'grade': 'A',
#             'recommendation': 'Bibit memenuhi standar SNI Grade A dengan karakteristik fisik dan kesehatan excellent.'
#         },
#         'layak_dibeli_standar': {
#             'label': 'Layak Dibeli - Grade Standar',
#             'grade': 'B',
#             'recommendation': 'Bibit direkomendasikan. Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.'
#         },
#         'kualitas_baik': {
#             'label': 'Kualitas Baik',
#             'grade': 'B',
#             'recommendation': 'Bibit memenuhi standar SNI Grade B dengan karakteristik yang baik.'
#         },
#         'perlu_penggemukan': {
#             'label': 'Potensial dengan Penggemukan',
#             'grade': 'C',
#             'recommendation': 'Bibit memiliki potensi namun memerlukan program penggemukan dan perawatan intensif selama 2-3 bulan.'
#         }
#     }
#
#     # Cari kesimpulan dengan CF tertinggi
#     best_conclusion = None
#     best_cf = 0.0
#
#     for conclusion_id, conclusion_data in conclusions.items():
#         if conclusion_id in facts and facts[conclusion_id] > best_cf:
#             best_cf = facts[conclusion_id]
#             best_conclusion = {
#                 'id': conclusion_id,
#                 'label': conclusion_data['label'],
#                 'grade': conclusion_data['grade'],
#                 'cf': best_cf,
#                 'score': int(best_cf * 100),
#                 'recommendation': conclusion_data['recommendation']
#             }
#
#     # LOGIC BARU: Hitung berdasarkan fakta yang dipilih jika tidak ada kesimpulan
#     if best_conclusion is None or best_cf < 0.3:
#         if selected_count == 0:
#             return {
#                 'id': 'no_data',
#                 'label': 'Belum Ada Data',
#                 'grade': 'N/A',
#                 'cf': 0.0,
#                 'score': 0,
#                 'recommendation': 'Silakan pilih minimal satu kondisi untuk memulai penilaian.'
#             }
#
#         # Hitung rata-rata CF dari fakta yang dipilih user
#         selected_facts = {k: v for k, v in facts.items() if k in st.session_state.get('selected_facts', {})}
#         if selected_facts:
#             avg_cf = sum(selected_facts.values()) / len(selected_facts)
#         else:
#             avg_cf = 0.5
#
#         # Tentukan grade berdasarkan CF
#         if avg_cf >= 0.8:
#             grade = 'B+'
#             label = 'Kualitas Cukup Baik'
#             recommendation = 'Bibit menunjukkan beberapa karakteristik baik. Perlu evaluasi lebih lengkap untuk penilaian optimal.'
#         elif avg_cf >= 0.7:
#             grade = 'B'
#             label = 'Kualitas Sedang'
#             recommendation = 'Bibit menunjukkan karakteristik standar. Disarankan melengkapi pemeriksaan untuk hasil lebih akurat.'
#         elif avg_cf >= 0.6:
#             grade = 'C+'
#             label = 'Kualitas Cukup'
#             recommendation = 'Bibit memiliki potensi namun perlu pemeriksaan lebih menyeluruh dan mungkin memerlukan perawatan tambahan.'
#         else:
#             grade = 'C'
#             label = 'Perlu Evaluasi Lebih Lanjut'
#             recommendation = 'Bibit perlu pemeriksaan lebih lengkap. Beberapa karakteristik perlu ditingkatkan.'
#
#         best_conclusion = {
#             'id': 'partial_evaluation',
#             'label': label,
#             'grade': grade,
#             'cf': avg_cf,
#             'score': int(avg_cf * 100),
#             'recommendation': f"{recommendation} (Berdasarkan {selected_count} kriteria yang dipilih)"
#         }
#
#     return best_conclusion
#
# def main():
#     # Initialize session state
#     if 'kb' not in st.session_state:
#         st.session_state.kb = KnowledgeBase()
#         st.session_state.wm = WorkingMemory()
#         st.session_state.ie = InferenceEngine(st.session_state.kb)
#         st.session_state.selected_facts = {}
#         st.session_state.result = None
#         st.session_state.history = []
#
#     # Header
#     st.title("🐄 Sistem Pakar Penilaian Bibit Sapi Potong")
#     st.markdown("**Berbasis Standar Nasional Indonesia (SNI) - Kelompok 6**")
#     st.divider()
#
#     # Tabs
#     tab1, tab2, tab3 = st.tabs(["📋 Konsultasi", "📜 Riwayat", "ℹ️ Tentang"])
#
#     with tab1:
#         st.header("Pemeriksaan Bibit Sapi Potong")
#         st.info("Pilih semua kondisi yang sesuai dengan bibit sapi yang diamati")
#
#         # Display symptoms by category
#         for category, symptoms in st.session_state.kb.symptom_database.items():
#             st.subheader(f"🔹 {category}")
#
#             # LOGIC BARU: Filter symptoms untuk Umur dan Berat
#             filtered_symptoms = symptoms.copy()
#             if category == 'Umur dan Berat':
#                 # Jika sudah pilih umur 8-12 bulan, hide umur kurang
#                 if 'umur_8_12_bulan' in st.session_state.selected_facts:
#                     filtered_symptoms = [s for s in filtered_symptoms if s['id'] != 'umur_kurang']
#                 # Jika sudah pilih umur kurang, hide umur 8-12
#                 if 'umur_kurang' in st.session_state.selected_facts:
#                     filtered_symptoms = [s for s in filtered_symptoms if s['id'] != 'umur_8_12_bulan']
#
#                 # Jika sudah pilih berat 150-200, hide berat kurang
#                 if 'berat_150_200kg' in st.session_state.selected_facts:
#                     filtered_symptoms = [s for s in filtered_symptoms if s['id'] != 'berat_kurang']
#                 # Jika sudah pilih berat kurang, hide berat 150-200
#                 if 'berat_kurang' in st.session_state.selected_facts:
#                     filtered_symptoms = [s for s in filtered_symptoms if s['id'] != 'berat_150_200kg']
#
#             cols = st.columns(2)
#             for idx, symptom in enumerate(filtered_symptoms):
#                 with cols[idx % 2]:
#                     is_checked = symptom['id'] in st.session_state.selected_facts
#                     if st.checkbox(
#                         symptom['label'],  # Removed CF display
#                         value=is_checked,
#                         key=symptom['id']
#                     ):
#                         st.session_state.selected_facts[symptom['id']] = symptom['cf']
#                     else:
#                         if symptom['id'] in st.session_state.selected_facts:
#                             del st.session_state.selected_facts[symptom['id']]
#
#         st.divider()
#
#         # Buttons
#         col1, col2 = st.columns([3, 1])
#         with col1:
#             if st.button("🔍 Diagnosa Sekarang", type="primary", use_container_width=True):
#                 # Clear working memory
#                 st.session_state.wm.clear()
#
#                 # Add selected facts to working memory
#                 for fact_id, cf in st.session_state.selected_facts.items():
#                     st.session_state.wm.add_fact(fact_id, cf)
#
#                 # Run forward chaining
#                 facts, trace = st.session_state.ie.forward_chaining(st.session_state.wm)
#
#                 # Determine conclusion
#                 selected_count = len(st.session_state.selected_facts)
#                 conclusion = determine_conclusion(facts, trace, selected_count)
#
#                 # Save result
#                 result = {
#                     'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                     'conclusion': conclusion,
#                     'facts': facts,
#                     'trace': trace,
#                     'selected_facts': st.session_state.selected_facts.copy()
#                 }
#
#                 st.session_state.result = result
#                 st.session_state.history.insert(0, result)
#
#                 st.rerun()
#
#         with col2:
#             if st.button("🔄 Reset", use_container_width=True):
#                 st.session_state.selected_facts = {}
#                 st.session_state.result = None
#                 st.rerun()
#
#         # Display Result
#         if st.session_state.result:
#             st.divider()
#             st.header("📊 Hasil Penilaian")
#
#             result = st.session_state.result
#             conclusion = result['conclusion']
#
#             # Grade badge
#             col1, col2 = st.columns([1, 3])
#             with col1:
#                 grade_color = {
#                     'A+': '🟢', 'A': '🟢',
#                     'B+': '🔵', 'B': '🔵',
#                     'C+': '🟡', 'C': '🟡',
#                     'N/A': '⚪'
#                 }
#                 grade_emoji = grade_color.get(conclusion['grade'], '⚪')
#                 st.markdown(f"### {grade_emoji} Grade **{conclusion['grade']}**")
#
#             with col2:
#                 st.markdown(f"### {conclusion['label']}")
#                 st.markdown(f"**Skor Kelayakan:** {conclusion['score']}/100")
#
#             # Progress bar
#             st.progress(conclusion['cf'], text=f"Tingkat Kepercayaan: {int(conclusion['cf'] * 100)}%")
#
#             # Recommendation
#             st.success(f"**Rekomendasi:** {conclusion['recommendation']}")
#
#             # Download buttons
#             st.divider()
#             st.subheader("💾 Download Hasil")
#             col1, col2, col3 = st.columns(3)
#
#             with col1:
#                 txt_data = export_to_txt(result, st.session_state.kb)
#                 st.download_button(
#                     label="📄 Download TXT",
#                     data=txt_data,
#                     file_name=f"laporan_sapi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#                     mime="text/plain",
#                     use_container_width=True
#                 )
#
#             with col2:
#                 json_data = export_to_json(result)
#                 st.download_button(
#                     label="📋 Download JSON",
#                     data=json_data,
#                     file_name=f"laporan_sapi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#                     mime="application/json",
#                     use_container_width=True
#                 )
#
#             with col3:
#                 csv_data = export_to_csv(result, st.session_state.kb)
#                 st.download_button(
#                     label="📊 Download CSV",
#                     data=csv_data,
#                     file_name=f"laporan_sapi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )
#
#             # Explanation
#             with st.expander("📄 Lihat Penjelasan Detail"):
#                 st.subheader("Kondisi yang Dipilih:")
#                 for fact_id, cf in result['selected_facts'].items():
#                     # Find symptom label
#                     for category, symptoms in st.session_state.kb.symptom_database.items():
#                         for symptom in symptoms:
#                             if symptom['id'] == fact_id:
#                                 st.write(f"✓ {symptom['label']} (CF: {cf:.2f})")
#                                 break
#
#                 if result['trace']:
#                     st.divider()
#                     st.subheader("Proses Penalaran:")
#                     for i, step in enumerate(result['trace'], 1):
#                         st.write(f"**{i}. {step['rule_id']}:** {step['description']}")
#                         st.write(f"   → Kesimpulan: {step['conclusion'].replace('_', ' ').title()} (CF: {step['cf']:.2f})")
#
#     with tab2:
#         st.header("📜 Riwayat Konsultasi")
#
#         if not st.session_state.history:
#             st.info("Belum ada riwayat konsultasi")
#         else:
#             for i, record in enumerate(st.session_state.history):
#                 with st.container():
#                     col1, col2, col3 = st.columns([2, 1, 1])
#                     with col1:
#                         st.write(f"**{record['timestamp']}**")
#                         st.write(record['conclusion']['label'])
#                     with col2:
#                         st.metric("Grade", record['conclusion']['grade'])
#                     with col3:
#                         st.metric("Skor", f"{record['conclusion']['score']}/100")
#                     st.divider()
#
#     with tab3:
#         st.header("ℹ️ Tentang Sistem")
#
#         st.markdown("""
#         ### Sistem Pakar Penilaian Kualitas Bibit Sapi Potong
#         Berbasis Rule-Based System dengan Forward Chaining
#
#         #### 👥 Kelompok 6:
#         1. YUYUN NAILUFAR
#         2. MUHAMMAD RAZI SIREGAR
#         3. REYAN ANDREA
#         4. FIRAH MAULIDA
#         5. IKRAM AL GHIFFARI
#         6. DIO FERDI JAYA
#
#         #### 📚 Mata Kuliah
#         **INF313 - Kecerdasan Artifisial**
#
#         #### ✨ Fitur Sistem:
#         - Forward Chaining Inference Engine
#         - Certainty Factor untuk ketidakpastian
#         - Explanation Facility (WHY & HOW)
#         - Riwayat konsultasi
#         - Interface web yang user-friendlyy
#
#         #### 📋 Standar Acuan:
#         SNI 7651.6:2015 - Bibit Sapi Potong
#
#         #### 🔧 Technology Stack:
#         - Python 3.x
#         - Streamlit
#         - Rule-Based Expert System
#         """)
#
# if __name__ == "__main__":
#     main()

import streamlit as st
import json
from datetime import datetime

# =============================================================================
# KONFIGURASI HALAMAN
# =============================================================================
st.set_page_config(
    page_title="Sistem Pakar Bibit Sapi Potong",
    page_icon="🐮",
    layout="wide"
)

# =============================================================================
# BASIS PENGETAHUAN (KNOWLEDGE BASE)
# =============================================================================
INITIAL_RULES = {
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
        'IF': ['umur_8_12_bulan'],
        'THEN': 'umur_ideal',
        'CF': 0.9,
        'description': 'Umur sesuai standar bibit'
    },
    'R4': {
        'IF': ['berat_150_200kg'],
        'THEN': 'berat_ideal',
        'CF': 0.9,
        'description': 'Berat sesuai standar bibit'
    },
    'R5': {
        'IF': ['riwayat_vaksin_lengkap', 'tidak_ada_penyakit'],
        'THEN': 'riwayat_kesehatan_baik',
        'CF': 0.95,
        'description': 'Riwayat kesehatan terdokumentasi baik'
    },
    'R6': {
        'IF': ['indikator_fisik_baik', 'indikator_kesehatan_baik', 'umur_ideal', 'berat_ideal'],
        'THEN': 'kualitas_sangat_baik',
        'CF': 0.95,
        'description': 'Bibit memenuhi kriteria SNI kualitas A'
    },
    'R7': {
        'IF': ['indikator_fisik_baik', 'indikator_kesehatan_baik', 'umur_ideal'],
        'THEN': 'kualitas_baik',
        'CF': 0.8,
        'description': 'Bibit memenuhi kriteria SNI kualitas B'
    },
    'R8': {
        'IF': ['punggung_rata', 'perut_tidak_buncit', 'ekor_panjang'],
        'THEN': 'konformasi_baik',
        'CF': 0.8,
        'description': 'Konformasi tubuh sesuai standar'
    },
    'R9': {
        'IF': ['konformasi_baik', 'indikator_fisik_baik'],
        'THEN': 'struktur_tubuh_ideal',
        'CF': 0.85,
        'description': 'Struktur tubuh memenuhi standar breeding'
    },
    'R10': {
        'IF': ['nafsu_makan_baik', 'aktif_bergerak', 'tidak_lemas'],
        'THEN': 'perilaku_normal',
        'CF': 0.8,
        'description': 'Perilaku menunjukkan kondisi sehat'
    },
    'R11': {
        'IF': ['struktur_tubuh_ideal', 'riwayat_kesehatan_baik', 'perilaku_normal', 'umur_ideal', 'berat_ideal'],
        'THEN': 'layak_dibeli_premium',
        'CF': 0.98,
        'description': 'Sangat direkomendasikan untuk pembelian premium'
    },
    'R12': {
        'IF': ['kualitas_baik', 'riwayat_kesehatan_baik'],
        'THEN': 'layak_dibeli_standar',
        'CF': 0.8,
        'description': 'Direkomendasikan untuk pembelian standar'
    },
    'R13': {
        'IF': ['umur_kurang', 'berat_kurang'],
        'THEN': 'perlu_penggemukan',
        'CF': 0.7,
        'description': 'Bibit potensial namun perlu perawatan intensif'
    },
    'R14': {
        'IF': ['umur_lebih', 'berat_lebih'],
        'THEN': 'terlalu_tua',
        'CF': 0.6,
        'description': 'Bibit sudah melewati usia ideal'
    }
}

# Definisikan bobot untuk setiap kriteria
CRITERIA_WEIGHTS = {
    'Postur Fisik': {
        'postur_tegak': 15,
        'dada_lebar': 12,
        'kaki_kuat': 13,
        'punggung_rata': 10,
        'perut_tidak_buncit': 8,
        'ekor_panjang': 7
    },
    'Kondisi Kesehatan': {
        'mata_cerah': 10,
        'hidung_basah': 8,
        'bulu_mengkilap': 7,
        'tidak_ada_penyakit': 15,
        'riwayat_vaksin_lengkap': 12
    },
    'Umur': {
        'umur_8_12_bulan': 20,
        'umur_kurang': 5,
        'umur_lebih': 8
    },
    'Berat': {
        'berat_150_200kg': 20,
        'berat_kurang': 5,
        'berat_lebih': 10
    },
    'Perilaku': {
        'nafsu_makan_baik': 12,
        'aktif_bergerak': 10,
        'tidak_lemas': 11
    }
}

SYMPTOM_CATEGORIES = {
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
    'Umur': [
        {'id': 'umur_8_12_bulan', 'label': 'Umur 8-12 bulan', 'cf': 0.9},
        {'id': 'umur_kurang', 'label': 'Umur kurang dari 8 bulan', 'cf': 0.6},
        {'id': 'umur_lebih', 'label': 'Umur lebih dari 12 bulan', 'cf': 0.7}
    ],
    'Berat': [
        {'id': 'berat_150_200kg', 'label': 'Berat 150-200 kg', 'cf': 0.9},
        {'id': 'berat_kurang', 'label': 'Berat kurang dari 150 kg', 'cf': 0.6},
        {'id': 'berat_lebih', 'label': 'Berat lebih dari 200 kg', 'cf': 0.7}
    ],
    'Perilaku': [
        {'id': 'nafsu_makan_baik', 'label': 'Nafsu makan baik', 'cf': 0.85},
        {'id': 'aktif_bergerak', 'label': 'Aktif bergerak', 'cf': 0.8},
        {'id': 'tidak_lemas', 'label': 'Tidak tampak lemas', 'cf': 0.85}
    ]
}

EXCLUSIVE_OPTIONS = {
    'umur': ['umur_8_12_bulan', 'umur_kurang', 'umur_lebih'],
    'berat': ['berat_150_200kg', 'berat_kurang', 'berat_lebih']
}

CONCLUSIONS = [
    {
        'id': 'layak_dibeli_premium',
        'label': 'Layak Dibeli - Grade Premium (A)',
        'recommendation': 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.',
        'min_score': 85
    },
    {
        'id': 'layak_dibeli_standar',
        'label': 'Layak Dibeli - Grade Standar (B)',
        'recommendation': 'Bibit direkomendasikan. Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.',
        'min_score': 70
    },
    {
        'id': 'kualitas_sangat_baik',
        'label': 'Kualitas Sangat Baik (A)',
        'recommendation': 'Bibit memenuhi standar SNI Grade A dengan karakteristik fisik dan kesehatan excellent.',
        'min_score': 80
    },
    {
        'id': 'kualitas_baik',
        'label': 'Kualitas Baik (B)',
        'recommendation': 'Bibit memenuhi standar SNI Grade B dengan karakteristik yang baik.',
        'min_score': 65
    },
    {
        'id': 'perlu_penggemukan',
        'label': 'Potensial dengan Penggemukan (C)',
        'recommendation': 'Bibit memiliki potensi namun memerlukan program penggemukan dan perawatan intensif selama 2-3 bulan.',
        'min_score': 50
    }
]

# =============================================================================
# INISIALISASI SESSION STATE
# =============================================================================
if 'symptoms' not in st.session_state:
    st.session_state.symptoms = {}
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = None
if 'reasoning' not in st.session_state:
    st.session_state.reasoning = []
if 'consultation_history' not in st.session_state:
    st.session_state.consultation_history = []
if 'rules' not in st.session_state:
    st.session_state.rules = INITIAL_RULES
if 'selected_umur' not in st.session_state:
    st.session_state.selected_umur = None
if 'selected_berat' not in st.session_state:
    st.session_state.selected_berat = None
if 'temp_symptoms' not in st.session_state:
    st.session_state.temp_symptoms = {}


# =============================================================================
# FUNGSI UTILITAS
# =============================================================================
def calculate_cf(cf1, cf2):
    """Menghitung Certainty Factor gabungan."""
    return cf1 + cf2 * (1 - cf1)


def handle_exclusive_selection(category, selected_id, temp_symptoms):
    """Menangani pilihan eksklusif untuk umur dan berat."""
    if category == 'umur':
        for umur_id in EXCLUSIVE_OPTIONS['umur']:
            if umur_id in temp_symptoms:
                del temp_symptoms[umur_id]
        if selected_id:
            item = next((item for cat in SYMPTOM_CATEGORIES.values() for item in cat if item['id'] == selected_id),
                        None)
            if item:
                temp_symptoms[selected_id] = item['cf']

    elif category == 'berat':
        for berat_id in EXCLUSIVE_OPTIONS['berat']:
            if berat_id in temp_symptoms:
                del temp_symptoms[berat_id]
        if selected_id:
            item = next((item for cat in SYMPTOM_CATEGORIES.values() for item in cat if item['id'] == selected_id),
                        None)
            if item:
                temp_symptoms[selected_id] = item['cf']

    return temp_symptoms


def reset_consultation():
    """Mereset state konsultasi."""
    st.session_state.symptoms = {}
    st.session_state.diagnosis = None
    st.session_state.reasoning = []
    st.session_state.selected_umur = None
    st.session_state.selected_berat = None
    st.session_state.temp_symptoms = {}


def get_export_string():
    """Membuat string teks untuk diunduh."""
    diag = st.session_state.diagnosis
    reas = st.session_state.reasoning
    symp = st.session_state.symptoms

    if not diag:
        return "Belum ada diagnosis."

    symptom_list = "\n".join([f"- {s.replace('_', ' ').capitalize()}" for s in symp.keys()])
    reasoning_list = "\n".join(
        [f"{i + 1}. {r['rule']}: {r['description']} (CF: {r['cf']})" for i, r in enumerate(reas)])

    content = f"""
LAPORAN PENILAIAN BIBIT SAPI POTONG
Tanggal: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

HASIL PENILAIAN:
Kesimpulan: {diag['conclusion']}
Skor Kelayakan: {diag['score']}/100
Tingkat Kepercayaan: {round(diag['certainty'] * 100)}%

REKOMENDASI:
{diag['recommendation']}

KRITERIA YANG DIAMATI:
{symptom_list}

PROSES PENALARAN:
{reasoning_list}
    """.strip()
    return content


# =============================================================================
# MESIN INFERENSI (INFERENCE ENGINE)
# =============================================================================
def calculate_weighted_score(symptoms_input):
    """Menghitung skor berbobot berdasarkan kriteria yang dipilih"""
    if not symptoms_input:
        return 0

    total_score = 0
    max_possible_score = 0

    # Hitung skor aktual dan skor maksimal
    for symptom_id, symptom_cf in symptoms_input.items():
        # Cari bobot untuk gejala ini
        weight = 0
        for category, weights in CRITERIA_WEIGHTS.items():
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

    # PENALTI untuk kriteria yang kurang
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


def forward_chaining(symptoms_input, rules):
    """Melakukan forward chaining berdasarkan gejala yang dipilih"""
    working_memory = symptoms_input.copy()
    used_rules = []
    changed = True
    iterations = 0
    max_iterations = 15

    while changed and iterations < max_iterations:
        changed = False
        iterations += 1

        for rule_id, rule in rules.items():
            if rule_id in used_rules:
                continue

            # Cek apakah semua kondisi IF ada di working_memory
            all_conditions_met = all(condition in working_memory for condition in rule['IF'])

            if all_conditions_met:
                # Hitung CF dari kondisi (rata-rata CF kondisi)
                condition_cfs = [working_memory[condition] for condition in rule['IF']]
                avg_condition_cf = sum(condition_cfs) / len(condition_cfs)

                # CF final = rata-rata CF kondisi * CF rule
                final_cf = avg_condition_cf * rule['CF']

                conclusion = rule['THEN']

                # Update working memory (gunakan CF tertinggi)
                if conclusion in working_memory:
                    working_memory[conclusion] = max(working_memory[conclusion], final_cf)
                else:
                    working_memory[conclusion] = final_cf

                used_rules.append(rule_id)
                changed = True

    return working_memory, used_rules


def diagnose(symptoms_input, rules, conclusions):
    """Membuat diagnosis akhir"""
    if not symptoms_input:
        diagnosis_result = {
            'conclusion': 'Data Tidak Cukup',
            'certainty': 0,
            'score': 0,
            'recommendation': 'Silakan pilih minimal 1 kriteria yang diamati.',
            'timestamp': datetime.now().isoformat()
        }
        return diagnosis_result, []

    # Hitung skor berbobot terlebih dahulu
    weighted_score = calculate_weighted_score(symptoms_input)

    # Gunakan rule-based system untuk kesimpulan yang lebih spesifik
    working_memory, used_rules_ids = forward_chaining(symptoms_input, rules)

    result = None
    highest_cf = 0.0

    # Cari kesimpulan dengan CF tertinggi dari rule-based system
    for c in conclusions:
        if c['id'] in working_memory and working_memory[c['id']] > highest_cf:
            highest_cf = working_memory[c['id']]
            result = c

    reasoning_steps = []
    for rule_id in used_rules_ids:
        rule = rules[rule_id]
        reasoning_steps.append({
            'rule': rule_id,
            'description': rule['description'],
            'conditions': rule['IF'],
            'conclusion': rule['THEN'],
            'cf': rule['CF']
        })

    # **PERBAIKAN KRITIS: Kombinasi yang seimbang dengan validasi konsistensi**
    if result and highest_cf > 0.3:
        # **FIXED: Weighted score lebih dominan (70%) vs rule-based (30%)**
        combined_score = (highest_cf * 30) + (weighted_score * 0.7)
        final_score = min(100, round(combined_score))

        # **VALIDASI KONSISTENSI: Pastikan grade sesuai dengan skor final**
        should_use_rule_based = False

        if final_score >= 85 and ("premium" in result['id'] or "sangat_baik" in result['id']):
            should_use_rule_based = True
            conclusion_label = result['label']
            recommendation = result['recommendation']
            certainty = highest_cf
        elif final_score >= 70 and ("standar" in result['id'] or "baik" in result['id']):
            should_use_rule_based = True
            conclusion_label = result['label']
            recommendation = result['recommendation']
            certainty = highest_cf
        elif final_score >= 50 and ("penggemukan" in result['id'] or "cukup" in result['id']):
            should_use_rule_based = True
            conclusion_label = result['label']
            recommendation = result['recommendation']
            certainty = highest_cf
        elif final_score < 50 and ("tua" in result['id'] or "kurang" in result['id']):
            should_use_rule_based = True
            conclusion_label = result['label']
            recommendation = result['recommendation']
            certainty = highest_cf

        if should_use_rule_based:
            diagnosis_result = {
                'conclusion': conclusion_label,
                'certainty': certainty,
                'score': final_score,
                'recommendation': recommendation,
                'timestamp': datetime.now().isoformat()
            }

            reasoning_steps.append({
                'rule': 'COMBINED_SCORING_VALID',
                'description': f'Kombinasi rule-based (CF: {highest_cf:.2f}) dan weighted scoring ({weighted_score}) - Konsisten',
                'conditions': list(symptoms_input.keys()),
                'conclusion': conclusion_label,
                'cf': highest_cf
            })
        else:
            # **FALLBACK: Gunakan weighted scoring system ketika tidak konsisten**
            diagnosis_result = get_diagnosis_by_weighted_score(weighted_score)
            reasoning_steps.append({
                'rule': 'FALLBACK_WEIGHTED',
                'description': f'Rule-based tidak konsisten dengan skor {final_score}, menggunakan weighted scoring',
                'conditions': list(symptoms_input.keys()),
                'conclusion': diagnosis_result['conclusion'],
                'cf': diagnosis_result['certainty']
            })
    else:
        # Gunakan weighted scoring system saja
        diagnosis_result = get_diagnosis_by_weighted_score(weighted_score)
        reasoning_steps.append({
            'rule': 'WEIGHTED_SCORING',
            'description': 'Analisis berbobot berdasarkan kriteria SNI',
            'conditions': list(symptoms_input.keys()),
            'conclusion': diagnosis_result['conclusion'],
            'cf': diagnosis_result['certainty']
        })

    st.session_state.diagnosis = diagnosis_result
    st.session_state.reasoning = reasoning_steps

    if diagnosis_result['score'] > 0:
        st.session_state.consultation_history.insert(0, diagnosis_result)

    return diagnosis_result, reasoning_steps


def get_diagnosis_by_weighted_score(weighted_score):
    """Helper function untuk menentukan diagnosis berdasarkan weighted score saja."""
    if weighted_score >= 85:
        conclusion_label = 'Layak Dibeli - Grade Premium (A)'
        recommendation = 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.'
    elif weighted_score >= 70:
        conclusion_label = 'Layak Dibeli - Grade Standar (B)'
        recommendation = 'Bibit direkomendasikan. Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.'
    elif weighted_score >= 60:
        conclusion_label = 'Kualitas Baik (B)'
        recommendation = 'Bibit menunjukkan kualitas yang baik.'
    elif weighted_score >= 50:
        conclusion_label = 'Potensial dengan Penggemukan (C)'
        recommendation = 'Bibit memiliki potensi namun perlu program penggemukan dan perawatan intensif selama 2-3 bulan.'
    elif weighted_score >= 40:
        conclusion_label = 'Kualitas Cukup (C)'
        recommendation = 'Bibit menunjukkan kualitas cukup, perlu observasi lebih lanjut.'
    elif weighted_score >= 30:
        conclusion_label = 'Perlu Perhatian Khusus (D)'
        recommendation = 'Bibit memerlukan perhatian dan perawatan khusus.'
    else:
        conclusion_label = 'Tidak Direkomendasikan (E)'
        recommendation = 'Bibit tidak direkomendasikan untuk dibeli.'

    return {
        'conclusion': conclusion_label,
        'certainty': weighted_score / 100,
        'score': weighted_score,
        'recommendation': recommendation,
        'timestamp': datetime.now().isoformat()
    }


# =============================================================================
# TAMPILAN UTAMA (UI)
# =============================================================================
st.title("🐮 Sistem Pakar Penilaian Bibit Sapi Potong")
st.caption("Berbasis Standar Nasional Indonesia (SNI) - Kelompok 6")

tab1, tab2, tab3, tab4 = st.tabs([
    "Konsultasi",
    "Basis Pengetahuan",
    "Riwayat",
    "Tentang"
])

# =============================================================================
# TAB 1: KONSULTASI
# =============================================================================
with tab1:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("Input Pemeriksaan")

        st.info(
            "ℹ️ **Pilih kriteria yang sesuai dengan pengamatan Anda.** Sistem akan menghitung skor berdasarkan bobot SNI.")

        # Inisialisasi temp_symptoms di session state jika belum ada
        if 'temp_symptoms' not in st.session_state:
            st.session_state.temp_symptoms = {}

        # Gunakan variabel lokal untuk tracking pilihan saat ini
        current_symptoms = {}

        with st.form(key="consultation_form"):
            for category, items in SYMPTOM_CATEGORIES.items():
                st.markdown(f"### {category}")

                if category == 'Umur':
                    st.write("Pilih salah satu:")
                    umur_options = {item['label']: item['id'] for item in items}

                    # Tentukan nilai default berdasarkan session state
                    default_index = 0
                    if st.session_state.selected_umur:
                        for i, (label, umur_id) in enumerate(umur_options.items()):
                            if umur_id == st.session_state.selected_umur:
                                default_index = i
                                break

                    selected_umur_label = st.radio(
                        "Umur:",
                        options=list(umur_options.keys()),
                        key="umur_radio",
                        index=default_index
                    )

                    selected_umur_id = umur_options[selected_umur_label]
                    current_symptoms = handle_exclusive_selection('umur', selected_umur_id, current_symptoms)

                elif category == 'Berat':
                    st.write("Pilih salah satu:")
                    berat_options = {item['label']: item['id'] for item in items}

                    # Tentukan nilai default berdasarkan session state
                    default_index = 0
                    if st.session_state.selected_berat:
                        for i, (label, berat_id) in enumerate(berat_options.items()):
                            if berat_id == st.session_state.selected_berat:
                                default_index = i
                                break

                    selected_berat_label = st.radio(
                        "Berat:",
                        options=list(berat_options.keys()),
                        key="berat_radio",
                        index=default_index
                    )

                    selected_berat_id = berat_options[selected_berat_label]
                    current_symptoms = handle_exclusive_selection('berat', selected_berat_id, current_symptoms)

                else:
                    for item in items:
                        # Tentukan status default berdasarkan session state
                        is_checked_default = item['id'] in st.session_state.temp_symptoms
                        is_checked = st.checkbox(
                            item['label'],
                            value=is_checked_default,
                            key=f"checkbox_{item['id']}"
                        )
                        if is_checked:
                            current_symptoms[item['id']] = item['cf']

                st.divider()

            # Update session state dengan pilihan terkini
            st.session_state.temp_symptoms = current_symptoms

            total_selected = len(st.session_state.temp_symptoms)

            if total_selected == 0:
                st.error("❌ **Belum memilih kriteria apapun**")
                st.info("💡 **Tips:** Pilih minimal 1 kriteria untuk mulai analisis")
                allow_submit = False
            elif total_selected == 1:
                st.warning(f"⚠️ **Total kriteria dipilih:** {total_selected}")
                st.info("💡 **Tips:** Tambah lebih banyak kriteria untuk hasil yang lebih akurat")
                allow_submit = True
            elif total_selected < 5:
                st.warning(f"⚠️ **Total kriteria dipilih:** {total_selected}")
                st.info("💡 **Tips:** Pilih minimal 5 kriteria untuk hasil optimal")
                allow_submit = True
            else:
                st.success(f"✅ **Total kriteria dipilih:** {total_selected}")
                allow_submit = True

            submitted = st.form_submit_button(
                "Analisis",
                type="primary" if allow_submit else "secondary",
                use_container_width=True,
                disabled=not allow_submit
            )

        # Tombol analisis di luar form untuk menghindari reset
        if submitted and allow_submit and total_selected > 0:
            st.session_state.symptoms = st.session_state.temp_symptoms.copy()

            # Simpan pilihan umur dan berat
            for umur_id in EXCLUSIVE_OPTIONS['umur']:
                if umur_id in st.session_state.temp_symptoms:
                    st.session_state.selected_umur = umur_id
                    break
            else:
                st.session_state.selected_umur = None

            for berat_id in EXCLUSIVE_OPTIONS['berat']:
                if berat_id in st.session_state.temp_symptoms:
                    st.session_state.selected_berat = berat_id
                    break
            else:
                st.session_state.selected_berat = None

            with st.spinner("Menganalisis kriteria..."):
                diagnose(st.session_state.temp_symptoms, st.session_state.rules, CONCLUSIONS)
            st.rerun()

        if st.button("Reset Konsultasi", use_container_width=True):
            reset_consultation()
            st.rerun()

    with col2:
        st.header("Hasil Penilaian")

        diagnosis = st.session_state.diagnosis

        if not diagnosis:
            st.info("""
            👉 **Petunjuk Penggunaan:**
            1. Pilih **minimal 1 kriteria** dari berbagai kategori
            2. Untuk **Umur** dan **Berat**, pilih **hanya satu opsi** masing-masing (atau tidak memilih)
            3. Klik tombol **Analisis** untuk mendapatkan hasil
            4. Hasil akan muncul di panel ini

            **💡 Sistem Penilaian Berbasis Bobot SNI:**
            - **Umur & Berat Ideal:** Bobot tinggi (20 poin)
            - **Kesehatan & Postur:** Bobot menengah (10-15 poin)
            - **Perilaku:** Bobot sedang (10-12 poin)
            - **Kriteria standar:** Bobot rendah (5-8 poin)

            **📊 Sistem Penalaran:**
            - **Rule-Based:** Menggunakan aturan pakar SNI
            - **Weighted Scoring:** Perhitungan berbobot
            - **Penalty System:** Pengurangan skor untuk data minim

            **Grade System:**
            - **A (85-100):** Premium
            - **B (70-84):** Standar  
            - **C (50-69):** Cukup
            - **D (30-49):** Perlu Perhatian
            - **E (0-29):** Tidak Direkomendasikan
            """)
        else:
            score = diagnosis['score']
            total_criteria_used = len(st.session_state.symptoms)

            # Tampilkan warning berdasarkan jumlah kriteria
            if total_criteria_used == 1:
                st.error(
                    f"⚠️ **PERINGATAN:** Hasil berdasarkan hanya {total_criteria_used} kriteria - Akurasi sangat terbatas")
            elif total_criteria_used < 3:
                st.warning(f"⚠️ **PERINGATAN:** Hasil berdasarkan {total_criteria_used} kriteria - Akurasi rendah")
            elif total_criteria_used < 5:
                st.warning(
                    f"⚠️ **PERINGATAN:** Hasil berdasarkan {total_criteria_used} kriteria - Disarankan tambah lebih banyak kriteria")
            elif total_criteria_used < 8:
                st.info(f"✅ Hasil berdasarkan {total_criteria_used} kriteria - Tingkat akurasi baik")
            else:
                st.success(f"✅ Hasil berdasarkan {total_criteria_used} kriteria - Tingkat akurasi optimal")

            # Tampilkan hasil dengan styling berbeda berdasarkan skor
            if score >= 85:
                st.success(f"**{diagnosis['conclusion']}**", icon="🏆")
            elif score >= 70:
                st.success(f"**{diagnosis['conclusion']}**", icon="👍")
            elif score >= 50:
                st.warning(f"**{diagnosis['conclusion']}**", icon="📋")
            elif score >= 30:
                st.error(f"**{diagnosis['conclusion']}**", icon="⚠️")
            else:
                st.error(f"**{diagnosis['conclusion']}**", icon="❌")

            st.metric(label="Skor Kelayakan", value=f"{score}/100")
            st.progress(score / 100, text=f"Tingkat Kepercayaan: {round(diagnosis['certainty'] * 100)}%")

            # Tampilkan kriteria yang digunakan
            with st.expander(f"Lihat {total_criteria_used} Kriteria yang Digunakan"):
                for symptom_id in st.session_state.symptoms.keys():
                    # Cari label yang sesuai
                    label = next((item['label'] for cat in SYMPTOM_CATEGORIES.values() for item in cat if
                                  item['id'] == symptom_id), symptom_id)
                    st.write(f"• {label}")

            st.info(f"**Rekomendasi:**\n\n{diagnosis['recommendation']}", icon="💡")

            st.download_button(
                label="Unduh Laporan (.txt)",
                data=get_export_string(),
                file_name=f"penilaian_sapi_{datetime.now().strftime('%Y%m%d%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            with st.expander("Tampilkan Proses Penalaran (Penjelasan)"):
                reasoning = st.session_state.reasoning
                if not reasoning:
                    st.write("Tidak ada langkah penalaran yang diambil.")
                else:
                    for i, step in enumerate(reasoning):
                        with st.container():
                            st.markdown(f"**Langkah {i + 1}: {step['rule']}**")
                            st.markdown(f"*{step['description']}*")
                            st.caption(f"**Kondisi:** {', '.join(step['conditions'])}")
                            st.caption(f"**Kesimpulan:** {step['conclusion']}")
                            st.caption(f"**CF:** {step['cf']}")
                            st.divider()

# =============================================================================
# TAB 2: BASIS PENGETAHUAN
# =============================================================================
with tab2:
    st.header("Basis Pengetahuan (Aturan)")
    st.caption(f"Total aturan: {len(st.session_state.rules)}")

    search_query = st.text_input("Cari aturan (berdasarkan ID, THEN, atau deskripsi)")

    for rule_id, rule in st.session_state.rules.items():
        rule_content = f"{rule_id} {rule['description']} {rule['THEN']}".lower()
        if search_query.lower() in rule_content or search_query == "":
            with st.container():
                st.subheader(f"`{rule_id}`: {rule['description']}")
                st.markdown(f"**IF**: `{', '.join(rule['IF'])}`")
                st.markdown(f"**THEN**: `{rule['THEN']}`")
                st.markdown(f"**CF**: `{rule['CF']}`")
                st.divider()

# =============================================================================
# TAB 3: RIWAYAT
# =============================================================================
with tab3:
    st.header("Riwayat Konsultasi")

    history = st.session_state.consultation_history
    if not history:
        st.info("Belum ada riwayat konsultasi.")
    else:
        for i, item in enumerate(history[:10]):
            with st.container():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.subheader(f"{item['conclusion']}")
                    st.text(f"Tanggal: {datetime.fromisoformat(item['timestamp']).strftime('%d %B %Y, %H:%M:%S')}")
                with col_b:
                    st.metric("Skor", f"{item['score']}/100")

                with st.expander("Lihat Detail"):
                    st.write(f"**Rekomendasi:** {item['recommendation']}")
                    st.write(f"**Tingkat Kepercayaan:** {round(item['certainty'] * 100)}%")

                st.divider()

# =============================================================================
# TAB 4: TENTANG
# =============================================================================
with tab4:
    st.header("Tentang Sistem")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Deskripsi Sistem")
        st.write("""
        **Sistem Pakar Penilaian Kualitas Bibit Sapi Potong** adalah aplikasi berbasis web 
        yang membantu peternak dalam menilai kelayakan bibit sapi potong berdasarkan 
        Standar Nasional Indonesia (SNI).
        """)

        st.subheader("Sistem Penilaian yang Ditingkatkan")
        st.write("""
        - **Weighted Scoring:** Setiap kriteria memiliki bobot berbeda
        - **Rule-Based System:** Menggunakan aturan pakar SNI
        - **Penalty System:** Pengurangan skor untuk data yang minim
        - **Combined Approach:** Gabungan rule-based dan weighted scoring
        - **Multi-grade System:** Grade A sampai E dengan threshold yang ketat
        """)

    with col2:
        st.subheader("Tim Pengembang")
        st.markdown("""
        **Kelompok 6 - INF313 Kecerdasan Artifisial**
        - YUYUN NAILUFAR
        - MUHAMMAD RAZI SIREGAR  
        - REYAN ANDREA
        - FIRAH MAULIDA
        - IKRAM AL GHIFFARI
        - DIO FERDI JAYA
        """)

        st.subheader("Peningkatan Akurasi")
        st.markdown("""
        **Fitur Baru:**
        - ✅ **Tidak ada pilihan default** untuk umur/berat
        - ✅ **Penalty system** untuk kriteria minim
        - ✅ **Kombinasi scoring** yang lebih seimbang
        - ✅ **Threshold yang lebih ketat** untuk setiap grade
        - ✅ **Peringatan akurasi** berdasarkan jumlah kriteria
        """)