# GazyavaTeam — LMML 2026

Задачи: https://sigmoid.academy/tasks
Решено: 25 / 54


## Europe — Classic ML & Data Science

- [x] **Albania** — Looks like an anomaly! _(Medium)_
- [x] **Belgium** — Fry-ndship _(Easy)_
- [x] **Estonia** — This Data Is Perfect! _(Medium)_
- [x] **Finland** — Pipes, Leaks, and the Graph Beneath _(Medium)_
- [ idk how to solve ] **France** — Point par point _(Easy)_ 
- [ ] **Germany** — Black Box _(Hard)_
- [x] **Greece** — Just a siblings' thing _(Medium)_
- [x] **Iceland** — What The Data? _(Easy)_
- [ ] **Moldova** — Feather Stories _(Hard)_
- [x] **Norway** — The Nisse's Bad Shift _(Medium)_
- [x] **Portugal** — The Douro Paradox _(Medium)_
- [ ] **Romania** — Shaken, Still Standing _(Hard)_
- [x] **Spain** — ¡Feliz Navidad! _(Easy)_
- [x] **Switzerland** — The Weak Layer _(Easy)_
- [ ] **United Kingdom** — Call My BLEUff _(Medium)_

## Asia — Computer Vision

- [ ] **Bhutan** — The 300-Year Old Tiger Nest Painting _(Medium)_
- [ ] **China** — Carved in bones, engraved in the heart _(Medium)_
- [x] **India** — Twins Separated at Birth _(Easy)_
- [ ] **Japan** — City of Subtitles _(Hard)_
- [ ] **Kazakhstan** — Stamp of Disapproval _(Hard)_
- [ ] **Laos** — Bad BOMB _(Medium)_
- [ ] **Mongolia** — The Baa-rilliant task! _(Medium)_
- [ ] **Vietnam** — That isn't my shoe! _(Medium)_

## Africa — General AI

- [ ] **Algeria** — Here, at your service! _(Hard)_
- [x] **Angola** — The Waterline Replay _(Medium)_
- [ ] **Côte d’Ivoire** — The Abidjan Transit Ledger _(Medium)_
- [x] **Egypt** — Always Valid, No Excuses _(Easy)_
- [ ] **Ethiopia** — The Azmari's Borrowed Melody _(Medium)_
- [ ] **Morocco** — The Dispatch Desk of Fez _(Medium)_
- [ ] **Mozambique** — The Professor of Maputo Bay _(Hard)_
- [x] **Nigeria** — The Gángan Never Lies _(Easy)_
- [x] **Rwanda** — The Drying Floor at Karongi _(Easy)_
- [x] **Senegal** — The Teranga FM Token Diet _(Medium)_
- [x] **South Africa** — Ngiyakuzwa? _(Easy)_
- [x] **Tanzania** — Please, You Are So Delusional! _(Easy)_

## North America — NLP

- [ ] **Canada** — Two Solitudes _(Hard)_
- [ ] **Costa Rica** — Pura Vida, No PII _(Medium)_
- [ ] **Cuba** — If you know, you know! _(Hard)_
- [x] **Mexico** — Ruta de las Identidades _(Easy)_
- [ ] **Panama** — The Canal Knows Too Much _(Medium)_
- [x] **United States** — The Great American Token Mystery _(Easy)_

## South America — AI Security & Adversarial ML

- [ ] **Argentina** — Carta para la Abuela _(Hard)_
- [ ] **Bolivia** — The Forest Went Quiet _(Medium)_
- [ ] **Brazil** — Don't Pull My Triggers _(Hard)_
- [x] **Chile** — The Second Lock _(Medium)_
- [ idk how to solve ] **Colombia** — Looks Good to Me! — Bogotá Sound Check _(Easy)_
- [x] **Ecuador** — Ciclopaseo Mirage _(Medium)_
- [ ] **Peru** — The Knots You Cannot Read _(Medium)_
- [x] **Venezuela** — Signal from the Sierra Nevada _(Easy)_

