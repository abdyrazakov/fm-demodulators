# FM Демодуляторы на GNU Radio

Готовые GNU Radio Python flowgraph'ы для демодуляции FM-записей в WAV. Сгенерированы из `.grc` (GNU Radio Companion 3.10).

| Файл | Формат входа | Источник записи |
|---|---|---|
| `demodulater.py` | unsigned 8-bit, интерливированные I/Q | SDR (RTL-SDR), эфирная запись, 2.048 МГц |
| `demodulater_omur.py` | complex float32 (cf32), интерливированные I/Q | Синтетический WBFM baseband, 192 кГц, 0 Гц |

---

## `demodulater.py` — демодуляция u8 RF (эфирный FM)

Демодулирует запись IQ с SDR, сохранённую как байты **unsigned char** (`u8`), чередующиеся `I0,Q0,I1,Q1,...`.

```
File Source (byte, 2.048 МГц)
  → Throttle (2 × samp_rate)
  → Deinterleave (2 потока: I и Q)
  → uchar → float → × 1/128 → − 1.0      (0..255 → примерно −1..+1)
  → Float → Complex
  → Freq Xlating FIR (CCC, decim=8, сдвиг на 700 кГц, ФНЧ 70 кГц / 20 кГц)
  → WFM Receiver (quad_rate = 256 кГц, audio_decimation = 8)
  → WAV Sink (32 кГц, mono, PCM16)
```

**Параметры:**

| Переменная | Значение |
|---|---|
| `samp_rate` | 2.048e6 |
| `quad_rate` | samp_rate / 8 = 256e3 |
| `audio_rate` | quad_rate / 8 = 32e3 |
| Центр (Freq Xlating FIR) | 700e3 |

> Файлы записываются по абсолютным путям — перед запуском поправь пути в `blocks.file_source` / `blocks.wavfile_sink`.

---

## `demodulater_omur.py` — демодуляция cf32 WBFM (синтетический baseband)

Демодулирует комплексный float32 IQ (синтетический WBFM, несущая на **0 Гц**, девиация 45 кГц).

```
File Source (complex, 192 кГц)
  → Quadrature Demod  (gain = samp_rate / (2π × freq_dev))
  → Low Pass Filter (fff, decim=4, ФНЧ 15 кГц / 3 кГц)
  → WAV Sink (48 кГц, mono, PCM16)
```

**Параметры:**

| Переменная | Значение |
|---|---|
| `samp_rate` | 192e3 |
| `freq_dev` | 45e3 |
| `gain` | 192000 / (2π × 45000) ≈ 0.679 |
| `audio_rate` | 48e3 |

> Квадратурный демодулятор выбран вместо broadcast-приёмника: он точно соответствует синтетической девиации 45 кГц и не добавляет deemphasis.

---

## Запуск

Требуется GNU Radio:

```bash
python3 demodulater.py        # u8 RF -> WAV 32 кГц
python3 demodulater_omur.py   # cf32 WBFM -> WAV 48 кГц
```

Исходники самих схем (`demodulater.grc`, `demodulater_omur.grc`) можно открыть в GNU Radio Companion.