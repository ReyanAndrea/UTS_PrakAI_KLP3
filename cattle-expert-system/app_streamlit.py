"""
Sistem Pakar Penilaian Kualitas Bibit Sapi Potong
Berbasis Standar Nasional Indonesia (SNI)
Web Version with Streamlit
Kelompok 6 - INF313 Kecerdasan Artifisial
"""

import streamlit as st
import json
import csv
import io
from datetime import datetime
from typing import Dict, List, Tuple

# Set page config
st.set_page_config(
    page_title="Sistem Pakar Bibit Sapi Potong",
    page_icon="🐄",
    layout="wide"
)

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
            },
            'R13': {
                'IF': ['tanduk_simetris', 'kepala_proporsional'],
                'THEN': 'karakteristik_kepala_baik',
                'CF': 0.75,
                'description': 'Karakteristik kepala sesuai standar'
            },
            'R14': {
                'IF': ['karakteristik_kepala_baik', 'struktur_tubuh_ideal'],
                'THEN': 'konformasi_sempurna',
                'CF': 0.88,
                'description': 'Konformasi tubuh sempurna untuk breeding'
            },
            'R15': {
                'IF': ['konformasi_sempurna', 'kualitas_sangat_baik'],
                'THEN': 'bibit_unggul',
                'CF': 0.92,
                'description': 'Bibit unggul kelas premium'
            }
        }
        
        self.symptom_database = {
            'Postur Fisik': [
                {'id': 'postur_tegak', 'label': 'Postur tubuh tegak dan proporsional', 'cf': 0.9},
                {'id': 'dada_lebar', 'label': 'Dada lebar dan dalam', 'cf': 0.85},
                {'id': 'kaki_kuat', 'label': 'Kaki kuat dan lurus', 'cf': 0.9},
                {'id': 'punggung_rata', 'label': 'Punggung rata dan kuat', 'cf': 0.8},
                {'id': 'perut_tidak_buncit', 'label': 'Perut tidak buncit', 'cf': 0.75},
                {'id': 'ekor_panjang', 'label': 'Ekor panjang hingga tumit', 'cf': 0.7},
                {'id': 'tanduk_simetris', 'label': 'Tanduk simetris', 'cf': 0.75},
                {'id': 'kepala_proporsional', 'label': 'Kepala proporsional dengan tubuh', 'cf': 0.75}
            ],
            'Kondisi Kesehatan': [
                {'id': 'mata_cerah', 'label': 'Mata cerah dan bersih', 'cf': 0.85},
                {'id': 'hidung_basah', 'label': 'Hidung basah dan bersih', 'cf': 0.8},
                {'id': 'bulu_mengkilap', 'label': 'Bulu mengkilap dan rapi', 'cf': 0.75},
                {'id': 'tidak_ada_penyakit', 'label': 'Tidak ada riwayat penyakit', 'cf': 0.95},
                {'id': 'riwayat_vaksin_lengkap', 'label': 'Vaksinasi lengkap', 'cf': 0.9},
                {'id': 'kulit_elastis', 'label': 'Kulit elastis dan tidak kering', 'cf': 0.75}
            ],
            'Umur dan Berat': [
                {'id': 'umur_8_12_bulan', 'label': 'Umur 8-12 bulan', 'cf': 0.9},
                {'id': 'umur_kurang', 'label': 'Umur kurang dari 8 bulan', 'cf': 0.6},
                {'id': 'berat_150_200kg', 'label': 'Berat 150-200 kg', 'cf': 0.9},
                {'id': 'berat_kurang', 'label': 'Berat kurang dari 150 kg', 'cf': 0.6}
            ],
            'Perilaku': [
                {'id': 'nafsu_makan_baik', 'label': 'Nafsu makan baik', 'cf': 0.85},
                {'id': 'aktif_bergerak', 'label': 'Aktif bergerak', 'cf': 0.8},
                {'id': 'tidak_lemas', 'label': 'Tidak tampak lemas', 'cf': 0.85},
                {'id': 'responsif', 'label': 'Responsif terhadap rangsangan', 'cf': 0.8}
            ]
        }

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
            self.derived_facts[fact] = self.combine_cf(self.derived_facts[fact], cf)
        else:
            self.derived_facts[fact] = cf
        
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
        """Forward Chaining (Data-Driven Reasoning)"""
        self.reasoning_trace = []
        used_rules = []
        changed = True
        iteration = 0
        max_iterations = 20
        
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            
            for rule_id, rule in self.kb.rules.items():
                if rule_id in used_rules:
                    continue
                
                all_conditions_met = all(
                    working_memory.has_fact(condition) 
                    for condition in rule['IF']
                )
                
                if all_conditions_met:
                    combined_cf = rule['CF']
                    for condition in rule['IF']:
                        fact_cf = working_memory.get_fact(condition)
                        combined_cf = working_memory.combine_cf(combined_cf, fact_cf)
                    
                    working_memory.add_derived_fact(rule['THEN'], combined_cf)
                    
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

