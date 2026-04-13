import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def vektoru_ciz():
    try:
        # Vektör A koordinatları
        ax1 = float(entry_ax1.get())
        ay1 = float(entry_ay1.get())
        ax2 = float(entry_ax2.get())
        ay2 = float(entry_ay2.get())

        # Vektör B koordinatları
        bx1 = float(entry_bx1.get())
        by1 = float(entry_by1.get())
        bx2 = float(entry_bx2.get())
        by2 = float(entry_by2.get())

    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm alanlara sayısal değer girin.")
        return

    # Vektör yönlerini hesapla
    a_yon_x = ax2 - ax1
    a_yon_y = ay2 - ay1

    b_yon_x = bx2 - bx1
    b_yon_y = by2 - by1

    # Varsayılan değerler tanımla
    sonuc_baslangic_x = 0
    sonuc_baslangic_y = 0
    sonuc_bitis_x = 0
    sonuc_bitis_y = 0
    fark_veya_toplam = "Belirtilmedi"  # Varsayılan değer

    # İşlem türüne göre hesaplama yap
    if islem_turu.get() == "toplama":
        sonuc_baslangic_x = ax1
        sonuc_baslangic_y = ay1
        sonuc_bitis_x = ax2 + (bx2 - bx1)
        sonuc_bitis_y = ay2 + (by2 - by1)
        sonuc_fark.config(text=f"Uç Uca Toplama: ({sonuc_baslangic_x:.2f}, {sonuc_baslangic_y:.2f}) → ({sonuc_bitis_x:.2f}, {sonuc_bitis_y:.2f})")
        fark_veya_toplam = "Uç Uca Toplama"
    elif islem_turu.get() == "vektorel_toplama":
        # Uzunluk ve yönlere göre toplama, başlangıç noktası mantığına göre
        a_vec = np.array([a_yon_x, a_yon_y])
        b_vec = np.array([b_yon_x, b_yon_y])
        a_mag = np.linalg.norm(a_vec)
        b_mag = np.linalg.norm(b_vec)
        a_dir = a_vec / a_mag if a_mag != 0 else np.array([0, 0])
        b_dir = b_vec / b_mag if b_mag != 0 else np.array([0, 0])
        dot = np.dot(a_dir, b_dir)
        # Her durumda sonuç vektörü A ve B'nin başlangıçlarının ortasından başlasın
        ortax = (ax1 + bx1) / 2
        ortay = (ay1 + by1) / 2
        # Yatay mı dikey mi baskın?
        if dot < -0.999:
            if a_mag >= b_mag:
                sonuc_mag = a_mag - b_mag
                sonuc_dir = a_dir
            else:
                sonuc_mag = b_mag - a_mag
                sonuc_dir = b_dir
        elif dot > 0.999:
            sonuc_mag = a_mag + b_mag
            sonuc_dir = a_dir
        else:
            sonuc_vec = a_vec + b_vec
            sonuc_mag = np.linalg.norm(sonuc_vec)
            sonuc_dir = sonuc_vec / sonuc_mag if sonuc_mag != 0 else np.array([0, 0])
        # Vektörün yönüne dik birim vektör bul (2D'de: (y, -x) veya (-y, x))
        dik_x = -sonuc_dir[1]
        dik_y = sonuc_dir[0]
        kaydir_miktar = 1
        sonuc_baslangic_x = ortax + kaydir_miktar * dik_x
        sonuc_baslangic_y = ortay + kaydir_miktar * dik_y
        sonuc_bitis_x = sonuc_baslangic_x + sonuc_mag * sonuc_dir[0]
        sonuc_bitis_y = sonuc_baslangic_y + sonuc_mag * sonuc_dir[1]
        sonuc_fark.config(text=f"Uzunluklara Göre Toplama: ({sonuc_baslangic_x:.2f}, {sonuc_baslangic_y:.2f}) → ({sonuc_bitis_x:.2f}, {sonuc_bitis_y:.2f})")
        fark_veya_toplam = "Uzunluklara Göre Toplama"
    elif islem_turu.get() == "cikarma":
        sonuc_baslangic_x = ax1
        sonuc_baslangic_y = ay1
        sonuc_bitis_x = ax2 - (bx2 - bx1)
        sonuc_bitis_y = ay2 - (by2 - by1)
        sonuc_fark.config(text=f"Uç Uca Çıkarma: ({sonuc_baslangic_x:.2f}, {sonuc_baslangic_y:.2f}) → ({sonuc_bitis_x:.2f}, {sonuc_bitis_y:.2f})")
        fark_veya_toplam = "Uç Uca Çıkarma"
    elif islem_turu.get() == "paralel":
        sonuc_baslangic_x = ax1
        sonuc_baslangic_y = ay1
        a_magnitude = np.sqrt(a_yon_x**2 + a_yon_y**2)
        b_magnitude = np.sqrt(b_yon_x**2 + b_yon_y**2)
        dot_product = a_yon_x * b_yon_x + a_yon_y * b_yon_y
        magnitude_product = a_magnitude * b_magnitude
        cos_theta = dot_product / magnitude_product
        theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))
        sonuc_magnitude = np.sqrt(a_magnitude**2 + b_magnitude**2 + 2 * a_magnitude * b_magnitude * np.cos(theta))
        sonuc_bitis_x = sonuc_baslangic_x + sonuc_magnitude * np.cos(theta / 2)
        sonuc_bitis_y = sonuc_baslangic_y + sonuc_magnitude * np.sin(theta / 2)
        sonuc_fark.config(text=f"Paralel Kenar: ({sonuc_baslangic_x:.2f}, {sonuc_baslangic_y:.2f}) → ({sonuc_bitis_x:.2f}, {sonuc_bitis_y:.2f})")
        fark_veya_toplam = "Paralel Kenar"

    # Sonuçları güncelle
    sonuc_a.config(text=f"A yönü: ({a_yon_x:.2f}, {a_yon_y:.2f})")
    sonuc_b.config(text=f"B yönü: ({b_yon_x:.2f}, {b_yon_y:.2f})")

    # Grafiği temizle ve yeniden çiz
    ax.clear()

    # Eksen sınırlarını hesapla
    tum_x = [ax1, ax2, bx1, bx2, sonuc_bitis_x, 0]
    tum_y = [ay1, ay2, by1, by2, sonuc_bitis_y, 0]
    max_sinir = max(max(abs(x) for x in tum_x), max(abs(y) for y in tum_y), 5) + 2

    ax.set_xlim(-0.5, max_sinir)
    ax.set_ylim(-0.5, max_sinir)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Vektör Gösterimi ({fark_veya_toplam})")

    ok_ayar = dict(head_width=max_sinir * 0.04, head_length=max_sinir * 0.04, length_includes_head=True)

    # Yansımaları sadece paralel kenar yönteminde çiz
    if islem_turu.get() == "paralel":
        paralel_bx1 = ax2
        paralel_by1 = ay2
        paralel_bx2 = ax2 + b_yon_x
        paralel_by2 = ay2 + b_yon_y
        paralel_ax1 = bx2
        paralel_ay1 = by2
        paralel_ax2 = bx2 + a_yon_x
        paralel_ay2 = by2 + a_yon_y
        ax.plot([paralel_bx1, paralel_bx2], [paralel_by1, paralel_by2], linestyle="dotted", color="blue", lw=1)
        ax.plot([paralel_ax1, paralel_ax2], [paralel_ay1, paralel_ay2], linestyle="dotted", color="red", lw=1)

    # Vektör A — mavi
    ax.annotate("", xy=(ax2, ay2), xytext=(ax1, ay1),
        arrowprops=dict(arrowstyle="-|>", color="#185FA5", lw=2))
    ax.text((ax1 + ax2) / 2 + 0.2, (ay1 + ay2) / 2 + 0.2,
        f"A ({a_yon_x:.1f}, {a_yon_y:.1f})", color="#185FA5", fontsize=7, fontweight='bold')

    # Vektör B — turuncu/kırmızı
    ax.annotate("", xy=(bx2, by2), xytext=(bx1, by1),
        arrowprops=dict(arrowstyle="-|>", color="#993C1D", lw=2))
    ax.text((bx1 + bx2) / 2 + 0.2, (by1 + by2) / 2 + 0.2,
        f"B ({b_yon_x:.1f}, {b_yon_y:.1f})", color="#993C1D", fontsize=7, fontweight='bold')

    # Sonuç vektörü — yeşil, orijinden başlar
    ax.annotate("", xy=(sonuc_bitis_x, sonuc_bitis_y), xytext=(sonuc_baslangic_x, sonuc_baslangic_y),
        arrowprops=dict(arrowstyle="-|>", color="#07DC15", lw=2, linestyle='dashed'))
    # Sonuç vektörü uzunluğunu her üç işlemde de göster (uç uca toplama, paralel kenar, uzunluklara göre toplama)
    if islem_turu.get() in ["toplama", "paralel", "vektorel_toplama"]:
        s_uzunluk = np.sqrt((sonuc_bitis_x - sonuc_baslangic_x) ** 2 + (sonuc_bitis_y - sonuc_baslangic_y) ** 2)
        ax.text((sonuc_baslangic_x + sonuc_bitis_x) / 2 + 0.2, (sonuc_baslangic_y + sonuc_bitis_y) / 2 + 0.2,
            f"   R |R|={s_uzunluk:.2f}", color="#07DC15", fontsize=7, fontweight='bold')
    else:
        ax.text((sonuc_baslangic_x + sonuc_bitis_x) / 2 + 0.2, (sonuc_baslangic_y + sonuc_bitis_y) / 2 + 0.2,
            f"   R ({sonuc_bitis_x:.1f}, {sonuc_bitis_y:.1f})", color="#07DC15", fontsize=7, fontweight='bold')

    # Başlangıç noktalarını işaretle
    ax.plot(ax1, ay1, 'o', color="#185FA5", markersize=5)
    ax.plot(ax2, ay2, 'o', color="#185FA5", markersize=5)
    ax.plot(bx1, by1, 'o', color="#993C1D", markersize=5)
    ax.plot(bx2, by2, 'o', color="#993C1D", markersize=5)
    ax.plot(sonuc_baslangic_x, sonuc_baslangic_y, 'o', color="#07DC15", markersize=5)

    # Lejant
    lejant = [
        mpatches.Patch(color="#185FA5", label="Vektör A"),
        mpatches.Patch(color="#993C1D", label="Vektör B"),
        mpatches.Patch(color="#07DC15", label=f"R ({fark_veya_toplam})"),
    ]
    ax.legend(handles=lejant, loc='upper left', fontsize=9)

    canvas.draw()


