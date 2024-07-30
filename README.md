# IMEAR autocalc
Adviesbasis voor Effecten van Rijksbeleid Integratie en Uniformering Stikstofdepositie (AERIUS) en InformatieModelAERius (IMAER) bieden rekentools om de ruimte te berekenen en door te voeren. Voor het berekenen van de ruimte kunnen punten, lijnen en vlakken worden gebruikt. Deze worden geconverteerd naar een GML-bestand waarmee de plug-in werkt. Met de AERIUS IMAER QGIS plug-in kunnen GML-bestanden ingeladen worden en worden geconverteerd naar een Geopackage. Vervolgens is het mogelijk om berekeningen van de depositie van NO en NH3 te maken op de hexagoon vlakken. Met de tool is mogelijk om te sommeren, af te trekken en/of het maximum te berekenen. De ImaerAutoCalc plug-in maakt gebruik van deze rekeninstrumenten van de AERIUS IMAER plug-in maar bied een intuïtieve manier om de verschillen in kaart te brengen. Het resultaat is voldoende ruimte of onvoldoende, waarbij onvoldoende de aanvragen moet wachten tot er meer ruimte ter beschikking is.

# Dependencies
* IMAER Plugin versie <= 3.5.0
* Geteste versies: 3.4.3, 3.5.0

# Inhoud
1.	Korte handleiding	
2.	Verschilberekeningen doorvoeren in de plugin
3.	GML-bestanden inladen in QGIS
4.	Berekeningen met ImaerAutoCalc
5.	Opslaan van de Difference layer
6.	Geavanceerde mogelijkheden
Bijlage 1: Installeren IMAER en ImaerAutoCalc plug-in
  Installeer IMAER plug-in
  Installeer ImaerAutoCalc plug-in

# 1.	Korte handleiding
1.	Aanvraag omzetten naar een GML rekenbestand in AERIUS Calculator (exporteren vanuit Rekentaak in AERIUS Calculator export omgeving, zorg dat er geen “.” in de naam staat)
2.  Start de ImaerAutoCalc plug-in
3.	Druk op start
4.	Importeer GML-bestanden met ‘Import IMAER Calculator result GML’ 
5.	Bij foutmelding .gpkg bestanden: zie opmerking onder hoofdstuk 3
6.	Sleep de saldogevers en -nemers onder de juiste groep 
7.  Vink zichtbaarheid aan voor de saldogevers en -nemers waarmee de berekening moet worden uitgevoerd 
8.	Start de berekening 
9.	Herhaal stap 5 tot 8 naar wens

# 2.	Verschilberekeningen doorvoeren in de plugin
Het komt regelmatig voor dat projecten reeds een referentiesituatie hebben waarmee zij intern kunnen salderen. Met name voor PAS-melders blijft hier echter nog een vraag naar meer ruimte omdat de referentiesituatie niet voldoende is voor de beoogde situatie. Er is dan nog extra ruimte nodig om het project te kunnen vergunnen. Om de benodigde ruimte correct te kunnen bereken, dient de interne saldering toegepast te worden voordat de berekening vanaf hoofdstuk 4 voortgezet kan worden. 

1.	Voer de verschilberekening van het project uit in AERIUS-Calculator. Zorg voor een duidelijke naamgeving voor de referentie- en de beoogde situatie. 
2.	Exporteer de resultaat GML bestanden (uit rekentaak bij exporteren), zorg dat de verschilberekening uitgevoerd is voordat je exporteert. Je krijgt een Zip-folder waarin twee GML bestanden te vinden zijn: de referentiesituatie en de beoogde situatie. 
3.	Voer de stappen onder hoofdstuk 3 uit om de bestanden te importeren naar de QGIS omgeving. 
4.	Zet vervolgens de referentiesituatie volgens stap 1 onder hoofdstuk 4 onder de “Saldonemer”, en de beoogde situatie onder “Saldogevers”. Dit is nodig zodat de ruimte uit de referentiesituatie van de beoogde situatie afgetrokken wordt, en de benodigde ruimte boven 0 blijft staan.  
5.	Voer de rest van de stappen uit zoals weergegeven onder hoofdstuk 4. 
6.	Je krijgt nu de nog resterende benodigde ruimte van het project na intern salderen in de Difference Layer te zien. Deze kan opgeslagen worden zoals weergegeven in hoofdstuk 5. 
7.	Na het opslaan van de resultaten kunnen de oorspronkelijke GLM bestanden uit de Saldogever en Saldonemer lagen verwijderd worden. 
8.	Vervolgens kan de verschilberekening onder de laag “Saldonemers” gezet worden. Hiermee kunnen vervolgens de gewenste berekeningen uitgevoerd worden.


# 3.	GML-bestanden inladen in QGIS
  
Voor het inladen van een GML-bestand van AERIUS moet de IMAER plug-in geïnstalleerd zijn en aan staan, zie bijlage 1. Wanneer de IMAER plug-in is geïnstalleerd zijn de tools te vinden in de toolbar. Laad de GML-bestanden in met de tool ‘Import IMAER Calculator result GML’  . Is de tool grijs gekleurd en kan er niet op geklikt worden zie dan bijlage 1. Zoek het juiste bestand   en druk op ‘openen’  .

