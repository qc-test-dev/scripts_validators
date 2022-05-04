#!/usr/local/bin/python3
#coding: utf-8

import requests
requests.packages.urllib3.disable_warnings()
import urllib3
import json
import hashlib
import sys
import os
import string
import re


#import warning



class Data_Verifier:
	def __init__(self):
		self.response_dict={}
		self.response_results={}
		self.serial=sys.argv[1]
		self.pais=sys.argv[2]
		print(self.serial,self.pais)


	def login(self):
		search_in_results=['username','user_id','subscriptions','email','paymentMethods','session_stringvalue','user_token']
		response_results=['username','user_id','subscriptions','email','paymentMethods','session_stringvalue']
		silo_device="mfwkweb-api.clarovideo.net"
		login_uri="http://{silo_device}/services/user/authdevice?HKS=d4hu5fc8m1oj0mjlt99d741714&api_version=v5.91&authpn=amco&authpt=12e4i8l6a581a&device_category=stb&device_id={serial}&device_manufacturer=kaonmedia&device_model=sc7210&device_name=Hi3798MV100&device_so=Android%204.4.2&device_type=ott&format=json&region={pais}&serial_id={serial}&serial_id={serial}".format(silo_device=silo_device,serial=self.serial,pais=self.pais)
		try:
			login_request=(requests.get(login_uri))
			response=login_request.json()['response']

		except requests.ConnectionError:
			print("ERROR EN SOLICITUD, VERIFICAR LA URL  " + str(requests.ConnectionError))
			exit()
		
		for k,v in response.items():
			if k in search_in_results:
				self.response_dict.update({k:v})
		
		for k,v in response.items():
			if k in response_results:
				self.response_results.update({k:v})


		self.user_id=self.response_dict['user_id']
		self.hks=self.response_dict['session_stringvalue']
		self.user_token=self.response_dict['user_token']
		#print(self.hks)
		for key,element in self.response_results.items():
			print(key,'=>' , element)
		#print(self.response_results)
		#print(self.response_dict)
		return self.response_dict

	def islogin(self):
		islogin_uri='http://mfwkweb-api.clarovideo.net/services/user/isloggedin?device_id=web&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.93&region=mexico&HKS={hks}&user_id={user_id}&includpaywayprofile=1'.format(user_id=self.user_id,hks=self.hks)
		try:
			login_request=(requests.get(islogin_uri))
			response=login_request.json()['response']
			#print(response['response'])
		except requests.ConnectionError:
			print("ERROR EN SOLICITUD, VERIFICAR LA URL  " + str(requests.ConnectionError))
			exit()
		return print('Usuario puede hacer login') if (response['is_user_logged_in']) == 1 else print('usuario no puede hacer login')

	def paquetes(self):
		
		paq_uri='http://mfwktv2sony-api.clarovideo.net/services/payway/linealchannels?HKS={hks}&device_category=generic&device_manufacturer=generic&device_model=generic&device_type=generic&api_version=v5.93&region={pais}&user_id={user_id}&authpn=webclient&authpt=tfg1h3j4k6fd7'.format(user_id=self.user_id,pais=self.pais,hks=self.hks)
		try:
			paq_request=(requests.get(paq_uri))
			response=paq_request.json()['response']
			print(str(response))
		except requests.ConnectionError:
			print("ERROR EN SOLICITUD, VERIFICAR LA URL  " + str(requests.ConnectionError))
			exit()
		

	def get_pin_parental(self):
		controlPin_uri='https://mfwkweb-api.clarovideo.net/services/user/controlpin/get?api_version=v5.93&authpn=webclient&authpt=tfg1h3j4k6fd7&device_category=web&device_model=web&device_type=chrome&device_manufacturer=sc-270&region=mexico&HKS=web623926893a95c&user_id=49987507&user_token={user_token}'.format(user_token=self.user_token)
		#os.system("networksetup "+"-connectpppoeservice "+"uat-mx")
		#time.sleep(15)
		try:
			pin_post_request=(requests.post(controlPin_uri))
			self.hashed_pin=pin_post_request.json()['response']['hashed_code']
		except requests.ConnectionError:
			print("ERROR EN SOLICITUD, VERIFICAR LA URL  " + str(requests.ConnectionError))
			exit()
		
		print("consulta el pin aqui=>  https://hashtoolkit.com/decrypt-hash/?hash="+self.hashed_pin)
		#return os.system("networksetup "+"-disconnectpppoeservice "+"uat-mx")

	def decode_pin(self):
		numbers=[str(x) for x in range(0,999999)]
		for number in numbers:
			number=number.strip()
			hashed_number=hashlib.sha1(number.encode('utf-8')).hexdigest()
			if hashed_number == self.hashed_pin:
				print("el pin es " + number)
		





	
data_verifier=Data_Verifier()
data_verifier.login()
data_verifier.islogin()
data_verifier.get_pin_parental()
data_verifier.paquetes()
#data_verifier.decode_pin()