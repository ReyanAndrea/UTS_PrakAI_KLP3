# # """
# # Sistem Pakar Penilaian Kualitas Bibit Sapi Potong
# # Berbasis Standar Nasional Indonesia (SNI)
# # Web Version with Streamlit
# # Kelompok 6 - INF313 Kecerdasan Artifisial
# # """

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