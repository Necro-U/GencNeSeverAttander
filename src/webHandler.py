import requests 
from requests.utils import dict_from_cookiejar
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from src.Globals.Globals import SiteGlobals
from pypasser import reCaptchaV3,reCaptchaV2
from selenium.webdriver.common.by import By

class WebHandler:
    def __init__(self) -> None:
        self.cekilis_links:list[str]=[]
        self.post_dict = SiteGlobals.PAYLOAD
        self.header = SiteGlobals.HEADER
        self.driver = webdriver.Chrome()

    def __info_formatter(self,info:str,day:str,link:str):
        name = info.text.split("\n")
        cekilis_aded = name[4].strip()
        name = name[2].strip()
        day = day.strip()
        if link != None:
            link = SiteGlobals.MAIN_PAGE_LINK + link
        else:
            print("Be carefull! link might is empty!")
        return (name,cekilis_aded,day,link)

    def draw_finder(self,session:requests.Session):
        respone = session.get(SiteGlobals.MAIN_PAGE_LINK)
        cookies = dict_from_cookiejar(respone.cookies)
        # TODO: need to be added an list to search all different sections
        main_page = BeautifulSoup(respone.content,'html.parser')
        div = main_page.find("section",attrs={"class":SiteGlobals.SPORSECTION_CLASS})


        cards = div.find_all("div",attrs={"class":SiteGlobals.CARDDIV_CLASS})
        # print(div)
        for card in cards: 
            info_section =card.find("div",attrs={"class":SiteGlobals.CARD_GENERAL_INFO_DIV})
            info = info_section.find("div",attrs={"class":SiteGlobals.CARD_INFO_DIV})
            last_day = card.find("p",attrs={"class":SiteGlobals.CARD_LASTDAY_P})
            atag = card.find("a")["href"]
            
            name,ticket_num,last_day,atag = self.__info_formatter(info,last_day.text,atag)

            print(name,"çekilişinin bilet adedi:",ticket_num,"\nGeçerli olduğu son tarih:",last_day,"\link = ",atag,"\n")

    def __selenium_starter(self):

        self.driver.get("https://gencnesever.com/sporsever/decathlon-200tl-hediye-ceki-374")
        sleep(1)
        elem = self.driver.find_element(By.XPATH,"//iframe[@title='reCAPTCHA']")
        src= elem.get_attribute("src")
        sleep(16)
        print(src)
        return src



    def __recap(self,anchor):
        # Buraya başvuru linkleri gelecek ! 
        anchor = self.__selenium_starter()
        # self.driver.get("https://gencnesever.com/sporsever/decathlon-200tl-hediye-ceki-374")
        rec = reCaptchaV3(anchor)
        return rec
    
    def __find_necessities(self,session:requests.Session,link)->tuple[str,str,str]:
        # returns csrf-token, recaptcha and page's html text
        response = session.get(link)
        page = BeautifulSoup(response.content,'html.parser')
        inp = page.find("input",attrs={"name":"csrf-token"})
        anchor = page.find("iframe",attrs={"name":"a-tvlnlpukynep"})
        print("crsf token has been taken.")

        recapctha = self.__recap(anchor)
        print("recaptcha has been taken.")

        print("all necesseties has been taken.")
        return (inp["value"],page,recapctha)
    
    def __fill_form_dict(self,session:requests.Session,link):
        csrf,page,recaptcha = self.__find_necessities(session,link)
        
        # Burda input alınacak ve girilen inputlar yerleştirilecektir. kontrolcü = self.control_post
        self.post_dict["adiniz"] = "Ubeydullah"
        self.post_dict["soyadiniz"] = "Önder"
        self.post_dict["tcno"]= "20140184156"
        self.post_dict["dogumyili"] = "2000"
        self.post_dict["bulundugu_sehir"] = "İstanbul"
        self.post_dict["emailadresi"] = "ubeyd02@outlook.com"
        self.post_dict["telefonno"] = "05522322202"
        self.post_dict["g-recaptcha-response"] = recaptcha
        self.post_dict["csrf-token"] = csrf
        if not self.__control_post():
            print("Post form has some empty or invalid values!")
            return (False,page)
        return (True,page)


    def __control_post(self)-> bool:
        for key in self.post_dict.keys():
            if self.post_dict[key] == "":
                print(key)
                return False
            if key == "dogumyili" or key =="telefonno" or key =="tcno":
                if not self.__control_integer(self.post_dict[key]):
                    print(key)
                    return False
        return True

    def __control_integer(self,value:str):
        return value.isnumeric()
    
    def send_form(self,session:requests.Session,link):
        filled,page = self.__fill_form_dict(session,link)
        if filled:
            session.headers.update({
                "referer":"https://gencnesever.com/sporsever/arabam-com-konyaspor-yukatel-kayserispor-spor-toto-super-lig-maci-381",
                "origin":"https://gencnesever.com"
                })
            response = session.post(SiteGlobals.POST_LINK,data=self.post_dict,headers=self.header)
            page = BeautifulSoup(response.text,'html.parser')
            hata = page.find("div",attrs={"id":"basvurusonuc"})
            # if hata:
            with open("response.html","+w") as file:
                file.write(response.text)
            print(response.url,hata)



    def main(self):
        with requests.Session() as session:
            self.draw_finder(session)
            self.send_form(session,"https://gencnesever.com/sporsever/decathlon-200tl-hediye-ceki-374")
