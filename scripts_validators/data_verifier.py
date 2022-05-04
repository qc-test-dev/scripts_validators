#!/usr/local/bin/python3
#coding: utf-8

import requests
import json
import hashlib
import sys
import os
import time

class Data_Verifier:
	def __init__(self):
		self.response_dict={}
		self.response_results={}
		self.username=sys.argv[1]
		self.password=sys.argv[2]
		print(self.password,self.username)

	def user_separator(self):
		user_credentials={}
		for user,password in user_credentials.items():
			pass

	def login(self):
		search_in_results=['name','user_id','subscriptions','email','paymentMethods','session_stringvalue','user_token']
		response_results=['name','user_id','subscriptions','email','paymentMethods','session_stringvalue']
		silo_device="mfwkweb-api.clarovideo.net"
		login_uri="http://{silo_device}/services/user/login?device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.93&region=guatemala&HKS=sfdgfgnfgdfbfdnzgfhs&includpaywayprofile=true&username={username}&password={password}".format(silo_device=silo_device,username=self.username,password=self.password)
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
			#print(response)
		except requests.ConnectionError:
			print("ERROR EN SOLICITUD, VERIFICAR LA URL  " + str(requests.ConnectionError))
			exit()
		return print('Usuario puede hacer login') if (response['is_user_logged_in']) == 1 else print('usuario no puede hacer login')


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
data_verifier.decode_pin()