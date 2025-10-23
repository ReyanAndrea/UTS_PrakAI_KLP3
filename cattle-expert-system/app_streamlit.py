import streamlit as st
import json
from datetime import datetime

# --- Konfigurasi Halaman ---
# Ini harus menjadi perintah Streamlit pertama yang dijalankan
st.set_page_config(
    page_title="Sistem Pakar Bibit Sapi Potong",
    page_icon="🐮",
    layout="wide"
)

# --- Basis Pengetahuan (Knowledge Base) ---
# Diterjemahkan dari 'initialRules' di JavaScript
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

# Diterjemahkan dari 'symptomCategories' di JavaScript
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
    'Umur dan Berat': [
        {'id': 'umur_8_12_bulan', 'label': 'Umur 8-12 bulan', 'cf': 0.9},
        {'id': 'berat_150_200kg', 'label': 'Berat 150-200 kg', 'cf': 0.9},
        {'id': 'umur_kurang', 'label': 'Umur kurang dari 8 bulan', 'cf': 0.6},
        {'id': 'berat_kurang', 'label': 'Berat kurang dari 150 kg', 'cf': 0.6}
    ],
    'Perilaku': [
        {'id': 'nafsu_makan_baik', 'label': 'Nafsu makan baik', 'cf': 0.85},
        {'id': 'aktif_bergerak', 'label': 'Aktif bergerak', 'cf': 0.8},
        {'id': 'tidak_lemas', 'label': 'Tidak tampak lemas', 'cf': 0.85}
    ]
}

# Kesimpulan akhir yang mungkin
CONCLUSIONS = [
    {
        'id': 'layak_dibeli_premium',
        'label': 'Layak Dibeli - Grade Premium',
        'recommendation': 'Bibit sangat direkomendasikan. Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.'
    },
    {
        'id': 'layak_dibeli_standar',
        'label': 'Layak Dibeli - Grade Standar',
        'recommendation': 'Bibit direkomendasikan. Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.'
    },
    {
        'id': 'kualitas_sangat_baik',
        'label': 'Kualitas Sangat Baik (Grade A)',
        'recommendation': 'Bibit memenuhi standar SNI Grade A dengan karakteristik fisik dan kesehatan excellent.'
    },
    {
        'id': 'kualitas_baik',
        'label': 'Kualitas Baik (Grade B)',
        'recommendation': 'Bibit memenuhi standar SNI Grade B dengan karakteristik yang baik.'
    },
    {
        'id': 'perlu_penggemukan',
        'label': 'Potensial dengan Penggemukan',
        'recommendation': 'Bibit memiliki potensi namun memerlukan program penggemukan dan perawatan intensif selama 2-3 bulan.'
    }
]


# --- Inisialisasi Session State ---
# Menggunakan st.session_state untuk menyimpan data antar render (seperti 'useState' di React)
if 'symptoms' not in st.session_state:
    st.session_state.symptoms = {}
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = None
if 'reasoning' not in st.session_state:
    st.session_state.reasoning = []
if 'consultation_history' not in st.session_state:
    st.session_state.consultation_history = []
if 'rules' not in st.session_state:
    st.session_state.rules = INITIAL_RULES # Saat ini, kita hanya pakai aturan awal


# --- Mesin Inferensi (Inference Engine) ---
def calculate_cf(cf1, cf2):
    """Menghitung Certainty Factor gabungan."""
    return cf1 + cf2 * (1 - cf1)

def forward_chaining(symptoms_input, rules):
    """
    Melakukan forward chaining berdasarkan gejala yang dipilih.
    'symptoms_input' adalah dict {id_gejala: cf_gejala}
    """
    st.write("Debug - Forward Chaining mulai dengan gejala:", symptoms_input)
    working_memory = symptoms_input.copy()
    used_rules = []
    changed = True
    iterations = 0
    max_iterations = 20

    while changed and iterations < max_iterations:
        changed = False
        iterations += 1
        
        for rule_id, rule in rules.items():
            if rule_id in used_rules:
                continue

            # Cek apakah semua kondisi (IF) ada di working_memory
            all_conditions_met = all(condition in working_memory for condition in rule['IF'])

            if all_conditions_met:
                # Ambil CF dari setiap kondisi
                condition_cfs = [working_memory[condition] for condition in rule['IF']]
                
                # Hitung CF gabungan dari semua kondisi (ambil minimum)
                # Logika CF bisa bervariasi, di sini kita ambil CF minimal dari premis
                # atau Anda bisa menggabungkannya satu per satu
                # Mari kita ikuti logika JS Anda: gabungkan CF
                combined_cf = 0
                if condition_cfs:
                   combined_cf = condition_cfs[0]
                   for i in range(1, len(condition_cfs)):
                       combined_cf = calculate_cf(combined_cf, condition_cfs[i])
                
                # CF final adalah CF gabungan dikali CF aturan
                final_rule_cf = combined_cf * rule['CF']
                
                conclusion = rule['THEN']

                # Update working memory dengan kesimpulan
                if conclusion in working_memory:
                    # Jika fakta sudah ada, gabungkan CF
                    working_memory[conclusion] = calculate_cf(working_memory[conclusion], final_rule_cf)
                else:
                    working_memory[conclusion] = final_rule_cf
                
                used_rules.append(rule_id)
                changed = True
                
    return working_memory, used_rules

