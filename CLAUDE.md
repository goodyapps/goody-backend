# Goody Backend — Claude instrukcijos

## TAUPYMO REŽIMAS
- Pagalvok ar būtina rašyti kodą prieš rašant
- Neskaityk failų kurių nereikia užduočiai
- Netestuok kiekvieno žingsnio — testuok tik kai reikia
- Vienas git commit po kelių susijusių pakeitimų
- Neklausk patvirtinimo — daryk iš karto

## PROJEKTO KONTEKSTAS
- **Projektas**: Goody — kainų palyginimo app
- **Backend**: Python/Flask — `server.py` (vienas failas)
- **Frontend**: Vanilla HTML/JS — `C:\Users\giedrius.simonaviciu\projektai\goody-app\index.html` (vienas failas)
- **Deployment**: Render (backend) + GitHub auto-deploy
- **API raktai**: visi Render environment variables — niekada neklausk jų
- **Aktyvios parduotuvės**: Varle.lt, Elesen.lt, Amazon.DE, Amazon.PL

## DARBŲ PRIORITETAI
1. Paieškos greitis
2. Paieškos tikslumas
3. Kainos minimizavimas (ScraperAPI kreditai, AI tokenai)

## TAISYKLĖS
- Taisyk tik kas tikrai sulaužyta — nekeisk kas veikia
- Nekurk naujų failų jei galima redaguoti esamą
- Nekomentuok akivaizdžių dalykų kode
- Trumpi atsakymai — mažiau tokenų
