// Import Firebase SDK
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js";
import { getDatabase, ref, push, onChildAdded } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-database.js";

// Config Firebase kamu
const firebaseConfig = {
  apiKey: "API_KEY_KAMU",
  authDomain: "PROJECT_ID.firebaseapp.com",
  databaseURL: "https://PROJECT_ID-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "PROJECT_ID",
  storageBucket: "PROJECT_ID.appspot.com",
  messagingSenderId: "SENDER_ID",
  appId: "APP_ID"
};

// Inisialisasi Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

// Fungsi kirim pesan
window.kirimPesan = function() {
  const nama = document.getElementById("namaInput").value.trim() || "Anonim";
  const pesan = document.getElementById("pesanInput").value.trim();
  if (pesan !== "") {
    push(ref(database, "pesan"), {
      nama: nama,
      teks: pesan,
      waktu: new Date().toLocaleString()
    });
    document.getElementById("pesanInput").value = "";
  } else {
    alert("Pesan tidak boleh kosong!");
  }
};

// Tampilkan pesan realtime
const daftarPesan = document.getElementById("daftarPesan");
onChildAdded(ref(database, "pesan"), (snapshot) => {
  const data = snapshot.val();
  const kotak = document.createElement("div");
  kotak.className = "pesan";
  kotak.innerHTML = `
    <strong>${data.nama}</strong><br>
    ${data.teks}
    <small>${data.waktu}</small>
  `;
  daftarPesan.prepend(kotak);
});