# --- Ana pencere ---
pencere = tk.Tk()
pencere.title("Vektör Uygulaması")
pencere.resizable(False, False)

# --- Sol panel (girişler) ---
sol = tk.Frame(pencere, padx=16, pady=16)
sol.pack(side=tk.LEFT, fill=tk.Y)

def baslik(parent, metin, renk="#185FA5"):
    tk.Label(parent, text=metin, font=("Arial", 11, "bold"), fg=renk).pack(anchor='w', pady=(10, 2))

def koordinat_satiri(parent, etiket):
    cerceve = tk.Frame(parent)
    cerceve.pack(anchor='w', pady=2)
    tk.Label(cerceve, text=etiket, width=8, font=("Arial", 9)).pack(side=tk.LEFT)
    entry = tk.Entry(cerceve, width=6, font=("Arial", 10), justify='center')
    entry.pack(side=tk.LEFT, padx=2)
    entry.insert(0, "0")
    return entry

# Vektör A girişleri
baslik(sol, "Vektör A", "#185FA5")
entry_ax1 = koordinat_satiri(sol, "x1 (başl.):")
entry_ay1 = koordinat_satiri(sol, "y1 (başl.):")
entry_ax2 = koordinat_satiri(sol, "x2 (bitiş):")
entry_ay2 = koordinat_satiri(sol, "y2 (bitiş):")

