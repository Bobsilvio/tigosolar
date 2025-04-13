# Integrazione Tigo Energy per Home Assistant

Questa è un'integrazione personalizzata per [Home Assistant](https://www.home-assistant.io/) che ti consente di monitorare il tuo **impianto solare Tigo Energy**, inclusi i singoli pannelli, in tempo reale utilizzando le API ufficiali di Tigo.

> ✅ **Importante**: Questa integrazione richiede un abbonamento attivo a **Tigo EI Premium**.  
> Maggiori info: [Piano Tigo EI Premium](https://it.tigoenergy.com/ei-solution/premium)

## 🔧 Funzionalità

- Supporta dati sia a **livello di sistema** che di **singolo pannello**
- Rilevamento automatico di tutti i **pannelli**, raggruppati per Inverter / MPPT / Stringa
- Crea un dispositivo per ogni pannello, con più sensori:
  - Potenza (W)
  - Tensione in ingresso (V)
  - Corrente in ingresso (A)
  - Intensità segnale (RSSI)
- Include sensori riepilogativi di sistema:
  - Energia giornaliera (kWh)
  - Energia anno corrente (kWh)
  - Energia totale (kWh)
  - Potenza corrente DC (W)
- Compatibile con **Energy Dashboard** di Home Assistant
- Utilizza **Tigo API v3** (`api2.tigoenergy.com`)
- Nessun sovraccarico di richieste: uso ottimizzato con un **coordinatore dati condiviso**

## 📆 Installazione

### 1. Installazione manuale

1. Scarica questo repository
2. Copia i file nella cartella `custom_components/tigo/` di Home Assistant
3. Riavvia Home Assistant

### 2. HACS (facoltativo, se pubblicata)

Da aggiungere quando disponibile su HACS.

## ⚙️ Configurazione

1. Vai su **Impostazioni > Dispositivi e Servizi**
2. Clicca su **Aggiungi Integrazione**
3. Cerca **Tigo Energy**
4. Inserisci la tua **email e password dell'account Tigo**
5. Fatto! Le entità saranno create automaticamente

## 🧲 Entità create

### Dispositivi pannello (uno per pannello)

- `sensor.panel_<nome>_power`
- `sensor.panel_<nome>_voltage_in`
- `sensor.panel_<nome>_current_in`
- `sensor.panel_<nome>_rssi`

### Sensori riepilogo sistema

- `sensor.tigo_daily_energy` *(kWh)*
- `sensor.tigo_ytd_energy` *(kWh)*
- `sensor.tigo_lifetime_energy` *(kWh)*
- `sensor.tigo_current_power` *(W)*

Tutti i sensori di energia sono compatibili con `device_class` e `state_class` per una perfetta integrazione nella Energy Dashboard.

## 🔐 Sicurezza

Questa integrazione richiede l'autenticazione con **email e password dell'account Tigo**. Le credenziali sono gestite in modo sicuro tramite le entry di configurazione di Home Assistant. Tutte le comunicazioni con i server Tigo avvengono tramite HTTPS.

## 🧱 Dipendenze

- `aiohttp` (installata automaticamente da Home Assistant)

## 🛠️ Note tecniche

- Le API Tigo sono soggette a **rate limit**. L'integrazione effettua **una singola richiesta per parametro** e distribuisce i dati a tutti i sensori
- Utilizza `DataUpdateCoordinator` per gestire cache e aggiornamenti ogni 60 secondi (pannelli) e ogni 5 minuti (riepilogo sistema)
- Il layout del sistema viene recuperato una volta durante l'avvio

## 🙏 Ringraziamenti

Sviluppato e mantenuto da [il tuo nome o username GitHub]

Ispirato al lavoro di [MartinStoffel's Tigo Integration](https://github.com/MartinStoffel/tigo)

---

**Non affiliato con Tigo Energy. Utilizzo a proprio rischio.**