# 💎 VIP Ekonomi Botu

Discord sunucun için hazırlanmış, sandık etkinliği ve el alıştırması (hız) etkinliği olan VIP tarzı bir ekonomi botu.

## Özellikler

- 🎁 **Sandık Etkinliği** — Rastgele zaman aralıklarında, 5 sandıklı VIP görsel gönderilir. Kullanıcılar bir sandığa tıklayarak rastgele miktarda coin kazanır. Her sandık ve her kullanıcı etkinlik başına sadece bir kez katılabilir.
- ⚡ **El Alıştırması Etkinliği** — Rastgele zaman aralıklarında, üzerinde rastgele harf/rakamlardan oluşan bir kod bulunan görsel gönderilir. Kodu ilk doğru yazan kullanıcı ödülü kapar.
- 💰 Slash komutları: `/bakiye`, `/liderlik`, `/istatistik`, `/coin-ver`, `/coin-al`, `/sandik-baslat`, `/hiz-baslat`
- 🗄️ SQLite ile kalıcı bakiye/istatistik kaydı (bot yeniden başlasa da veriler kaybolmaz)
- 🎨 Pillow ile üretilen özel VIP görseller (altın/mor sandık teması, renkli hız kodu)

## Kurulum

### 1. Botu Discord Developer Portal'da oluştur

1. https://discord.com/developers/applications adresine git, **New Application** ile bir uygulama oluştur.
2. Sol menüden **Bot** sekmesine gir, **Add Bot** de.
3. **MESSAGE CONTENT INTENT** ve **SERVER MEMBERS INTENT** seçeneklerini aç (el alıştırmasında mesaj içeriğini okumak için zorunlu).
4. **Reset Token** ile bir token oluştur ve kopyala (bunu kimseyle paylaşma!).

### 2. Botu sunucuna davet et

**OAuth2 → URL Generator** sekmesinde:
- Scopes: `bot`, `applications.commands`
- Bot Permissions: `Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`, `Use Slash Commands`

Oluşan linki tarayıcında aç ve botu sunucuna ekle.

### 3. Proje dosyalarını hazırla

```bash
pip install -r requirements.txt
cp .env.example .env
```

`.env` dosyasını aç ve şunları doldur:

- `DISCORD_TOKEN` → 1. adımda aldığın token
- `GUILD_ID` → Sunucunun ID'si (Discord'da Ayarlar → Gelişmiş → Geliştirici Modu açık olmalı, sonra sunucuya sağ tık → ID Kopyala)
- `CHEST_CHANNEL_ID` → Sandık etkinliğinin gönderileceği kanalın ID'si
- `SPEED_CHANNEL_ID` → El alıştırması etkinliğinin gönderileceği kanalın ID'si

İstersen ödül miktarlarını, aralıkları ve para birimi adını/emojisini de `.env` üzerinden özelleştirebilirsin.

### 4. Botu çalıştır

```bash
python main.py
```

Bot açıldığında konsolda "... olarak giriş yapıldı" yazısını görürsün ve komutlar sunucunda anında kullanılabilir olur.

## Komutlar

| Komut | Açıklama |
|---|---|
| `/bakiye [kullanıcı]` | Kendi veya başka birinin bakiyesini gösterir |
| `/liderlik` | En zengin 10 kullanıcıyı listeler |
| `/istatistik [kullanıcı]` | Açılan sandık, kazanılan hız etkinliği sayısı vb. gösterir |
| `/coin-ver <kullanıcı> <miktar>` | (Sadece yöneticiler) Kullanıcıya coin ekler |
| `/coin-al <kullanıcı> <miktar>` | (Sadece yöneticiler) Kullanıcıdan coin düşer |
| `/sandik-baslat` | (Sadece yöneticiler) Sandık etkinliğini beklemeden hemen başlatır |
| `/hiz-baslat` | (Sadece yöneticiler) El alıştırması etkinliğini beklemeden hemen başlatır |

## Özelleştirme fikirleri

- `utils/image_gen.py` içindeki renkleri değiştirerek sunucunun kendi temasına (örn. sunucu logon renklerine) uydurabilirsin.
- `config.py` üzerinden ödül aralıklarını ve etkinlik sıklıklarını istediğin gibi ayarlayabilirsin.
- Sandık sayısını değiştirmek istersen `chest_event.py` içinde `generate_chest_image(5)` ve `rewards` listesindeki `5` değerini güncelle.
- İleride mağaza, günlük ödül (`/gunluk`), çekiliş gibi özellikler eklemek istersen yeni bir `cogs/` dosyası olarak ekleyip `main.py` içindeki `load_extension` listesine eklemen yeterli.

## Notlar

- Veriler `data/economy.db` dosyasında SQLite formatında tutulur. Bu dosyayı yedeklemeni öneririm.
- Botu 7/24 açık tutmak istersen bir VPS, Raspberry Pi veya Railway/Render gibi bir barındırma servisi kullanabilirsin.