def diagnose(symptoms_input, rules, conclusions):
    """Membuat diagnosis akhir."""
    print("Debug - Fungsi diagnose dipanggil dengan:", symptoms_input)
    
    if not symptoms_input:  # Jika tidak ada gejala yang dipilih
        st.warning("Debug - Tidak ada gejala yang dipilih")
        diagnosis_result = {
            'conclusion': 'Data Tidak Cukup',
            'certainty': 0,
            'score': 0,
            'recommendation': 'Silakan pilih minimal beberapa gejala/kondisi yang diamati.',
            'timestamp': datetime.now().isoformat()
        }
        return diagnosis_result, []

    working_memory, used_rules_ids = forward_chaining(symptoms_input, rules)

    result = None
    highest_cf = 0.3  # Menurunkan ambang batas minimum

    # Cari kesimpulan dengan CF tertinggi
    for c in conclusions:
        if c['id'] in working_memory and working_memory[c['id']] > highest_cf:
            highest_cf = working_memory[c['id']]
            result = c

    if result:
        cf = highest_cf
        score = round(cf * 100)
        
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
        
        diagnosis_result = {
            'conclusion': result['label'],
            'certainty': cf,
            'score': score,
            'recommendation': result['recommendation'],
            'timestamp': datetime.now().isoformat()
        }
    else:
        diagnosis_result = {
            'conclusion': 'Data Tidak Cukup',
            'certainty': 0,
            'score': 0,
            'recommendation': 'Informasi yang diberikan belum cukup untuk memberikan penilaian. Silakan lengkapi data pemeriksaan bibit sapi.',
            'timestamp': datetime.now().isoformat()
        }
        reasoning_steps = []

    # Simpan hasil ke session state
    st.session_state.diagnosis = diagnosis_result
    st.session_state.reasoning = reasoning_steps
    
    # Tambahkan ke riwayat jika ada kesimpulan valid
    if result and diagnosis_result['score'] > 30:  # Hanya simpan jika skor di atas 30
        st.session_state.consultation_history.insert(0, diagnosis_result)

def reset_consultation():
    """Mereset state konsultasi."""
    st.session_state.symptoms = {}
    st.session_state.diagnosis = None
    st.session_state.reasoning = []

def get_export_string():
    """Membuat string teks untuk diunduh."""
    diag = st.session_state.diagnosis
    reas = st.session_state.reasoning
    symp = st.session_state.symptoms

    if not diag:
        return "Belum ada diagnosis."

    symptom_list = "\n".join([f"- {s.replace('_', ' ').capitalize()}" for s in symp.keys()])
    reasoning_list = "\n".join([f"{i+1}. {r['rule']}: {r['description']} (CF: {r['cf']})" for i, r in enumerate(reas)])

    content = f"""
LAPORAN PENILAIAN BIBIT SAPI POTONG
Tanggal: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

HASIL PENILAIAN:
Kesimpulan: {diag['conclusion']}
Skor Kelayakan: {diag['score']}/100
Tingkat Kepercayaan: {round(diag['certainty'] * 100)}%

REKOMENDASI:
{diag['recommendation']}

GEJALA YANG DIAMATI:
{symptom_list}

PROSES PENALARAN:
{reasoning_list}
    """.strip()
    return content

# --- Tampilan Utama (UI) ---
st.title("🐮 Sistem Pakar Penilaian Bibit Sapi Potong")
st.caption("Berbasis Standar Nasional Indonesia (SNI) - Kelompok 6")

# Menggunakan Tabs untuk navigasi halaman
tab1, tab2, tab3, tab4 = st.tabs([
    "Konsultasi", 
    "Basis Pengetahuan (Aturan)", 
    "Riwayat", 
    "Tentang"
])

