import subprocess
import re


def get_server_ip(domain):
	command = subprocess.Popen(['ssh', 'ruslanakmanov@support-console.beget', '"yii"', '"info"', '"%s"' %(domain)], stdout=subprocess.PIPE)
	ip_info = command.communicate()[0].decode('utf-8')
	duty_ips = re.search(r"\w+ \| ([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}) \| ([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}) \| ([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})", ip_info)

	try:
		ips = duty_ips.group(0).split('|')
	except AttributeError as err:
		return ['Not our', 'Not our']

	apache_nginx = []
	apache_nginx.append(ips[1])
	apache_nginx.append(ips[2])

	return apache_nginx

	
# For check
# print(get_customer_data('tang0.ru'))