## Oceania — Reinforcement Learning

- [x] **Australia** — The Drunken Mario Adventures _(Medium)_
- [x] **Fiji** — Walu Season _(Easy)_
- [ ] **New Zealand** — The Braided River Run _(Hard)_
- [x] **Papua New Guinea** — Bihainim Angkol (Follow Your Uncle) _(Medium)_
- [ ] **Samoa** — Island Duel: the homeward chart _(Medium)_

## Шпаргалка к опросу: как решали

| Задача | Суть решения | Папка |
|---|---|---|
| Albania | Детектор учит обычные плавные колебания датчиков и тревожит, если один датчик сильно выбился или несколько чуть-чуть, но долго | [albania](albania) |
| Belgium | Регрессия края поля только на то, что декларирует фермер (периметр прямоугольника + канава); остатки рисуют слово | [belgium](belgium) |
| Estonia | Один заявитель встречается несколько раз -> утечка между train и test; LeaveOneGroupOut по (дата рождения, гражданство) даёт честные 0.7666 | [estonia](estonia) |
| Finland | Чистка названий городов (пробелы, точки, регистр, умлауты, шведские названия), граф без дублей, топ-7 по степени | [finland](finland) |
| Greece | Точность у всех 0.95, но пропуск угрозы дороже ложной тревоги -> берём модель с максимальным recall (ARES) | [greece](greece) |
| Iceland | Правила очистки: пропуск комментариев, дубли, запятая в числах, F -> C, починка кодировки названий | [iceland](iceland) |
| Norway | Плохая ночь = подряд идущие образцы, где две цифры перепутаны; SVM находит такие серии, внутри меняем a <-> b | [norway](norway) |
| Portugal | Перебрали все колонки и разбиения; полный парадокс Симпсона даёт только расстояние от Порту (лечение стояло в основном на дальних участках) | [portugal](portugal) |
| Spain | Фильтр по справедливой цене за единицу, таблица товар x пилот рисует слово | [spain](spain) |
| Switzerland | Дерево с параметрами по умолчанию; первые буквы признаков в узлах (обход в прямом порядке) дают слово | [Switzerland](Switzerland) |
| India | Кандидаты по похожим миниатюрам, проверка SIFT + гомография: дубликат совпадает почти пиксель в пиксель | [india](india) |
| Angola | Сравнили 3 прогона агента: неверный ответ дала устаревшая запись памяти SIGMOID_MEM_KILAMBA | [angola](angola) |
| Egypt | Правила чистят OCR-шум, локальная LLM пишет JSON, грамматика GBNF не даёт выдать невалидный JSON | [egypt](egypt) |
| Nigeria | Флаг нарисован в спектрограмме звука (3-4 кГц) | [Nigeria](Nigeria) |
| Rwanda | inspect_batch не записывал approved -> бесконечный цикл; исправление в одну строку | [rwanda](rwanda) |
| Senegal | Вопросы независимы -> для каждого перебор 16 вариантов маршрутизации, берём самый дешёвый проходящий | [senegal](senegal) |
| Tanzania | Починили RAG: одна модель эмбеддингов, префикс passage:, документы целиком, архивные выкинуты | [tanzania](tanzania) |
| Mexico | Цифры в адресе не портятся -> ключ = отсортированные цифры адреса, все пары внутри группы | [Mexico](Mexico) |
| United States | Перебор токенизаторов tiktoken: какой точно повторяет калибровочные ID, тем и декодируем | [usa](usa) |
| Australia | Кода нет: обученный агент берёт 7 монет из 20; взято/пропущено = биты, по 5 бит на букву -> TANH | [australia](australia) |
| Fiji | Многорукий бандит: UCB1 с коэффициентом 3 (уловы в кг, а не 0-1) | [fiji](fiji) |
| Papua New Guinea | Правила лагуны известны -> точное решение MDP обратной индукцией | [papua](papua) |
| South Africa, Venezuela, Chile | Решены без кода в репо, объясняет тот, кто решал | - |
