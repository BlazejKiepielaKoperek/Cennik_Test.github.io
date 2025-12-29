# 📱 N Studios - Streamlit Instrukcja

## 🚀 Szybki Start (Lokalnie)

### Krok 1: Instalacja Zależności

```bash
pip install -r requirements.txt
```

### Krok 2: Konfiguracja WhatsApp (Twilio)

1. Przejdź do [twilio.com/try-twilio](https://www.twilio.com/try-twilio) i zarejestruj się
2. Pobierz dane uwierzytelniające:
   - **Account SID**
   - **Auth Token**
3. Aktywuj WhatsApp Sandbox:
   - Messaging → Try it out → Send a WhatsApp message
   - Wyślij kod `join` do numeru Twilio

### Krok 3: Utwórz Plik .env

Skopiuj `.env.example` do `.env`:

```bash
copy .env.example .env
```

Wypełnij danymi:

```env
TWILIO_ACCOUNT_SID=AC1234567890abcdef...
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+48123456789
```

### Krok 4: Uruchom Aplikację

```bash
streamlit run app.py
```

Aplikacja otworzy się w przeglądarce na `http://localhost:8501`

---

## 🌐 Deployment na Streamlit Cloud

### Krok 1: Przygotowanie Repozytorium

1. Utwórz nowe repozytorium GitHub
2. Dodaj pliki:
   - `app.py`
   - `requirements.txt`
   - `.gitignore` (już utworzony)

**NIE dodawaj pliku `.env` do repozytorium!**

```bash
git init
git add app.py requirements.txt .gitignore STREAMLIT_INSTRUCTIONS.md
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TWOJ_USERNAME/n-studios-calculator.git
git push -u origin main
```

### Krok 2: Deploy na Streamlit Cloud

1. Przejdź do [share.streamlit.io](https://share.streamlit.io)
2. Zaloguj się przez GitHub
3. Kliknij **"New app"**
4. Wybierz:
   - Repository: `TWOJ_USERNAME/n-studios-calculator`
   - Branch: `main`
   - Main file path: `app.py`

### Krok 3: Konfiguracja Secrets (Zmienne Środowiskowe)

W panelu Streamlit Cloud:

1. Kliknij **"Advanced settings"**
2. Dodaj do **Secrets**:

```toml
TWILIO_ACCOUNT_SID = "AC1234567890abcdef..."
TWILIO_AUTH_TOKEN = "your_auth_token_here"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
YOUR_WHATSAPP_NUMBER = "whatsapp:+48123456789"
```

3. Kliknij **"Deploy"**

Twoja aplikacja będzie dostępna pod adresem:
`https://TWOJ_USERNAME-n-studios-calculator.streamlit.app`

---

## 🎨 Funkcje Aplikacji

### Tryb Tradycyjny
- Wybór sprzętu (Sony FX3 / ARRI Alexa / RED Komodo)
- Wybór studia (Brak / Cyklorama / Ściana LED)
- Zakres długości: 15-120 sekund
- Złożoność: Montaż / VFX / 3D

### Tryb AI Reklama
- Uproszczona konfiguracja
- Tylko długość wideo
- 100 PLN za sekundę

### Powiadomienia WhatsApp
Po wypełnieniu formularza otrzymasz wiadomość z:
- Trybem produkcji
- Szacowaną ceną
- Danymi kontaktowymi klienta
- Pełną konfiguracją

---

## 🔧 Rozwiązywanie Problemów

### Problem: "ModuleNotFoundError: No module named 'streamlit'"
**Rozwiązanie:**
```bash
pip install -r requirements.txt
```

### Problem: Nie otrzymuję WhatsApp
**Rozwiązania:**
1. Sprawdź czy wysłałeś kod `join` do Twilio Sandbox
2. Upewnij się że format numeru to `whatsapp:+48...` (bez spacji)
3. Sprawdź Twilio Console → Messaging Logs

### Problem: Błąd Twilio credentials
**Rozwiązanie:**
- Lokalnie: Sprawdź plik `.env`
- Streamlit Cloud: Sprawdź sekcję **Secrets** w ustawieniach

### Problem: Aplikacja nie ładuje się na Streamlit Cloud
**Rozwiązanie:**
1. Sprawdź logi w panelu Streamlit Cloud
2. Upewnij się że `requirements.txt` zawiera wszystkie zależności
3. Sprawdź czy secrets są poprawnie skonfigurowane

---

## 📊 Aktualizacja Aplikacji

### Lokalnie
Po zmianach w `app.py`, Streamlit automatycznie wykryje zmiany.
Naciśnij **"Rerun"** w przeglądarce.

### Streamlit Cloud
```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud automatycznie zdeployuje nową wersję.

---

## 🎯 Zaawansowane Opcje

### Własna Domena
W panelu Streamlit Cloud możesz dodać własną domenę CNAME.

### Analytics
Dodaj Google Analytics:
```python
# W app.py, w sekcji <head>
st.components.v1.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
""")
```

### Multiple Recipients
W `.env` dodaj więcej numerów (rozdzielonych przecinkami):
```env
YOUR_WHATSAPP_NUMBER=whatsapp:+48111111111,whatsapp:+48222222222
```

Zaktualizuj `app.py`:
```python
recipients = os.getenv('YOUR_WHATSAPP_NUMBER').split(',')
for recipient in recipients:
    client.messages.create(...)
```

---

## 💡 Wskazówki

✅ Streamlit automatycznie odświeża przy zmianach  
✅ Używaj `st.cache_data` dla funkcji wymagających czasie  
✅ WhatsApp Sandbox Twilio działa 72h - po tym wyślij ponownie `join`  
✅ W produkcji rozważ WhatsApp Business API  

---

## 📞 Potrzebujesz Pomocy?

- [Streamlit Docs](https://docs.streamlit.io)
- [Twilio WhatsApp Docs](https://www.twilio.com/docs/whatsapp)
- [Streamlit Community](https://discuss.streamlit.io)

---

**Gratulacje! Twoja aplikacja N Studios działa na Streamlit! 🎬**
