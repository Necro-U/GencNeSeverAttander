from dataclasses import dataclass


@dataclass
class SiteGlobals():
    MAIN_PAGE_LINK="https://gencnesever.com/" 
    POST_LINK = "https://gencnesever.com/ajax/CekilisBasvuru.php"

    SANATSECTION_CLASS = "section-sanatsever-liste"
    SPORSECTION_CLASS= "section-sporsever-liste"
    SEYEHATSECTION_CLASS = "section-seyehat-liste"
    KITAPSECTION_CLASS = "section-kitap-liste"
    IYILIKSECTION_CLASS = "section-iyilik-liste"

    # her kısmın isimler değişiyor.
    CARDDIV_CLASS= "box"
    CARD_GENERAL_INFO_DIV = "ust-kisim gencspor-renk"
    CARD_LASTDAY_P="cekilis-tarihi gencspor-sever-renk-yazi"
    CARD_INFO_DIV="sag-aciklama"

    # Header attributes
    HEADER = {
        "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    }

    # Post attributes 
    PAYLOAD = {
        "adiniz":"",
        "soyadiniz":"",
        "tcno":"",
        "dogumyili":"",
        "bulundugu_sehir":"",
        "emailadresi":"",
        "telefonno":"",
        "g-recaptcha-response":"",
        "kabulet":"1",
        "csrf-token":"",
        "deg1":"25",
        "deg2":"18",
        "deg3":"375"
    }