import requests
import re
from bs4 import BeautifulSoup

def is_catagory(href):
    return href and re.compile('categories-by-alphabet').search(href)

def is_sublink(id_val):
    return re.compile('ContentPlaceHolder1_dlkeyword_detail_hplink_keyword_[0-9]+').search(id_val)

def is_cmpnylink(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_hlcampanyname_[0-9]+').search(id_val)

def is_addr(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblAddress1_([0-9]+)').search(id_val)

def is_area(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblarea_([0-9]+)').search(id_val)

def is_country(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblAddress5_Emirates_([0-9]+)').search(id_val)

def is_landmark(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblLandmark_([0-9]+)').search(id_val) 

def is_pobox(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblPoBox1_Number_([0-9]+)').search(id_val) 

def is_countrycode(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblTel1_CntryCode_([0-9]+)').search(id_val)

def is_areacode(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblTel2_AreaCode_([0-9]+)').search(id_val)

def is_telnbr(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblTel3_ListingTel_([0-9]+)').search(id_val)

def is_faxnbr(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_lblFax3_FaxNumber_([0-9]+)').search(id_val)

def is_mblnbr(id_val):
    return re.compile('ContentPlaceHolder1_grdListing_dlothercontact_0_lblcontactinfo_([0-9]+)').search(id_val)


r = requests.get("https://www.yellowpages.ae/")
soup = BeautifulSoup(r.content, 'html.parser')

# For all links in yellowpages.ae
for alp_link in soup.find_all("a"):
    if (is_catagory(href=alp_link.get('href'))):
        print("----------------------------------")
        print(alp_link.text, alp_link.get('href'))
        r1 = requests.get(alp_link.get('href'))
        s1 = BeautifulSoup(r1.content, 'html.parser')

        # For each a.html, b.html etc in the catagory division
        for each_alp in s1.find_all("a"):
            if (is_sublink(id_val=str(each_alp.get('id')))):
                print("*******************************")
                print(each_alp.text, each_alp.get('href'))
                r2 = requests.get(each_alp.get('href'))
                s2 = BeautifulSoup(r2.content, 'html.parser')
                    
                # For each links starts with the corresponding alphabet
                listoflist = []
                sublist = []
                for s in s2.find_all('span'):
                    id_val = str(s.get('id'))
                    m = is_addr(id_val)
                    if m:
                        # extract the nbr alone and use this as key
                        if sublist:
                            listoflist.append(sublist)
                            #print("sublist : ", sublist)
                        sublist = []
                        sublist.append("Street: " + s.text)
                    if(is_area(id_val)):
                        sublist.append("Area: " + s.text)
                    if(is_country(id_val)):
                        sublist.append("Country: " + s.text)
                    if(is_landmark(id_val)):
                        sublist.append("Landmark: " + s.text)
                    if(is_pobox(id_val)):
                        sublist.append("POBox Nbr: " + s.text)
                    if(is_countrycode(id_val)):
                        sublist.append("Country code: " + s.text)
                    if(is_areacode(id_val)):
                        sublist.append("Area code: " + s.text)
                    if(is_telnbr(id_val)):
                        sublist.append("Tel Nbr: " + s.text)
                    if(is_faxnbr(id_val)):
                        sublist.append("Fax Nbr: " + s.text)
                    if(is_mblnbr(id_val)):
                        sublist.append("Mobile Nbr: " + s.text)
                if sublist:
                    listoflist.append(sublist)

                idx = 0
                for cmpnys in s2.find_all('h2'):
                    if (is_cmpnylink(id_val=str(cmpnys.a.get('id')))):
                        print("#################")
                        print("Company: ", cmpnys.a.text)
                        for dtl in listoflist[idx]:
                            print(dtl)
                        idx = idx + 1