Tip: Als de ImaerAutoCalc al een keer gestart is staan de juiste groepen al klaar. Als de juiste groep geselecteerd is wordt bij het openen van de GML-bestand de laag direct onder deze groep gezet.

1.  Druk op ‘Import IMAER Calculator result GML’
2.	Zoek en selecteer het juiste GML-bestand
3.	Druk op Openen om het in te laden in QGIS

Let op! Als er al een Geopackage (.gpkg) van het bestand is gemaakt wordt er een foutmelding gegeven en moet de Geopackage eerst verwijderd worden.

# 4.	Berekeningen met ImaerAutoCalc
Met de ImaerAutoCalc plug-in kan snel opsommingen en verschilberekeningen gemaakt worden. Er zijn twee mogelijkheden om de berekening uit te voeren. De eerste is door het gebruik van de start knop, elke keer wanneer een berekening uitgevoerd moet worden. De tweede manier is door AutoCalc functie. Hierbij wordt de berekening uitgevoerd elke keer wanneer de zichtbaarheid van een laag veranderd.

1.  Start de ImaerAutoCalc plug-in
Methode één:

1.  Verplaats de lagen naar de juiste groep
2.	Vink de lagen aan waar de berekening op uitgevoerd moet worden
3.	Start de berekening

Methode twee:
1.	Verplaats de lagen naar de juiste groep
2.	Activeer de AutoCalc knop  
3.	Vink de lagen aan waar de berekening op uitgevoerd moet worden

Let op! De output is een tijdelijke laag. Bij het afsluiten van het project wordt dit niet opgeslagen. De resultaten kunnen worden opgeslagen of bij de volgende keer opnieuw berekend worden.

Let op! Wanneer AutoCalc aan staat wordt de berekening bij elke gevinkte laag aan of uit geactiveerd. Wacht tot de berekening klaar is voordat een nieuwe laag aan- of uit-gevinkt wordt. 

# 5.	Opslaan van de Difference layer
De verschillen laag kan opgeslagen worden als Geopackage (.gpkg), Excel (.xlsx) en CSV (.csv). Wanneer de verschillen-laag opgeslagen is als geopackage verschijnt dit in een nieuwe groep ‘Export’. Een Excel- of CSV-bestand wordt niet toegevoegd aan het project maar wel alleen in de opgegeven locatie.

1.	Druk op ‘Save Difference layer’
2.	Navigeer naar een locatie waar de laag opgeslagen moet worden
3.	Voer een gewenste bestandsnaam in
4.	Selecteer een gewenst bestandstype
5.	Druk op opslaan

# 6.	Geavanceerde mogelijkheden
Het is mogelijk om exports of geëxporteerde selecties te gebruiken als saldogever of -nemer bij een nieuwe berekening. Sleep in dit geval de laag onder de gewenste groep (saldogever of -nemer). Daarnaast is het mogelijk om externe gegevens te gebruiken in de berekening, zoals bijvoorbeeld lagen uit het Nationaal Georegister. Om het te gebruiken in de tool moeten de kolomnamen overeenkomen. Gebruik hiervoor de geoprocessing tool ‘Refactor fields’ of ‘bijgewerkte velden’.

1.	Laad de externe laag in het project
2.	Open de geoprocessing toolbox
3.	Zoek naar ‘Refactor fields’ of ‘Bijgewerkte velden’
4.	Dubbelklik op de tool om deze te openen.
5.	Selecteer de invoerlaag
6.	Selecteer bij ‘Velden uit sjabloonlaag laden’ een referentielaag 
7.	Klik op ‘Velden laden’
8.	Selecteer bij elke kolom de bijpassende kolom
9.	(Optioneel) Sla de uitkomsten op
10.	Klik op uitvoeren
11.	Verplaats de laag naar de juiste groep

Let op! Onder de fid kolom moet de kolom dat de id van de hexagoon bevat worden gezet

Let op! Als er geen bestandslocatie is gekozen wordt een tijdelijke laag gemaakt van de uitkomsten. Als deze niet opgeslagen worden zullen ze bij het sluiten van het project verloren gaan.

# Bijlage 1: Installeren IMAER en ImaerAutoCalc plug-in
1.	Open het beheerscherm van de plug-ins

Installeer IMAER plug-in
1.	Zoek naar ‘IMAER...’
2.	Klik op plug-in installeren
3.  Klik op het sleuteltje om een api aan te vragen
4.	Vul de gegevens in en druk op opslaan

Installeer ImaerAutoCalc plug-in
1.	Open het beheerscherm van de plug-ins
2.	Klik op instaleren vanuit ZIP
3.	Zoek naar de locatie van het ZIP-bestand van de plug-in
4.	Druk op Openen 
5.	Installeer de plug-in
6.	Zorg dat IMAER plug-in en ImaerAutoCalc aan staan



