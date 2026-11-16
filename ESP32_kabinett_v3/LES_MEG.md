# Følelsespanel – avrundet kabinett v3

Ny, parametrisk konstruksjon inspirert av referansebildet fra Tuverud.com.
Dette er ikke de tidligere STL-filene fra nettsiden. Den har avrundede hjørner,
skjulte bakskruer, lysramme, knapp under skjermen og kabelåpning på høyre side.

Modellen er kontrollert digitalt, men er **ikke fysisk prøveprintet**. Bildet er
en illustrasjon og gir ikke mål på de faktiske komponentene. Målene fra den
tidligere prosjektpakken er derfor utgangspunktet for skjerm og knapp.

## Filene du skriver ut

| Fil | Antall | Materiale / funksjon |
| --- | --- | --- |
| `01_Hus_og_front.stl` | 1 | Hvit PLA eller PETG, hus og front i én del |
| `02_Baklokk.stl` | 1 | Samme materiale, skrus fra baksiden |
| `03_Lysdiffusor.stl` | 1 | Natur/translucent PETG eller lysgjennomslippelig hvit PLA |
| `04_Provebit_knapp_og_passning.stl` | 1 først | Liten prøve av knapphull og 0,25 mm passklarering |
| `05_Provebit_innlegg.stl` | 1 først | Innlegg til passningsprøven |

Alle STL-er bruker millimeter, riktig skala og har flat utskriftsside på Z = 0.
`Sammenstilling_for_visning.glb` er kun til 3D-visning. Den skal ikke skrives ut
som én sammenstilt del. Skjerm, knapp og elektronikk følger ikke med i STL-ene.

## Mål og forutsetninger

| Egenskap | Mål |
| --- | --- |
| Ferdig hus, bredde × høyde × dybde | 82 × 126 × 36 mm |
| Utvendig hjørneradius | 8 mm |
| Sidevegger / bakplate | 2,4 / 2,4 mm |
| Skjermåpning, stående | 33,5 × 43,5 mm |
| Skjermmodulens lomme | 41,5 × 66,5 mm |
| Antatt skjermmodul | ca. 40 × 65 mm, rotert til stående |
| Skjermens senter | 12 mm over husets midtpunkt |
| Knapphull | Ø 12,3 mm for nominell 12 mm gjenge |
| Paneltykkelse ved knappen | 2,4 mm |
| Plass til knappemutter fra innsiden | Ø 22 mm |
| Knappens senter | 48 mm under husets midtpunkt |
| LED-kanal, utvendig mål | 67 × 91 mm |
| LED-kanal, innvendig mål | 45 × 69 mm |
| Rett kanalbredde / dybde | 11 / 7,5 mm |
| Diffusor, utvendig mål / tykkelse | 66,5 × 90,5 / 1,2 mm |
| Klarering diffusor per side | 0,25 mm |
| Klarering baklokkets styrekant per side | 0,30 mm |
| Kabelåpning på høyre side | 14 mm høy × 8 mm i dybderetningen, R2 |

Skjermlommen forutsetter at det synlige skjermområdet er sentrert på modulen.
Det finnes forskjellige ST7789-kort med ulike rammer, plasseringer og
pinnekontakter. Kontroller modulens faktiske bredde, høyde, synlige område og
kontaktplassering før full utskrift. Skjermfronten ligger 2 mm bak frontplanet.

Kabelåpningen er en gjennomføring for kabel/USB-plugg. Den fester ikke en bestemt
USB-kontakt og er ikke tilpasset et bestemt ESP32-korts kontaktsenter.

## LED-rammen

Kanalen har en hel 1,8 mm bunn, slik at området rundt skjermen henger mekanisk
sammen med huset. Rammen er ikke et løst skjermfelt i et gjennomgående spor.

Bruk fire rette, opptil 10 mm brede WS2812B-segmenter som lyser fremover.
Stripa skal ikke brettes sideveis rundt hjørnene: forbind segmentene med ledninger.
Kontroller at segmentenes klippepunkter passer tilgjengelig lengde:

