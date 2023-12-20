# Ecommerce
 Ecomerce Shop Demo - Django, Django Rest Framework

## MVC Endpoints
/ - app root

/home - app homepage

/products - katalog produktů

/about - stránka o nás

/contact - kontaktní stránka, včetně emailového formuláře

/cart - nákupní koš

/search - výsledky vyhledávání

/login - přihlášení uživatele

/logout - odhlášení uživatele

/user - stránka s profilem přihlášeného uživatele

/user/register - registrace nového uživatele

/admin - administrace

# RestApi Endpoint
/api/products - katalog produktů (GET)

# Povolené metody RestAPI
- GET

# Rozhraní aplikace
- MVC, AJAX - WebUI interface
- RestAPI - API interface

# Autentizace a Autorizace
- WebUI: registrace uživatele, profil uživatele. Pro vytvoření objednávky musí být uživatel přihlášen.
- RestAPI: Neimplementováno. Omezeno pouze pro čtení metodou GET.

# Email rozhraní
- aplikace používá k automatickému zasílání potvrzovacích emailových zpráv:

- účet na Gmail.com
- SSL zabezpečení
- odesílá potvrzení objednávky
- odesílá kontaktní emailový formulář

# Nákupní košík
- v session se ukládá pouze id produktu a množství nakupované položky
- všechny výpočty jsou prováděny pouze na straně serveru. Uživatel k těmto hodnotám nemá přístup.
- změny v nákupním košíku jsou prováděny pouze na straně serveru a ukládány v objektu Cart. Změny jsou zasílány na server pomocí AJAX metody POST, následně provedena změna v objektu Cart a odpověď je aktualizována na stránce ihned pomocí Javascriptu.
- persistence obsahu košíku je zajištěna po celou dobu platnosti konkrétní session. Ceny jsou aktualizovány vždy podle platné ceny ze strany serveru.

# Katalog produktů
- katalog je zpracován pomocí Bootstrap karet
- každý produkt má také svojí detailní stránku
- katalog produktů lze stránkovat pomocí parametrů implementovaného paginátoru
- Bootstrap modals jsou využívány k potvrzení zásadních kroků uživatele, např. smazání celého košíku

# Nákupní proces
- uživatel si vybere zboží na hlavní stránce, v katalogu produktů nebo může použít vyhledávání (název produktu)
- každé přidání do košíku je také notifikováno změnou čísla v notifikaci nad tlačítkem košík (AJAX)
- v nákupním košíku může změnit množství každé jednotlivé položky
- v nákupním košíku může odstranit každou z nakupovaných položek
- může kompletně vysypat nákupní košík
- každá změna množství v košíku má ihned vliv na položkovou cenu zboží, celkovou cenu nákupu a množství položek v košíku
- tyto změny jsou ihned ukládány do objektu Cart na straně serveru, případně také session 

# Možnosti rozšíření
- RestAPI - kompletní RestAPI pro využití frontendu (React, Angular, Vue) a mobilních aplikací
- zabezpečení RestAPI prostřednictvím JWT
- autentifikace a autorizace prostřednictvím třetích stran (OAuth2, Bankovní identita)
- dvoufázové ověření přihlášení
- profesionální HTML šablona

# Admin
- /admin
- pro testovací účely je k dispozici účet: admin/admin
- lze administrovat uživatele eshopu
- lze administrovat produkty eshopu
- lze administrovat objednávky a jednotlivé položky objednávky
- u objednávek lze měnit stav dle vytvořeného ENUM: Přijato, Zaplaceno, Odesláno, Fakturováno
- je ukládána kopie odeslaných zpráv prostřednictvím emailového formuláře (/contact)

# Tech Stack
Django 5.0

Django Rest Framework 3.14.0

Pillow 10.1.0

SQLite 3

Bootstrap 5.3