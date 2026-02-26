ETL Crawling Review Aplikasi DANA
Proyek ini mengimplementasikan proses ETL (Extract, Transform, Load) untuk mengumpulkan 10.000 review pengguna aplikasi DANA dari Google Play Store. Data disimpan secara terstruktur dalam database PostgreSQL.

Alur Proses ETL
Proses dijalankan melalui tiga tahapan utama:

| Tahap     | Deskripsi                                                                                                  | Teknologi            |
| --------- | ---------------------------------------------------------------------------------------------------------- | -------------------- |
| Extract   | Mengambil 10.000 review dengan sistem pagination untuk memenuhi target data                                | google-play-scraper  |
| Transform | Menyesuaikan schema data, membersihkan null values, dan mengonversi format waktu (Unix → Formatted String) | Python               |
| Load      | Menyimpan data terstruktur ke database                                                                     | psycopg2, PostgreSQL |

Struktur Tabel dana_reviews
Data disimpan dalam tabel dana_reviews dengan skema berikut:

| Nama Kolom           | Deskripsi                          |
| -------------------- | ---------------------------------- |
| reviewId             | ID unik setiap review              |
| userName             | Nama pengguna                      |
| userImage            | URL foto profil pengguna           |
| content              | Isi teks review                    |
| score                | Rating bintang (1-5)               |
| thumbsUpCount        | Jumlah like/support review         |
| reviewCreatedVersion | Versi aplikasi saat review dibuat  |
| review_datetime      | Waktu review (format datetime)     |
| replyContent         | Balasan dari developer             |
| repliedAt            | Waktu balasan developer            |
| appVersion           | Versi aplikasi terbaru             |
| timestamp_unix       | Waktu review (Unix timestamp)      |
| timestamp_formatted  | Waktu review (YYYY-MM-DD HH:MM:SS) |

Hasil Akhir
| Metrik      | Nilai                                |
| ----------- | ------------------------------------ |
| Target Data | 10.000 baris                         |
| Status      | Sukses                               |
| Output      | 10.000 baris tersimpan di PostgreSQL |

Total waktu eksekusi: Stabil dan efisien untuk skala data ini.