- Vertikale sider: omtrent 66 mm fri, kontrollert plass til 10 mm bred stripe.
- Topp og bunn: omtrent 50 mm fri, kontrollert plass til 10 mm bred stripe.
- LED-høyde over kanalbunnen bør være maks. ca. 2 mm for å beholde lysavstand.

To Ø 3,6 mm hull i kanalbunnen fører ledninger til innsiden. Test LED-ene før
diffusoren festes. Hold diffusoren i flukt med frontflaten, og bruk små punkter
klart, egnet lim langs diffusorens ytterkant. Det er ingen innvendig stoppkant;
limet holder den i riktig dybde. Unngå å presse den ned på LED-ene.
Passningen er med klarering og er ikke en garantert låsende presspasning.
Diffusoren gir lysgjennomgang; lysfarge og jevnhet bestemmes av filament,
LED-avstand og de faktiske LED-ene.

## Utskrift og montering

1. Skriv ut de to små prøvebitene. Kontroller 12 mm-knappen og at innlegget går
   i sporet uten kraft. Sporet er 4,0 mm og innlegget 3,5 mm bredt.
2. Sjekk skjermmålene i tabellen. Print eventuelt bare de første 2–3 mm av huset
   i sliceren for å kontrollere frontåpningene før en full utskrift.
3. Print hus og baklokk i levert orientering. Utgangspunkt: 0,20 mm lag,
   3–4 vegger, 5 topp-/bunnlag og 15–20 % infill. Tilpass eget materiale.
4. LED-kanalens tak blir en kort bro på ca. 11–14 mm når fronten ligger ned.
   Kontroller broforhåndsvisningen i sliceren. Bruk broinnstillinger eller
   fjernbar støtte i kanalen hvis printeren trenger det. Støtte kan tas ut
   fra fronten før diffusoren monteres. Den runde USB-åpningen kan også trenge
   litt støtte. Ikke fyll hele elektronikkrommet med støtte uten behov.
5. Print diffusoren separat, flatt, med 100 % infill ved 0,20 mm lag.
6. Sett inn skjermmodulen fra baksiden. Bruk smale striper egnet dobbeltsidig
   montasjetape på lommens anslag, eller egne tilpassede klemmer.
   Det er ikke antatt noen bestemt PCB-hullavstand, så modellen har ikke
   universelle skjermskruehull. Unngå trykk direkte på LCD-panelet.
7. Monter knappen med dens mutter fra innsiden. Sett inn LED-segmentene og
   før ledningene gjennom de to små hullene. Fest ESP32 med isolerende
   montasjepad på innsiden av baklokket. Kontroller plass til kort, knappekropp,
   kontakter og ledninger før lokket lukkes.
8. Skru sammen med fire **M2,5 × 8 mm selvskjærende plastskruer med senkhode**.
   Pilotene er Ø 2,0 mm og 9 mm dype. Dette er ikke gjengede maskinskruehull.
   Skru for hånd, og stopp når delene ligger an. Skruehodet må passe den
   Ø 5,5 mm og ca. 1,4 mm dype forsenkningen. Mål skruene du faktisk bruker.

## Digital kontroll

`kontrollrapport.json` dokumenterer at hver printdel er én lukket solid med
konsistente normaler og positivt volum. Sammensatte deler er kontrollert uten
volumkollisjon. Åpningene for skjerm, knapp og sidekabel, skjermlommens antatte
PCB-volum og fire rette LED-segmenters plass er kontrollert geometrisk.
Dette erstatter ikke prøvemontering eller kalibrering av printerens toleranser.

## Tilpasning

`generate_enclosure.py` inneholder alle mål i parameterordboken `P` øverst.
`maal_og_parametere.json` er en lesbar oversikt, ikke en separat konfigurasjonsfil
som skriptet leser. Rediger `P` og kjør skriptet på nytt ved andre komponentmål.
Avhengigheter: Python 3.12+, numpy, trimesh, manifold3d og scipy.
Forhåndsvisningsskriptet bruker i tillegg matplotlib og Pillow.

Dato: 16. november 2026. Designversjon: v3.0.0, prøvepassmodell.
