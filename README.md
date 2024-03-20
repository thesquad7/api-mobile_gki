# API Mobile GKI V.1

# Get Started
## Memulai memuat kebutuhan server
pastikan server yang di gunakan untuk deploy telah memiliki
 * python = **Versi 3.8** ke atas
 * python3-pip telah terinstall
 * memiliki git

## Tahap instalasi
**Ubuntu/Debian**
python 
```bash
sudo apt-get install python3
```
python3-pip
```bash
sudo apt-get install python3-pip
```
git
```bash
sudo apt-get install git
```

**FEDORA/RHEL** 
python
```bash
yum install python3
```
python3-pip
```bash
yum install python3-pip
```
git
```bash
yum apt-get install git
```
**Arc/RedHat** 
python
```bash
pacman install python3
```
python3-pip
```bash
pacman install python3-pip
```
git
```bash
pacman apt-get install git
```
# Penyiapan Ecosistem API

## Clone Project
Siapkan folder yang akan menampung project, pada folder terkait buka **prompt executor pilihan** anda,
dalam kasus ini saya mengunakan **bash** (apapun prompt yang digunakan tidak akan membedakan script code untuk eksekusi)

isi perintah di bawah

```bash
git clone https://github.com/thesquad7/api-mobile_gki.git
```
saat proses berakhir lakukan
Linux/Mac
```bash
ls
```
Windows
```bash
dir
```
maka akan muncul data folder
```bash
api_mobile_gki
```
kamu dapat mengubah folder terkait dengan nama yang proper, pastikan tidak memiliki spasi saat melakukan penamaan ulang
kemudian masuk ke folder
```bash
api_mobile_gki
```
## instalasi dependency python
untuk mengetahui kebutuhan dari project ini anda dapat membuka file **requirement.txt**

lakukan instalasi dengan perintah berikut
```bash
pip install "nama dependency"
```
instal seluruh paket secara **Beurutan**
⚠️ **Perhatian:** dependency bcrypt harus pada versi **4.0.1**, versi diatasnya mengalami bug

## Penambahan folder untuk repository gambar
buatlah folder berikut pada main direktori projek. dan sub foldernya
this is the schema
 * [image]
   * [jadwal_bg]
   * [jadwal_pendeta]
   * [feedback_img]
   * [jemaat_img]
   * [renungan_bg]
   * [acara_bg]
   * [gereja_img]
  