# --- Tab 1: Konsultasi ---
with tab1:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("Input Pemeriksaan")
        
        # Gunakan form agar input dikumpulkan sebelum diproses
        with st.form(key="consultation_form"):
            selected_symptoms = {}
            
            # Tambahkan panduan penggunaan
            st.info("ℹ️ Pilih kondisi-kondisi yang sesuai dengan pengamatan Anda pada bibit sapi yang dinilai.")
            
            for category, items in SYMPTOM_CATEGORIES.items():
                st.markdown(f"### {category}")
                st.divider()
                for item in items:
                    if st.checkbox(item['label'], key=item['id']):
                        selected_symptoms[item['id']] = item['cf']
                st.divider()
            
            # Tombol Analisis
            submitted = st.form_submit_button("Analisis", type="primary", use_container_width=True)
            
            if submitted:
                st.session_state.symptoms = selected_symptoms
                st.write("Debug - Gejala yang dipilih:", selected_symptoms)
                if len(selected_symptoms) > 0:
                    st.write("Debug - Jumlah gejala dipilih:", len(selected_symptoms))
                    diagnose(selected_symptoms, st.session_state.rules, CONCLUSIONS)
                else:
                    st.warning("⚠️ Anda belum memilih gejala apapun")
        
        # Tombol Reset di luar form
        if st.button("Reset Konsultasi", use_container_width=True):
            reset_consultation()
            st.rerun()

    with col2:
        st.header("Hasil Penilaian")
        
        diagnosis = st.session_state.diagnosis
        
        if not diagnosis:
            st.info("👉 Silakan pilih minimal beberapa gejala/kondisi yang diamati di panel sebelah kiri, lalu klik tombol Analisis untuk mendapatkan hasil penilaian.")
        else:
            score = diagnosis['score']
            
            # Tampilkan hasil dengan warna berbeda
            if score >= 80:
                st.success(f"**{diagnosis['conclusion']}**", icon="🏆")
            elif score >= 60:
                st.warning(f"**{diagnosis['conclusion']}**", icon="👍")
            else:
                st.error(f"**{diagnosis['conclusion']}**", icon="📋")

            # Tampilkan Skor dan Kepercayaan
            st.metric(label="Skor Kelayakan", value=f"{score}/100")
            st.progress(score, text=f"Tingkat Kepercayaan: {round(diagnosis['certainty'] * 100)}%")
            
            # Tampilkan Rekomendasi
            st.info(f"**Rekomendasi:**\n\n{diagnosis['recommendation']}", icon="💡")

            # Tombol Unduh Laporan
            st.download_button(
                label="Unduh Laporan (.txt)",
                data=get_export_string(),
                file_name=f"penilaian_sapi_{datetime.now().strftime('%Y%m%d%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            # Penjelasan (Explanation Facility)
            with st.expander("Tampilkan Proses Penalaran (Penjelasan)"):
                reasoning = st.session_state.reasoning
                if not reasoning:
                    st.write("Tidak ada langkah penalaran yang diambil.")
                else:
                    for step in reasoning:
                        with st.container():
                            st.markdown(f"**{step['rule']}**: {step['description']}")
                            st.caption(f"IF: {', '.join(step['conditions'])} → THEN: {step['conclusion']} (CF: {step['cf']})")

# --- Tab 2: Basis Pengetahuan (Aturan) ---
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

# --- Tab 3: Riwayat ---
with tab3:
    st.header("Riwayat Konsultasi")
    
    history = st.session_state.consultation_history
    if not history:
        st.info("Belum ada riwayat konsultasi.")
    else:
        for i, item in enumerate(history):
            with st.container():
                st.subheader(f"Hasil: {item['conclusion']}")
                st.text(f"Tanggal: {datetime.fromisoformat(item['timestamp']).strftime('%d %B %Y, %H:%M:%S')}")
                st.text(f"Skor: {item['score']}/100 (Kepercayaan: {round(item['certainty'] * 100)}%)")
                with st.expander("Lihat Rekomendasi"):
                    st.write(item['recommendation'])

# --- Tab 4: Tentang ---
with tab4:
    st.header("Tentang Sistem")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Deskripsi")
        st.write("""
        Sistem Pakar untuk Penilaian Kualitas Bibit Sapi Potong berbasis *Rule-Based System* dengan
        metode *Forward Chaining* dan *Certainty Factor*. Sistem ini membantu peternak dalam menilai
        kelayakan bibit sapi potong berdasarkan Standar Nasional Indonesia (SNI).
        """)
        
        st.subheader("Standar Penilaian")
        st.write("""
        Sistem mengacu pada SNI 7651.6:2015 tentang Bibit Sapi Potong dan pedoman teknis penilaian
        kualitas ternak dari Kementerian Pertanian RI.
        """)

    with col2:
        st.subheader("Kelompok 6")
        st.markdown("""
        - YUYUN NAILUFAR
        - MUHAMMAD RAZI SIREGAR
        - REYAN ANDREA
        - FIRAH MAULIDA
        - IKRAM AL GHIFFARI
        - DIO FERDI JAYA
        """)
        
        st.subheader("Fitur")
        st.markdown("""
        - *Forward Chaining* inference engine
        - *Certainty Factor* untuk ketidakpastian
        - *Explanation facility* (Penjelasan penalaran)
        - Basis pengetahuan yang dapat dilihat
        - Ekspor laporan hasil
        - Riwayat konsultasi
        """)