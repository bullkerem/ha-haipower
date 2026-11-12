# ☀️ HaiPower Solar & Battery (Aohai Digital Power) — Home Assistant Integration

[![GitHub Release](https://img.shields.io/github/v/release/bullkerem/ha-haipower?style=for-the-badge&color=brightgreen)](https://github.com/bullkerem/ha-haipower/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://github.com/hacs/integration)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.8%2B-18BCF2?style=for-the-badge&logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/bullkerem/ha-haipower?style=for-the-badge&color=yellow)](https://github.com/bullkerem/ha-haipower/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/bullkerem/ha-haipower?style=for-the-badge&color=orange)](https://github.com/bullkerem/ha-haipower/issues)
[![Last Commit](https://img.shields.io/github/last-commit/bullkerem/ha-haipower?style=for-the-badge&color=purple)](https://github.com/bullkerem/ha-haipower/commits/main)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bullkerem&repository=ha-haipower&category=integration)

**HaiPower** / **Aohai Digital Power** (`cloud.aohaidigitalpower.com` / `eu.aohaidigitalpower.com` / `solarhaipower.com`) hibrit güneş enerjisi inverterleri ve batarya depolama sistemleri için geliştirilmiş **Home Assistant** özel bileşeni (custom integration).

Custom Home Assistant integration for **HaiPower** / **Aohai Digital Power** hybrid solar inverters and battery storage systems (e.g., `HUA-15K3P-BL`, `HUA` series).

---

## ✨ Özellikler / Features

- 🔐 **Otomatik Cihaz & İstasyon Keşfi (Auto-Discovery):** Sadece HaiPower mobil uygulama e-posta ve şifrenizi girmeniz yeterlidir. İnverter Seri Numarası (`DSN`), Veri Kaydedici (`CSN`), İstasyon Adı ve İnverter Modeli buluttan otomatik olarak çekilir.
- ⚡ **24 Adet Gerçek Zamanlı Sensör:** Güneş (PV) üretimi, Batarya doluluk oranı (`SOC %`), şarj/deşarj gücü, ev anlık ve günlük tüketimi, şebeke alış/satış verileri ve 3 faz gerilimleri 60 saniyede bir güncellenir.
- 📊 **Home Assistant Enerji Paneli (Energy Dashboard) Uyumlu:** Tüm enerji (`kWh`) sensörleri `SensorDeviceClass.ENERGY` ve `SensorStateClass.TOTAL_INCREASING` sınıflarına sahiptir; doğrudan Home Assistant **Enerji** sekmesine eklenebilir.
- 🌍 **Çoklu Sunucu Desteği:** Global (`cloud.aohaidigitalpower.com`), Avrupa (`eu.aohaidigitalpower.com`) ve `solarhaipower.com` sunucularını destekler.
- 🇹🇷 / 🇬🇧 **Türkçe ve İngilizce Arayüz Desteği:** Kurulum ekranı (Config Flow) Türkçe ve İngilizce dil dosyalarıyla birlikte gelir.

---

## 📦 Kurulum / Installation

### Yöntem 1: HACS ile Kurulum (Önerilen / Recommended)

1. Home Assistant'ta **HACS** -> **Integrations** bölümüne gidin.
2. Sağ üstteki üç noktaya (`⋮`) tıklayıp **Custom repositories** (Özel depolar) seçeneğini açın.
3. **Repository** kısmına bu GitHub deposunun adresini yapıştırın, **Category** olarak **Integration** (veya **entegre**) seçip **Add** butonuna basın.
4. Listede **HaiPower Solar & Battery (Aohai Digital Power)** eklentisini bulup **Download** (İndir) butonuna tıklayın.
5. **Home Assistant'ı yeniden başlatın.**

### Yöntem 2: Manuel Kurulum / Manual Installation

1. Bu depodaki `custom_components/haipower` klasörünü indirin.
2. Kendi Home Assistant sunucunuzdaki `/config/custom_components/haipower` dizinine kopyalayın:
   ```text
   /config/custom_components/haipower/
   ├── __init__.py
   ├── config_flow.py
   ├── const.py
   ├── manifest.json
   ├── sensor.py
   ├── strings.json
   └── translations/
       ├── en.json
       └── tr.json
   ```
3. **Home Assistant'ı yeniden başlatın.**

---

## ⚙️ Yapılandırma / Configuration

1. Home Assistant'ta **Ayarlar (Settings)** -> **Cihazlar ve Hizmetler (Devices & Services)** sayfasına gidin.
2. Sağ alttaki **+ Entegrasyon Ekle (+ Add Integration)** butonuna tıklayın.
3. Arama kutusuna **HaiPower** yazın ve seçin.
4. Açılan pencerede:
   - **E-posta / Kullanıcı Adı:** HaiPower mobil uygulamasındaki e-posta adresiniz
   - **Şifre:** HaiPower şifreniz
   - **Bulut Sunucu Bölgesi:** Varsayılan olarak `Global Cloud (cloud.aohaidigitalpower.com)` seçilidir (Türkiye'deki çoğu kurulum bu sunucudadır).
   - **İnverter Seri No (DSN):** Boş bırakabilirsiniz (otomatik bulunur). Birden fazla inverteriniz varsa eklemek istediğiniz inverterin `DSN` numarasını girebilirsiniz.

---

## 📡 Oluşturulan Sensörler / Provided Sensors (24 Entities)

| Kategori | Sensör Adı | Entity ID (Örnek) | Birim | API Alanı |
| :--- | :--- | :--- | :--- | :--- |
| **☀️ Güneş (PV)** | Güneş Anlık Üretim | `sensor.haipower_gunes_anlik_uretim` | `kW` | `ppvAll` |
| **☀️ Güneş (PV)** | Güneş Günlük Üretim | `sensor.haipower_gunes_gunluk_uretim` | `kWh` | `epVAllToday` |
| **☀️ Güneş (PV)** | Güneş Aylık Üretim | `sensor.haipower_gunes_aylik_uretim` | `kWh` | `epvMonth` |
| **☀️ Güneş (PV)** | Güneş Yıllık Üretim | `sensor.haipower_gunes_yillik_uretim` | `kWh` | `epvYear` |
| **☀️ Güneş (PV)** | Güneş Toplam Üretim | `sensor.haipower_gunes_toplam_uretim` | `kWh` | `epvTotal` |
| **☀️ Güneş (PV)** | PV1 Gerilim | `sensor.haipower_pv1_gerilim` | `V` | `vpv1` |
| **☀️ Güneş (PV)** | PV2 Gerilim | `sensor.haipower_pv2_gerilim` | `V` | `vpv2` |
| **🔋 Batarya** | Batarya Doluluk (SOC) | `sensor.haipower_batarya_doluluk_soc` | `%` | `soc` |
| **🔋 Batarya** | Batarya Gerilimi | `sensor.haipower_batarya_gerilimi` | `V` | `vbat` |
| **🔋 Batarya** | Batarya Anlık Şarj Gücü | `sensor.haipower_batarya_anlik_sarj_gucu` | `kW` | `pcharge` |
| **🔋 Batarya** | Batarya Anlık Deşarj Gücü | `sensor.haipower_batarya_anlik_desarj_gucu` | `kW` | `pdischarge` |
| **🔋 Batarya** | Batarya Günlük Şarj | `sensor.haipower_batarya_gunluk_sarj` | `kWh` | `echargeToday` |
| **🔋 Batarya** | Batarya Günlük Deşarj | `sensor.haipower_batarya_gunluk_desarj` | `kWh` | `edischargeToday` |
| **🏠 Ev Tüketimi** | Ev Anlık Tüketim | `sensor.haipower_ev_anlik_tuketim` | `kW` | `plocalLoadtotal` |
| **🏠 Ev Tüketimi** | Ev Günlük Tüketim | `sensor.haipower_ev_gunluk_tuketim` | `kWh` | `eloadToday` |
| **🏠 Ev Tüketimi** | Ev Aylık Tüketim | `sensor.haipower_ev_aylik_tuketim` | `kWh` | `eloadMonth` |
| **🏠 Ev Tüketimi** | Ev Toplam Tüketim | `sensor.haipower_ev_toplam_tuketim` | `kWh` | `eloadTotal` |
| **🗼 Şebeke** | Şebekeden Çekilen Anlık Güç | `sensor.haipower_sebekeden_cekilen_anlik_guc` | `kW` | `pactouserTotal` |
| **🗼 Şebeke** | Şebekeye Verilen Anlık Güç | `sensor.haipower_sebekeye_verilen_anlik_guc` | `kW` | `pactogridtotal` |
| **🗼 Şebeke** | Şebekeden Günlük Çekilen Enerji | `sensor.haipower_sebekeden_gunluk_cekilen_enerji` | `kWh` | `efromGridToday` |
| **🗼 Şebeke** | Şebekeye Günlük Verilen Enerji | `sensor.haipower_sebekeye_gunluk_verilen_enerji` | `kWh` | `etoGridToday` |
| **🗼 Şebeke** | Şebekeden Toplam Çekilen Enerji | `sensor.haipower_sebekeden_toplam_cekilen_enerji` | `kWh` | `efromGridTotal` |
| **🗼 Şebeke** | Şebekeye Toplam Verilen Enerji | `sensor.haipower_sebekeye_toplam_verilen_enerji` | `kWh` | `etoGridTotal` |
| **ℹ️ Durum** | İnverter Durumu | `sensor.haipower_inverter_durumu` | Metin | `status2` + ek öznitelikler (`vac1`, `vac2`, `vac3`, `co2_saved_tons`, `trees_planted`) |

---

## 🔋 Home Assistant Enerji Paneli (Energy Dashboard) Eşleştirmesi

Home Assistant **Ayarlar -> Panolar -> Enerji** menüsünde şu sensörleri seçebilirsiniz:

- **Elektrik Şebekesi (Grid Consumption):** `sensor.haipower_sebekeden_gunluk_cekilen_enerji` (veya `toplam`)
- **Şebekeye Geri Dönüş (Return to Grid):** `sensor.haipower_sebekeye_gunluk_verilen_enerji` (veya `toplam`)
- **Güneş Panelleri (Solar Production):** `sensor.haipower_gunes_gunluk_uretim` (veya `toplam`)
- **Ev Batarya Depolaması (Battery Systems):**
  - Bataryaya giren enerji: `sensor.haipower_batarya_gunluk_sarj`
  - Bataryadan çıkan enerji: `sensor.haipower_batarya_gunluk_desarj`

---

## 🆕 Sürüm Geçmişi / Changelog

### v1.1.0
- 🏷️ Dinamik GitHub Release, Home Assistant (`2023.8+`), HACS tek tıkla kurulum (`My Home Assistant`), yıldız, sorun ve son commit rozetleri eklendi.
- 🎨 `sensor.py` içindeki MDI ikon adları (`mdi:white-balance-sunny`, `mdi:home-import-outline`) küçük harf standardına göre düzeltildi.
- 📦 `manifest.json` sürümü `1.1.0` olarak güncellendi.

### v1.0.0
- 🚀 İlk sürüm: HaiPower / Aohai Digital Power bulut API otomatik keşfi, 24 gerçek zamanlı sensör, Energy Dashboard uyumu ve TR/EN dil desteği.

---

## 📄 Lisans / License

Bu proje [MIT Lisansı](LICENSE) altında açık kaynak olarak paylaşılmıştır. Herkes özgürce kullanabilir, geliştirebilir ve paylaşabilir.
