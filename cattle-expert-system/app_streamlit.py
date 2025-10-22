import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, FileText, Search, Plus, Edit, Trash2, Download, History, Info } from 'lucide-react';

const CattleExpertSystem = () => {
const [currentPage, setCurrentPage] = useState('home');
const [symptoms, setSymptoms] = useState({});
const [diagnosis, setDiagnosis] = useState(null);
const [reasoning, setReasoning] = useState([]);
const [consultationHistory, setConsultationHistory] = useState([]);
const [rules, setRules] = useState({});
const [showExplanation, setShowExplanation] = useState(false);
const [editingRule, setEditingRule] = useState(null);
const [searchQuery, setSearchQuery] = useState('');

// Initialize rules and load from storage
useEffect(() => {
const initializeRules = async () => {
try {
const storedRules = await window.storage.get('cattle_rules');
if (storedRules) {
setRules(JSON.parse(storedRules.value));
} else {
setRules(initialRules);
await window.storage.set('cattle_rules', JSON.stringify(initialRules));
}
} catch (error) {
setRules(initialRules);
}
};

const loadHistory = async () => {
try {
const stored = await window.storage.get('consultation_history');
if (stored) {
setConsultationHistory(JSON.parse(stored.value));
}
} catch (error) {
console.log('No history found');
}
};

initializeRules();
loadHistory();
}, []);

const initialRules = {
R1: {
IF: ['postur_tegak', 'dada_lebar', 'kaki_kuat'],
THEN: 'indikator_fisik_baik',
CF: 0.85,
description: 'Postur tubuh ideal untuk sapi potong'
},
R2: {
IF: ['mata_cerah', 'hidung_basah', 'bulu_mengkilap'],
THEN: 'indikator_kesehatan_baik',
CF: 0.8,
description: 'Tanda-tanda kesehatan yang baik'
},
R3: {
IF: ['umur_8_12_bulan', 'berat_150_200kg'],
THEN: 'umur_berat_ideal',
CF: 0.9,
description: 'Umur dan berat sesuai standar bibit'
},
R4: {
IF: ['riwayat_vaksin_lengkap', 'tidak_ada_penyakit'],
THEN: 'riwayat_kesehatan_baik',
CF: 0.95,
description: 'Riwayat kesehatan terdokumentasi baik'
},
R5: {
IF: ['indikator_fisik_baik', 'indikator_kesehatan_baik', 'umur_berat_ideal'],
THEN: 'kualitas_sangat_baik',
CF: 0.9,
description: 'Bibit memenuhi kriteria SNI kualitas A'
},
R6: {
IF: ['indikator_fisik_baik', 'indikator_kesehatan_baik'],
THEN: 'kualitas_baik',
CF: 0.75,
description: 'Bibit memenuhi kriteria SNI kualitas B'
},
R7: {
IF: ['punggung_rata', 'perut_tidak_buncit', 'ekor_panjang'],
THEN: 'konformasi_baik',
CF: 0.8,
description: 'Konformasi tubuh sesuai standar'
},
R8: {
IF: ['konformasi_baik', 'indikator_fisik_baik'],
THEN: 'struktur_tubuh_ideal',
CF: 0.85,
description: 'Struktur tubuh memenuhi standar breeding'
},
R9: {
IF: ['nafsu_makan_baik', 'aktif_bergerak', 'tidak_lemas'],
THEN: 'perilaku_normal',
CF: 0.8,
description: 'Perilaku menunjukkan kondisi sehat'
},
R10: {
IF: ['struktur_tubuh_ideal', 'riwayat_kesehatan_baik', 'perilaku_normal'],
THEN: 'layak_dibeli_premium',
CF: 0.95,
description: 'Sangat direkomendasikan untuk pembelian'
},
R11: {
IF: ['kualitas_baik', 'riwayat_kesehatan_baik'],
THEN: 'layak_dibeli_standar',
CF: 0.8,
description: 'Direkomendasikan untuk pembelian'
},
R12: {
IF: ['postur_tegak', 'berat_kurang', 'umur_kurang'],
THEN: 'perlu_penggemukan',
CF: 0.7,
description: 'Bibit potensial namun perlu perawatan intensif'
}
};

const symptomCategories = {
'Postur Fisik': [
{ id: 'postur_tegak', label: 'Postur tubuh tegak dan proporsional', cf: 0.9 },
{ id: 'dada_lebar', label: 'Dada lebar dan dalam', cf: 0.85 },
{ id: 'kaki_kuat', label: 'Kaki kuat dan lurus', cf: 0.9 },
{ id: 'punggung_rata', label: 'Punggung rata dan kuat', cf: 0.8 },
{ id: 'perut_tidak_buncit', label: 'Perut tidak buncit', cf: 0.75 },
{ id: 'ekor_panjang', label: 'Ekor panjang hingga tumit', cf: 0.7 }
],
'Kondisi Kesehatan': [
{ id: 'mata_cerah', label: 'Mata cerah dan bersih', cf: 0.85 },
{ id: 'hidung_basah', label: 'Hidung basah dan bersih', cf: 0.8 },
{ id: 'bulu_mengkilap', label: 'Bulu mengkilap dan rapi', cf: 0.75 },
{ id: 'tidak_ada_penyakit', label: 'Tidak ada riwayat penyakit', cf: 0.95 },
{ id: 'riwayat_vaksin_lengkap', label: 'Vaksinasi lengkap', cf: 0.9 }
],
'Umur dan Berat': [
{ id: 'umur_8_12_bulan', label: 'Umur 8-12 bulan', cf: 0.9 },
{ id: 'berat_150_200kg', label: 'Berat 150-200 kg', cf: 0.9 },
{ id: 'umur_kurang', label: 'Umur kurang dari 8 bulan', cf: 0.6 },
{ id: 'berat_kurang', label: 'Berat kurang dari 150 kg', cf: 0.6 }
],
'Perilaku': [
{ id: 'nafsu_makan_baik', label: 'Nafsu makan baik', cf: 0.85 },
{ id: 'aktif_bergerak', label: 'Aktif bergerak', cf: 0.8 },
{ id: 'tidak_lemas', label: 'Tidak tampak lemas', cf: 0.85 }
]
};

const calculateCF = (cf1, cf2) => {
return cf1 + cf2 * (1 - cf1);
};

const forwardChaining = () => {
const workingMemory = { ...symptoms };
const usedRules = [];
let changed = true;
let iterations = 0;
const maxIterations = 20;

while (changed && iterations < maxIterations) { changed=false; iterations++; for (const [ruleId, rule] of
    Object.entries(rules)) { if (usedRules.includes(ruleId)) continue; const allConditionsMet=rule.IF.every(condition=>
    workingMemory[condition]);

    if (allConditionsMet) {
    let combinedCF = rule.CF;
    rule.IF.forEach(condition => {
    if (workingMemory[condition] && typeof workingMemory[condition] === 'number') {
    combinedCF = calculateCF(combinedCF, workingMemory[condition]);
    }
    });

    if (workingMemory[rule.THEN]) {
    workingMemory[rule.THEN] = calculateCF(workingMemory[rule.THEN], combinedCF);
    } else {
    workingMemory[rule.THEN] = combinedCF;
    }

    usedRules.push(ruleId);
    changed = true;
    }
    }
    }

    return { workingMemory, usedRules };
    };

    const diagnose = () => {
    const { workingMemory, usedRules } = forwardChaining();

    const conclusions = [
    { id: 'layak_dibeli_premium', label: 'Layak Dibeli - Grade Premium', recommendation: 'Bibit sangat direkomendasikan.
    Memenuhi seluruh kriteria SNI untuk sapi potong berkualitas tinggi. Cocok untuk breeding atau penggemukan intensif.'
    },
    { id: 'layak_dibeli_standar', label: 'Layak Dibeli - Grade Standar', recommendation: 'Bibit direkomendasikan.
    Memenuhi kriteria SNI standar. Cocok untuk penggemukan dengan manajemen yang baik.' },
    { id: 'kualitas_sangat_baik', label: 'Kualitas Sangat Baik (Grade A)', recommendation: 'Bibit memenuhi standar SNI
    Grade A dengan karakteristik fisik dan kesehatan excellent.' },
    { id: 'kualitas_baik', label: 'Kualitas Baik (Grade B)', recommendation: 'Bibit memenuhi standar SNI Grade B dengan
    karakteristik yang baik.' },
    { id: 'perlu_penggemukan', label: 'Potensial dengan Penggemukan', recommendation: 'Bibit memiliki potensi namun
    memerlukan program penggemukan dan perawatan intensif selama 2-3 bulan.' }
    ];

    const result = conclusions.find(c => workingMemory[c.id] && workingMemory[c.id] > 0.6);

    if (result) {
    const cf = workingMemory[result.id];
    const score = Math.round(cf * 100);

    const reasoningSteps = usedRules.map(ruleId => ({
    rule: ruleId,
    description: rules[ruleId].description,
    conditions: rules[ruleId].IF,
    conclusion: rules[ruleId].THEN,
    cf: rules[ruleId].CF
    }));

    const diagnosisResult = {
    conclusion: result.label,
    certainty: cf,
    score: score,
    recommendation: result.recommendation,
    timestamp: new Date().toISOString()
    };

    setDiagnosis(diagnosisResult);
    setReasoning(reasoningSteps);

    const newHistory = [...consultationHistory, diagnosisResult];
    setConsultationHistory(newHistory);
    window.storage.set('consultation_history', JSON.stringify(newHistory)).catch(console.error);
    } else {
    setDiagnosis({
    conclusion: 'Data Tidak Cukup',
    certainty: 0,
    score: 0,
    recommendation: 'Informasi yang diberikan belum cukup untuk memberikan penilaian. Silakan lengkapi data pemeriksaan
    bibit sapi.',
    timestamp: new Date().toISOString()
    });
    setReasoning([]);
    }
    };

    const resetConsultation = () => {
    setSymptoms({});
    setDiagnosis(null);
    setReasoning([]);
    setShowExplanation(false);
    };

    const exportToPDF = () => {
    const content = `
    LAPORAN PENILAIAN BIBIT SAPI POTONG
    Tanggal: ${new Date().toLocaleString('id-ID')}

    HASIL PENILAIAN:
    Kesimpulan: ${diagnosis.conclusion}
    Skor Kelayakan: ${diagnosis.score}/100
    Tingkat Kepercayaan: ${Math.round(diagnosis.certainty * 100)}%

    REKOMENDASI:
    ${diagnosis.recommendation}

    GEJALA YANG DIAMATI:
    ${Object.keys(symptoms).map(s => `- ${s.replace(/_/g, ' ')}`).join('\n')}

    PROSES PENALARAN:
    ${reasoning.map((r, i) => `${i + 1}. ${r.rule}: ${r.description} (CF: ${r.cf})`).join('\n')}
    `.trim();

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `penilaian_sapi_${Date.now()}.txt`;
    a.click();
    };

    const addRule = (newRule) => {
    const ruleId = `R${Object.keys(rules).length + 1}`;
    const updatedRules = { ...rules, [ruleId]: newRule };
    setRules(updatedRules);
    window.storage.set('cattle_rules', JSON.stringify(updatedRules)).catch(console.error);
    };

    const deleteRule = (ruleId) => {
    const updatedRules = { ...rules };
    delete updatedRules[ruleId];
    setRules(updatedRules);
    window.storage.set('cattle_rules', JSON.stringify(updatedRules)).catch(console.error);
    };

    const filteredRules = Object.entries(rules).filter(([id, rule]) =>
    searchQuery === '' ||
    id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    rule.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    rule.THEN.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
        <div className="container mx-auto px-4 py-8 max-w-6xl">
            {/* Header */}
            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                <h1 className="text-3xl font-bold text-green-800 mb-2">
                    Sistem Pakar Penilaian Bibit Sapi Potong
                </h1>
                <p className="text-gray-600">Berbasis Standar Nasional Indonesia (SNI) - Kelompok 6</p>
            </div>

            {/* Navigation */}
            <div className="bg-white rounded-lg shadow-lg p-4 mb-6">
                <div className="flex flex-wrap gap-2">
                    <button onClick={()=> setCurrentPage('home')}
                        className={`px-4 py-2 rounded-lg font-medium ${currentPage === 'home' ? 'bg-green-600
                        text-white' : 'bg-gray-200 text-gray-700'}`}
                        >
                        Konsultasi
                    </button>
                    <button onClick={()=> setCurrentPage('rules')}
                        className={`px-4 py-2 rounded-lg font-medium ${currentPage === 'rules' ? 'bg-green-600
                        text-white' : 'bg-gray-200 text-gray-700'}`}
                        >
                        Kelola Aturan
                    </button>
                    <button onClick={()=> setCurrentPage('history')}
                        className={`px-4 py-2 rounded-lg font-medium ${currentPage === 'history' ? 'bg-green-600
                        text-white' : 'bg-gray-200 text-gray-700'}`}
                        >
                        Riwayat
                    </button>
                    <button onClick={()=> setCurrentPage('about')}
                        className={`px-4 py-2 rounded-lg font-medium ${currentPage === 'about' ? 'bg-green-600
                        text-white' : 'bg-gray-200 text-gray-700'}`}
                        >
                        Tentang
                    </button>
                </div>
            </div>

            {/* Main Content */}
            {currentPage === 'home' && (
            <div className="grid md:grid-cols-2 gap-6">
                {/* Input Section */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                        <FileText className="mr-2" /> Input Pemeriksaan
                    </h2>

                    {Object.entries(symptomCategories).map(([category, items]) => (
                    <div key={category} className="mb-6">
                        <h3 className="font-semibold text-lg text-green-700 mb-3">{category}</h3>
                        {items.map(item => (
                        <label key={item.id} className="flex items-start mb-3 cursor-pointer">
                            <input type="checkbox" checked={symptoms[item.id] || false} onChange={(e)=> {
                            const newSymptoms = { ...symptoms };
                            if (e.target.checked) {
                            newSymptoms[item.id] = item.cf;
                            } else {
                            delete newSymptoms[item.id];
                            }
                            setSymptoms(newSymptoms);
                            }}
                            className="mt-1 mr-3"
                            />
                            <span className="text-gray-700">{item.label}</span>
                        </label>
                        ))}
                    </div>
                    ))}

                    <div className="flex gap-3">
                        <button onClick={diagnose}
                            className="flex-1 bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700">
                            Analisis
                        </button>
                        <button onClick={resetConsultation}
                            className="flex-1 bg-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-400">
                            Reset
                        </button>
                    </div>
                </div>

                {/* Result Section */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                        <CheckCircle className="mr-2" /> Hasil Penilaian
                    </h2>

                    {diagnosis ? (
                    <div>
                        <div className={`p-4 rounded-lg mb-4 ${diagnosis.score>= 80 ? 'bg-green-100' : diagnosis.score
                            >= 60 ? 'bg-yellow-100' : 'bg-red-100'}`}>
                            <h3 className="font-bold text-xl mb-2">{diagnosis.conclusion}</h3>
                            <div className="mb-2">
                                <span className="font-semibold">Skor Kelayakan:</span> {diagnosis.score}/100
                            </div>
                            <div className="mb-2">
                                <span className="font-semibold">Kepercayaan:</span> {Math.round(diagnosis.certainty *
                                100)}%
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
                                <div className={`h-4 rounded-full ${diagnosis.score>= 80 ? 'bg-green-600' :
                                    diagnosis.score >= 60 ? 'bg-yellow-600' : 'bg-red-600'}`}
                                    style={{ width: `${diagnosis.score}%` }}
                                    ></div>
                            </div>
                        </div>

                        <div className="bg-blue-50 p-4 rounded-lg mb-4">
                            <h4 className="font-semibold mb-2">Rekomendasi:</h4>
                            <p className="text-gray-700">{diagnosis.recommendation}</p>
                        </div>

                        <button onClick={()=> setShowExplanation(!showExplanation)}
                            className="w-full bg-blue-600 text-white py-2 rounded-lg mb-3 hover:bg-blue-700"
                            >
                            {showExplanation ? 'Sembunyikan' : 'Tampilkan'} Penjelasan
                        </button>

                        {showExplanation && (
                        <div className="bg-gray-50 p-4 rounded-lg mb-3">
                            <h4 className="font-semibold mb-3">Proses Penalaran:</h4>
                            {reasoning.map((step, index) => (
                            <div key={index} className="mb-3 p-3 bg-white rounded border-l-4 border-green-500">
                                <div className="font-semibold text-green-700">{step.rule}</div>
                                <div className="text-sm text-gray-600">{step.description}</div>
                                <div className="text-xs text-gray-500 mt-1">
                                    IF: {step.conditions.join(', ')} → THEN: {step.conclusion} (CF: {step.cf})
                                </div>
                            </div>
                            ))}
                        </div>
                        )}

                        <button onClick={exportToPDF}
                            className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 flex items-center justify-center">
                            <Download className="mr-2" size={20} /> Unduh Laporan
                        </button>
                    </div>
                    ) : (
                    <div className="text-center text-gray-500 py-12">
                        <AlertCircle size={48} className="mx-auto mb-4 text-gray-400" />
                        <p>Silakan pilih gejala/kondisi yang diamati lalu klik tombol Analisis</p>
                    </div>
                    )}
                </div>
            </div>
            )}

            {/* Rules Management */}
            {currentPage === 'rules' && (
            <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Kelola Basis Pengetahuan</h2>

                <div className="mb-4 flex gap-2">
                    <input type="text" placeholder="Cari aturan..." value={searchQuery} onChange={(e)=>
                    setSearchQuery(e.target.value)}
                    className="flex-1 px-4 py-2 border rounded-lg"
                    />
                    <button className="bg-green-600 text-white px-4 py-2 rounded-lg flex items-center">
                        <Search size={20} />
                    </button>
                </div>

                <div className="space-y-3">
                    {filteredRules.map(([ruleId, rule]) => (
                    <div key={ruleId} className="border rounded-lg p-4 bg-gray-50">
                        <div className="flex justify-between items-start mb-2">
                            <div className="font-bold text-green-700">{ruleId}</div>
                            <button onClick={()=> deleteRule(ruleId)}
                                className="text-red-600 hover:text-red-800"
                                >
                                <Trash2 size={20} />
                            </button>
                        </div>
                        <div className="text-sm text-gray-700 mb-1">{rule.description}</div>
                        <div className="text-xs text-gray-600">
                            <div><strong>IF:</strong> {rule.IF.join(', ')}</div>
                            <div><strong>THEN:</strong> {rule.THEN}</div>
                            <div><strong>CF:</strong> {rule.CF}</div>
                        </div>
                    </div>
                    ))}
                </div>

                <div className="mt-4 text-center text-gray-600">
                    Total Aturan: {Object.keys(rules).length}
                </div>
            </div>
            )}

            {/* History */}
            {currentPage === 'history' && (
            <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                    <History className="mr-2" /> Riwayat Konsultasi
                </h2>

                {consultationHistory.length > 0 ? (
                <div className="space-y-3">
                    {consultationHistory.slice().reverse().map((item, index) => (
                    <div key={index} className="border rounded-lg p-4 bg-gray-50">
                        <div className="flex justify-between items-start mb-2">
                            <div className="font-semibold">{item.conclusion}</div>
                            <div className="text-sm text-gray-500">
                                {new Date(item.timestamp).toLocaleString('id-ID')}
                            </div>
                        </div>
                        <div className="text-sm">
                            <div>Skor: {item.score}/100</div>
                            <div>Kepercayaan: {Math.round(item.certainty * 100)}%</div>
                        </div>
                    </div>
                    ))}
                </div>
                ) : (
                <div className="text-center text-gray-500 py-12">
                    <History size={48} className="mx-auto mb-4 text-gray-400" />
                    <p>Belum ada riwayat konsultasi</p>
                </div>
                )}
            </div>
            )}

            {/* About */}
            {currentPage === 'about' && (
            <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                    <Info className="mr-2" /> Tentang Sistem
                </h2>

                <div className="space-y-4 text-gray-700">
                    <div>
                        <h3 className="font-semibold text-lg mb-2">Deskripsi</h3>
                        <p>Sistem Pakar untuk Penilaian Kualitas Bibit Sapi Potong berbasis Rule-Based System dengan
                            metode Forward Chaining dan Certainty Factor. Sistem ini membantu peternak dalam menilai
                            kelayakan bibit sapi potong berdasarkan Standar Nasional Indonesia (SNI).</p>
                    </div>

                    <div>
                        <h3 className="font-semibold text-lg mb-2">Kelompok 6</h3>
                        <ul className="list-disc list-inside">
                            <li>YUYUN NAILUFAR</li>
                            <li>MUHAMMAD RAZI SIREGAR</li>
                            <li>REYAN ANDREA</li>
                            <li>FIRAH MAULIDA</li>
                            <li>IKRAM AL GHIFFARI</li>
                            <li>DIO FERDI JAYA</li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="font-semibold text-lg mb-2">Fitur</h3>
                        <ul className="list-disc list-inside">
                            <li>Forward Chaining inference engine</li>
                            <li>Certainty Factor untuk ketidakpastian</li>
                            <li>Explanation facility (WHY & HOW)</li>
                            <li>Knowledge acquisition interface</li>
                            <li>Export laporan</li>
                            <li>Riwayat konsultasi</li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="font-semibold text-lg mb-2">Standar Penilaian</h3>
                        <p>Sistem mengacu pada SNI 7651.6:2015 tentang Bibit Sapi Potong dan pedoman teknis penilaian
                            kualitas ternak dari Kementerian Pertanian RI.</p>
                    </div>
                </div>
            </div>
            )}
        </div>
    </div>
    );
    };

    export default CattleExpertSystem;
