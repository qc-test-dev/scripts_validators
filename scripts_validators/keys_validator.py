#!/usr/local/bin/python3
# install using pip3=> requests,re,assertpy,xlrd,pytest
#url sessionKey=d48c48c956cda082e2e03b717c81c220-mexico directo a translations-json

import requests
import json
import re
from assertpy import assert_that, soft_assertions
import xlrd
import pytest

class WebGetTranslations:

	def __init__(self):
		self.pais_input=input("ingresa pais: ").lower()
		self.device=input("ingresa dispositivo: ").lower()
		self.dict={}
		self.uri=""

	def case_uri(self):
		regex=re.compile('[a-zA-Z0-9]*')
		devices=['stb','ios','adr','stv','web','roku']
		if self.device == ("stv"):
			self.uri="http://aaf-cvideo-tv.clarovideo.net/webapi-video/metadata?HKS=0trtcgcrnvs14tn77jdalm4dg3&api_version=v5.93&authpn=amco&authpt=12e4i8l6a581a&device_type=TV&format=json&region={pais}&sessionKey=2a6ec299f2f6ea0a821f00ded282f77a-{pais}".format(pais=self.pais_input)
		if self.device == ("ios"):
			self.uri="https://mfwktabletios-api.clarovideo.net/services/apa/metadata?user_id=21696669&format=json&authpt=12e4i8l6a581a&HKS=0B7C28FE4EDA402DB8C153CF96EA96366109c692cc7c4&sessionKey=542d4967e4b033898a8e7277-{pais}&region={pais}&authpn=amco&device_model=aapl&api_version=v5.93".format(pais=self.pais_input)
		if self.device == ("adr"):
			self.uri="http://mfwkmobileandroid-api.clarovideo.net/services/apa/metadata?authpt=12e4i8l6a581a&HKS=thomues9gmnbi91tfttgffjf20&device_model=android&sessionKey=5281f871e4b07f987f4cb32e-{pais}&format=json&authpn=amco&api_version=v5.93&region={pais}&device_category=mobile".format(pais=self.pais_input)
		if self.device == ("roku"):
			self.uri="https://mfwkstbroku-api.clarovideo.net/services/apa/metadata?user_id=21696669&format=json&authpt=12e4i8l6a581a&HKS=0B7C28FE4EDA402DB8C153CF96EA96366109c692cc7c4&sessionKey=542d4967e4b033898a8e7277-{pais}&region={pais}&authpn=amco&device_model=aapl&api_version=v5.93".format(pais=self.pais_input)
		if self.device ==  ("web"):
			self.uri="https://mfwkweb-api.clarovideo.net/services/apa/metadata?device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.93&region={pais}&HKS=r257tnjj3hrqlcpjel0titp4i5&sessionKey=d48c48c956cda082e2e03b717c81c220-{pais}".format(pais=self.pais_input)
		if self.device ==  ("stb"):
			self.uri="https://mfwkweb-api.clarovideo.net/services/apa/metadata?device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.93&region={pais}&HKS=r257tnjj3hrqlcpjel0titp4i5&sessionKey=d48c48c956cda082e2e03b717c81c220-{pais}".format(pais=self.pais_input)
		if self.device not in devices:
			
			print("Dispositivo no valido,ingrese (stv,ios,adr,roku,web,stb)")
			return WebGetTranslations.main()
		return self.uri	
	#hacer request a la URL
	def get_request(self):
		try:
			requested_uri=(requests.get(self.uri))
			self.response=requested_uri.json()['translations']
			self.response_dict=json.loads(self.response)
			return self.response_dict
		except requests.ConnectionError:
			print("ERROR EN SOLICITUD, VERIFICAR LA URL  " + str(requests.ConnectionError))
			exit()
		except requests.Timeout:
			print("ERROR DE TIMEOUT  " + str(requests.Timeout))
			exit()
		except requests.RequestException:
			print("ERROR EN API, VALIDAR CON ADMIN DE API  " + str(requests.RequestException))	
			exit()
		
    
	#limpiar html de la respuesta
	def clean_html_response(self):
		clean = re.compile('<.*?>')
		self.string_processed = re.sub(clean, " ", self.string_from_response)

	#validar usando un keyvalue especifico
	def get_text_by_key(self):
		self.keyValue=input("keyValue: ").strip()
		if not self.keyValue :
			print("ingrese un valor")
			WebGetTranslations.get_text_by_key(self)
		elif  self.keyValue :
			if self.keyValue == "exit":
				exit()
			else:
				try:
					self.string_from_response=self.response_dict['language'][self.pais_input][self.keyValue]
					WebGetTranslations.clean_html_response(self)
					print(self.string_processed)
				except KeyError:
					print("No se encontro la llave => " + self.keyValue)
					WebGetTranslations.get_text_by_key(self)
				except NameError:
					print("Alguno de los datos proporcionados es invalido, verificarlo")
					exit()
				except TypeError :
					print("Alguno de los datos proporcionados es invalido, verificarlo")
					exit()		
		else:
			WebGetTranslations.get_text_by_key(self)


	#validar list comprehension
	#obtener todos los keyvalues, la respuesta tiene 3 niveles con diccionarios cada uno
	def get_all_keyvalues(self):		
		for k,v in self.response_dict.items():
			if isinstance(v,dict):
				for nk,nv in v.items():
					if type(nv) is dict:
						for nk2,nv2 in nv.items():
							if nk2 not in self.dict:
								self.dict.update({nk2:nv2})


	#obtener todos los keyvalues, la respuesta tiene 3 niveles con diccionarios cada uno
	def print_all_keyvalues(self):	
		WebGetTranslations.get_all_keyvalues(self)
		for k,v in self.dict.items():
			print(k)



	#obtener todos los keyvalues con texto actual del API
	def print_all_keys_and_Values(self):
		WebGetTranslations.get_all_keyvalues(self)
		for k,v in self.dict.items():
			print(k + ' => ' +v)


		
	#obtener todos los keyvalues con texto actual del API, sin valores vacios
	def print_all_keys_and_Values_not_empty(self):
		WebGetTranslations.get_all_keyvalues(self)
		for k,v in self.dict.items():
			if len(v) > 1:
				print(k + ' => ' +v)


	#verificar si texto es igual que valor de clave
	def verify_if_value_equal_string(self):
		WebGetTranslations.get_text_by_key(self)
		self.string_toverify_equals=input("ingrese texto para validar: ")
		try:
			assert_that(self.string_processed).is_equal_to(self.string_toverify_equals)
			print("TEXTO INGRESADO ES EL MISMO QUE TEXTO EN LLAVE")
		except AssertionError:
			print(self.string_toverify_equals + ' != ' + self.string_processed)
			print("TEXTOS DIFERENTES  ")


	#verificar si texto es contenido en valor de clave
	def verify_if_value_contains_string(self):
		WebGetTranslations.get_text_by_key(self)
		self.string_toverify_contains=input("ingrese texto para validar: ")
		try:
			assert_that(self.string_processed).contains(self.string_toverify_contains)
			print(self.string_toverify_contains + " <= ESTA CONTENIDO EN TEXTO DE LA LLAVE")
		except AssertionError:
			print("TEXTOS NO INCLUIDO EN VALOR DE LA LLAVE")
			print(self.string_toverify + ' != ' + self.string_processed)




	#verificar si valor de clave es igual que valor en excel
	def verify_if_value_is_equal_to_xls(self):
		WebGetTranslations.get_text_by_key(self)
		path="/Users/at/Desktop/Book1.xls"
		wb = xlrd.open_workbook(path)
		sheet = wb.sheet_by_index(0)
		text_excel=sheet.cell_value(0,0)
		assert_that(self.string_processed).is_equal_to(text_excel)
		if   AssertionError:
			print(' != ' + text_excel)
		else:	
			print(' es igual que => '+ text_excel)


	#main function
	def main():
		get_translation = WebGetTranslations()
		get_translation.case_uri()
		get_translation.get_request()
		#get_translation.clean_html_response()
		get_translation.get_text_by_key()
		#get_translation.get_all_keyvalues()
		#get_translation.print_all_keyvalues()
		#get_translation.print_all_keys_and_Values()
		#get_translation.print_all_keys_and_Values_not_empty()
		#get_translation.verify_if_value_equal_string()
		#get_translation.verify_if_value_contains_string()
		#get_translation.verify_if_value_is_equal_to_xls()
		get_translation.continue_ask()

	#ask to continue
	def continue_ask(self):
		ask_continue_input=input("continuar? Y/N ").lower()
		if str(ask_continue_input) == 'y':
			WebGetTranslations.main()
		else:
			exit()

if __name__ == '__main__':
	while True:
		WebGetTranslations.main()