# Vektör B girişleri
baslik(sol, "Vektör B", "#993C1D")
entry_bx1 = koordinat_satiri(sol, "x1 (başl.):")
entry_by1 = koordinat_satiri(sol, "y1 (başl.):")
entry_bx2 = koordinat_satiri(sol, "x2 (bitiş):")
entry_by2 = koordinat_satiri(sol, "y2 (bitiş):")

# Çiz butonu
tk.Button(sol, text="Çiz", font=("Arial", 11, "bold"),
          bg="#185FA5", fg="white", padx=10, pady=6,
          command=vektoru_ciz).pack(pady=16, fill=tk.X)

# Sonuçlar
tk.Label(sol, text="Sonuçlar", font=("Arial", 10, "bold")).pack(anchor='w')
sonuc_a   = tk.Label(sol, text="A yönü: —", font=("Arial", 9), fg="#185FA5")
sonuc_b   = tk.Label(sol, text="B yönü: —", font=("Arial", 9), fg="#993C1D")
sonuc_fark = tk.Label(sol, text="A - B:  —", font=("Arial", 9, "bold"), fg="#07DC15")
sonuc_a.pack(anchor='w')
sonuc_b.pack(anchor='w')
sonuc_fark.pack(anchor='w')

# --- Yeni seçenekler için değişken ---
islem_turu = tk.StringVar(value="fark")  # Varsayılan olarak "fark" seçili

# --- Sol panelde işlem seçimi ---
baslik(sol, "İşlem Türü", "#000000")
tk.Radiobutton(sol, text="Uç Uca Toplama", variable=islem_turu, value="toplama", font=("Arial", 10)).pack(anchor='w')
#tk.Radiobutton(sol, text="Uç Uca Çıkarma", variable=islem_turu, value="cikarma", font=("Arial", 10)).pack(anchor='w')
tk.Radiobutton(sol, text="Paralel Kenar", variable=islem_turu, value="paralel", font=("Arial", 10)).pack(anchor='w')
tk.Radiobutton(sol, text="Toplama (Uzunluklara Göre)", variable=islem_turu, value="vektorel_toplama", font=("Arial", 10)).pack(anchor='w')

# --- Sağ panel (grafik) ---
fig, ax = plt.subplots(figsize=(6, 6))
fig.tight_layout(pad=2)

canvas = FigureCanvasTkAgg(fig, master=pencere)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Başlangıç grafiği
ax.set_xlim(-0.5, 10)
ax.set_ylim(-0.5, 10)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.4)
ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Vektör Gösterimi")
canvas.draw()

pencere.mainloop()