def export_to_txt(result: Dict, kb: KnowledgeBase) -> str:
    """Export hasil ke format TXT"""
    output = []
    output.append("=" * 60)
    output.append("LAPORAN PENILAIAN BIBIT SAPI POTONG")
    output.append("Sistem Pakar Berbasis Rule-Based")
    output.append("=" * 60)
    output.append("")
    output.append(f"Tanggal: {result['timestamp']}")
    output.append("")
    output.append("HASIL PENILAIAN:")
    output.append("-" * 60)
    output.append(f"Kesimpulan: {result['conclusion']['label']}")
    output.append(f"Grade: {result['conclusion']['grade']}")
    output.append(f"Skor Kelayakan: {result['conclusion']['score']}/100")
    output.append(f"Tingkat Kepercayaan: {int(result['conclusion']['cf'] * 100)}%")
    output.append("")
    output.append("REKOMENDASI:")
    output.append("-" * 60)
    output.append(result['conclusion']['recommendation'])
    output.append("")
    output.append("KONDISI YANG DIAMATI:")
    output.append("-" * 60)
    
    for fact_id, cf in result['selected_facts'].items():
        for category, symptoms in kb.symptom_database.items():
            for symptom in symptoms:
                if symptom['id'] == fact_id:
                    output.append(f"- {symptom['label']} (CF: {cf:.2f})")
                    break
    
    if result['trace']:
        output.append("")
        output.append("=" * 60)
        output.append("PROSES PENALARAN:")
        output.append("=" * 60)
        output.append("")
        
        for i, step in enumerate(result['trace'], 1):
            output.append(f"Langkah {i}:")
            output.append(f"  Rule: {step['rule_id']} - {step['description']}")
            output.append(f"  IF: {', '.join(step['conditions'])}")
            output.append(f"  THEN: {step['conclusion']}")
            output.append(f"  CF: {step['cf']:.2f}")
            output.append("")
    
    return "\n".join(output)

