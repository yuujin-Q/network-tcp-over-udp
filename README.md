# Implementasi protokol TCP-like Go-Back-N

> Tugas Besar 1
> IF3130 - Jaringan Komputer

## Deskripsi Tugas

### Deskripsi Singkat

Berikut adalah deskripsi (tujuan) dari tugas besar ini:

- Memahami esensi-esensi dari protokol Transmission Control Protocol (TCP) atas dua hal: reliability dan congestion
  control.
- Membuat program sederhana yang memanfaatkan socket programming sebagai fungsi utamanya.
- Membuat dan memahami cara pengiriman data sederhana lewat jaringan menggunakan protokol transport layer.

### Link Spesifikasi

[IF3130 - Tugas Besar 1](https://docs.google.com/document/d/1X_EaDFzL4pKTPDygLlIKAWCwahGTEIciDMsArVXriAY/edit?usp=sharing)

## Deskripsi Implementasi

### Fitur

Fitur terdiri atas pengiriman file dari server ke berbagai client. Implementasi TCP menggunakan bantuan UDP socket.

Fitur-fitur bonus yang diimplementasikan adalah sebagai berikut:

- Threading (Parallel File Transfer)
- TicTacToe
- ECC
- Komunikasi di dua (atau lebih) _end device_

### Cara penggunaan

#### Server

Akses `server.py` dari root. Berikut adalah tampilan bantuan dari perintah `python server.py -h`

```
usage: server.py [-h] [--ip IP] port filename

server host for file transfer

positional arguments:
  port        specifies port number
  filename    specifies filename

options:
  -h, --help  show this help message and exit
  --ip IP     set server ip, defaults to localhost
```

Contoh penggunaan adalah sebagai berikut.

```shell
python server.py 1000 file.txt --ip 127.0.0.1
```

Pada contoh ini, port server adalah 1000, file adalah file.txt dari _current working dir_. Parameter IP opsional,
dan parameter ini menyatakan IP server (default ke localhost).

#### ClientInstance

Akses `clientinstance.py` dari root. Berikut adalah tampilan bantuan dari perintah `python clientinstance.py -h`

```

usage: clientinstance.py [-h] [--src_ip [SRC_IP]] src_port dest_ip dest_port

client host for file transfer

positional arguments:
src_port specifies client port number
dest_ip specifies server ip
dest_port specifies server port number

options:
-h, --help show this help message and exit
--src_ip [SRC_IP]  set client ip, defaults to localhost

```

Contoh penggunaan adalah sebagai berikut.

```shell
python clientinstance.py 1000 127.0.0.1 5000 --src_ip 127.0.0.1
```

Pada contoh ini, port client adalah 1000, address server adalah 127.0.0.1:5000. Parameter src_ip opsional,
dan parameter ini menyatakan IP client (default ke localhost).

#### Urutan Pemanggilan

Aktifkan `server.py`, kemudian aktifkan `clientinstance.py` (instansiasi client dapat dilakukan berkali-kali). Ikut
prompt pada terminal masing-masing server/client.

## Pembagian Tugas

| Nama                     | NIM      | Task                                          |
|--------------------------|----------|-----------------------------------------------|
| Eugene Yap Jin Quan      | 13521074 | Connection, MessageInfo, Threading            |
| Ulung Adi Putra          | 13521122 | Segment Struct, ECC, TicTacToe                |
| Johann Christian Kandani | 13521138 | Node (Client/ServerHandler), Segment Handling |