def export_to_json(result: Dict) -> str:
    """Export hasil ke format JSON"""
    export_data = {
        'timestamp': result['timestamp'],
        'conclusion': {
            'label': result['conclusion']['label'],
            'grade': result['conclusion']['grade'],
            'score': result['conclusion']['score'],
            'cf': result['conclusion']['cf'],
            'recommendation': result['conclusion']['recommendation']
        },
        'selected_conditions': [
            {'id': fact_id, 'cf': cf}
            for fact_id, cf in result['selected_facts'].items()
        ],
        'reasoning_trace': result['trace']
    }
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def export_to_csv(result: Dict, kb: KnowledgeBase) -> str:
    """Export hasil ke format CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['LAPORAN PENILAIAN BIBIT SAPI POTONG'])
    writer.writerow(['Tanggal', result['timestamp']])
    writer.writerow([])
    
    # Hasil Penilaian
    writer.writerow(['HASIL PENILAIAN'])
    writer.writerow(['Kesimpulan', result['conclusion']['label']])
    writer.writerow(['Grade', result['conclusion']['grade']])
    writer.writerow(['Skor', result['conclusion']['score']])
    writer.writerow(['Tingkat Kepercayaan (%)', int(result['conclusion']['cf'] * 100)])
    writer.writerow(['Rekomendasi', result['conclusion']['recommendation']])
    writer.writerow([])
    
    # Kondisi yang diamati
    writer.writerow(['KONDISI YANG DIAMATI'])
    writer.writerow(['Kondisi', 'Certainty Factor'])
    
    for fact_id, cf in result['selected_facts'].items():
        for category, symptoms in kb.symptom_database.items():
            for symptom in symptoms:
                if symptom['id'] == fact_id:
                    writer.writerow([symptom['label'], f"{cf:.2f}"])
                    break
    
    writer.writerow([])
    
    # Proses Penalaran
    if result['trace']:
        writer.writerow(['PROSES PENALARAN'])
        writer.writerow(['Step', 'Rule ID', 'Description', 'Conclusion', 'CF'])
        
        for i, step in enumerate(result['trace'], 1):
            writer.writerow([
                i,
                step['rule_id'],
                step['description'],
                step['conclusion'],
                f"{step['cf']:.2f}"
            ])
    
    return output.getvalue()

def determine_conclusion(facts: Dict, trace: List, selected_count: int) -> Dict:
    """Menentukan kesimpulan dengan logic yang lebih baik"""
    
    conclusions = {
        'bibit_unggul': {
            'label': 'Bibit Unggul Kelas Premium',
            'grade': 'A+',
            'recommendation': 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas premium. Sangat cocok untuk breeding atau penggemukan intensif dengan potensi keuntungan tinggi.'
        },
        'layak_dibeli_premium': {
            'label': 'Layak Dibeli - Grade Premium',
            'grade': 'A',
            'recommendation': 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.'
        },
        'kualitas_sangat_baik': {
            'label': 'Kualitas Sangat Baik',
            'grade': 'A',
            'recommendation': 'Bibit memenuhi standar SNI Grade A dengan karakteristik fisik dan kesehatan excellent.'
        },
        'layak_dibeli_standar': {
            'label': 'Layak Dibeli - Grade Standar',
            'grade': 'B',
            'recommendation': 'Bibit direkomendasikan. Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.'
        },
        'kualitas_baik': {
            'label': 'Kualitas Baik',
            'grade': 'B',
            'recommendation': 'Bibit memenuhi standar SNI Grade B dengan karakteristik yang baik.'
        },
        'perlu_penggemukan': {
            'label': 'Potensial dengan Penggemukan',
            'grade': 'C',
            'recommendation': 'Bibit memiliki potensi namun memerlukan program penggemukan dan perawatan intensif selama 2-3 bulan.'
        }
    }
    
    # Cari kesimpulan dengan CF tertinggi
    best_conclusion = None
    best_cf = 0.0
    
    for conclusion_id, conclusion_data in conclusions.items():
        if conclusion_id in facts and facts[conclusion_id] > best_cf:
            best_cf = facts[conclusion_id]
            best_conclusion = {
                'id': conclusion_id,
                'label': conclusion_data['label'],
                'grade': conclusion_data['grade'],
                'cf': best_cf,
                'score': int(best_cf * 100),
                'recommendation': conclusion_data['recommendation']
            }
    
    # LOGIC BARU: Hitung berdasarkan fakta yang dipilih jika tidak ada kesimpulan
    if best_conclusion is None or best_cf < 0.3:
        if selected_count == 0:
            return {
                'id': 'no_data',
                'label': 'Belum Ada Data',
                'grade': 'N/A',
                'cf': 0.0,
                'score': 0,
                'recommendation': 'Silakan pilih minimal satu kondisi untuk memulai penilaian.'
            }
        
        # Hitung rata-rata CF dari fakta yang dipilih user
        selected_facts = {k: v for k, v in facts.items() if k in st.session_state.get('selected_facts', {})}
        if selected_facts:
            avg_cf = sum(selected_facts.values()) / len(selected_facts)
        else:
            avg_cf = 0.5
        
        # Tentukan grade berdasarkan CF
        if avg_cf >= 0.8:
            grade = 'B+'
            label = 'Kualitas Cukup Baik'
            recommendation = 'Bibit menunjukkan beberapa karakteristik baik. Perlu evaluasi lebih lengkap untuk penilaian optimal.'
        elif avg_cf >= 0.7:
            grade = 'B'
            label = 'Kualitas Sedang'
            recommendation = 'Bibit menunjukkan karakteristik standar. Disarankan melengkapi pemeriksaan untuk hasil lebih akurat.'
        elif avg_cf >= 0.6:
            grade = 'C+'
            label = 'Kualitas Cukup'
            recommendation = 'Bibit memiliki potensi namun perlu pemeriksaan lebih menyeluruh dan mungkin memerlukan perawatan tambahan.'
        else:
            grade = 'C'
            label = 'Perlu Evaluasi Lebih Lanjut'
            recommendation = 'Bibit perlu pemeriksaan lebih lengkap. Beberapa karakteristik perlu ditingkatkan.'
        
        best_conclusion = {
            'id': 'partial_evaluation',
            'label': label,
            'grade': grade,
            'cf': avg_cf,
            'score': int(avg_cf * 100),
            'recommendation': f"{recommendation} (Berdasarkan {selected_count} kriteria yang dipilih)"
        }
    
    return best_conclusion

def main():
    # Initialize session state
    if 'kb' not in st.session_state:
        st.session_state.kb = KnowledgeBase()
        st.session_state.wm = WorkingMemory()
        st.session_state.ie = InferenceEngine(st.session_state.kb)
        st.session_state.selected_facts = {}
        st.session_state.result = None
        st.session_state.history = []
    
    # Header
    st.title("🐄 Sistem Pakar Penilaian Bibit Sapi Potong")
    st.markdown("**Berbasis Standar Nasional Indonesia (SNI) - Kelompok 6**")
    st.divider()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Konsultasi", "📜 Riwayat", "ℹ️ Tentang"])
    
    with tab1:
        st.header("Pemeriksaan Bibit Sapi Potong")
        st.info("Pilih semua kondisi yang sesuai dengan bibit sapi yang diamati")
        
        # Display symptoms by category
        for category, symptoms in st.session_state.kb.symptom_database.items():
            st.subheader(f"🔹 {category}")
            
            # LOGIC BARU: Filter symptoms untuk Umur dan Berat
            filtered_symptoms = symptoms.copy()
            if category == 'Umur dan Berat':
                # Jika sudah pilih umur 8-12 bulan, hide umur kurang
                if 'umur_8_12_bulan' in st.session_state.selected_facts:
                    filtered_symptoms = [s for s in filtered_symptoms if s['id'] != 'umur_kurang']
                # Jika sudah pilih umur kurang, hide umur 8-12
                if 'umur_kurang' in st.session_state.selected_facts:
                    filtered_symptoms = [s for s in filtered_symptoms if s['id'] != 'umur_8_12_bulan']
                
                # Jika sudah pilih berat 150-200, hide berat kurang
                if 'berat_150_200kg' in st.session_state.selected_facts:
                    filtered_symptoms = [s for s in filtered_symptoms if s['id'] != 'berat_kurang']
                # Jika sudah pilih berat kurang, hide berat 150-200
                if 'berat_kurang' in st.session_state.selected_facts:
                    filtered_symptoms = [s for s in filtered_symptoms if s['id'] != 'berat_150_200kg']
            
            cols = st.columns(2)
            for idx, symptom in enumerate(filtered_symptoms):
                with cols[idx % 2]:
                    is_checked = symptom['id'] in st.session_state.selected_facts
                    if st.checkbox(
                        symptom['label'],  # Removed CF display
                        value=is_checked,
                        key=symptom['id']
                    ):
                        st.session_state.selected_facts[symptom['id']] = symptom['cf']
                    else:
                        if symptom['id'] in st.session_state.selected_facts:
                            del st.session_state.selected_facts[symptom['id']]
        
        st.divider()
        
        # Buttons
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔍 Diagnosa Sekarang", type="primary", use_container_width=True):
                # Clear working memory
                st.session_state.wm.clear()
                
                # Add selected facts to working memory
                for fact_id, cf in st.session_state.selected_facts.items():
                    st.session_state.wm.add_fact(fact_id, cf)
                
                # Run forward chaining
                facts, trace = st.session_state.ie.forward_chaining(st.session_state.wm)
                
                # Determine conclusion
                selected_count = len(st.session_state.selected_facts)
                conclusion = determine_conclusion(facts, trace, selected_count)
                
                # Save result
                result = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'conclusion': conclusion,
                    'facts': facts,
                    'trace': trace,
                    'selected_facts': st.session_state.selected_facts.copy()
                }
                
                st.session_state.result = result
                st.session_state.history.insert(0, result)
                
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.selected_facts = {}
                st.session_state.result = None
                st.rerun()
        
        # Display Result
        if st.session_state.result:
            st.divider()
            st.header("📊 Hasil Penilaian")
            
            result = st.session_state.result
            conclusion = result['conclusion']
            
            # Grade badge
            col1, col2 = st.columns([1, 3])
            with col1:
                grade_color = {
                    'A+': '🟢', 'A': '🟢',
                    'B+': '🔵', 'B': '🔵',
                    'C+': '🟡', 'C': '🟡',
                    'N/A': '⚪'
                }
                grade_emoji = grade_color.get(conclusion['grade'], '⚪')
                st.markdown(f"### {grade_emoji} Grade **{conclusion['grade']}**")
            
            with col2:
                st.markdown(f"### {conclusion['label']}")
                st.markdown(f"**Skor Kelayakan:** {conclusion['score']}/100")
            
            # Progress bar
            st.progress(conclusion['cf'], text=f"Tingkat Kepercayaan: {int(conclusion['cf'] * 100)}%")
            
            # Recommendation
            st.success(f"**Rekomendasi:** {conclusion['recommendation']}")
            
            # Download buttons
            st.divider()
            st.subheader("💾 Download Hasil")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                txt_data = export_to_txt(result, st.session_state.kb)
                st.download_button(
                    label="📄 Download TXT",
                    data=txt_data,
                    file_name=f"laporan_sapi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                json_data = export_to_json(result)
                st.download_button(
                    label="📋 Download JSON",
                    data=json_data,
                    file_name=f"laporan_sapi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col3:
                csv_data = export_to_csv(result, st.session_state.kb)
                st.download_button(
                    label="📊 Download CSV",
                    data=csv_data,
                    file_name=f"laporan_sapi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Explanation
            with st.expander("📄 Lihat Penjelasan Detail"):
                st.subheader("Kondisi yang Dipilih:")
                for fact_id, cf in result['selected_facts'].items():
                    # Find symptom label
                    for category, symptoms in st.session_state.kb.symptom_database.items():
                        for symptom in symptoms:
                            if symptom['id'] == fact_id:
                                st.write(f"✓ {symptom['label']} (CF: {cf:.2f})")
                                break
                
                if result['trace']:
                    st.divider()
                    st.subheader("Proses Penalaran:")
                    for i, step in enumerate(result['trace'], 1):
                        st.write(f"**{i}. {step['rule_id']}:** {step['description']}")
                        st.write(f"   → Kesimpulan: {step['conclusion'].replace('_', ' ').title()} (CF: {step['cf']:.2f})")
    
    with tab2:
        st.header("📜 Riwayat Konsultasi")
        
        if not st.session_state.history:
            st.info("Belum ada riwayat konsultasi")
        else:
            for i, record in enumerate(st.session_state.history):
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{record['timestamp']}**")
                        st.write(record['conclusion']['label'])
                    with col2:
                        st.metric("Grade", record['conclusion']['grade'])
                    with col3:
                        st.metric("Skor", f"{record['conclusion']['score']}/100")
                    st.divider()
    
    with tab3:
        st.header("ℹ️ Tentang Sistem")
        
        st.markdown("""
        ### Sistem Pakar Penilaian Kualitas Bibit Sapi Potong
        Berbasis Rule-Based System dengan Forward Chaining
        
        #### 👥 Kelompok 6:
        1. YUYUN NAILUFAR
        2. MUHAMMAD RAZI SIREGAR
        3. REYAN ANDREA
        4. FIRAH MAULIDA
        5. IKRAM AL GHIFFARI
        6. DIO FERDI JAYA
        
        #### 📚 Mata Kuliah
        **INF313 - Kecerdasan Artifisial**
        
        #### ✨ Fitur Sistem:
        - Forward Chaining Inference Engine
        - Certainty Factor untuk ketidakpastian
        - Explanation Facility (WHY & HOW)
        - Riwayat konsultasi
        - Interface web yang user-friendly
        
        #### 📋 Standar Acuan:
        SNI 7651.6:2015 - Bibit Sapi Potong
        
        #### 🔧 Technology Stack:
        - Python 3.x
        - Streamlit
        - Rule-Based Expert System
        """)

if __name__ == "__main__":
    main()