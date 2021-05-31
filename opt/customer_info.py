import subprocess
import re


def get_customer_data(domain):
	command = subprocess.Popen(['ssh', 'ruslanakmanov@support-console.beget', '"yii"', '"domain/check"', '"%s"' %(domain)], stdout=subprocess.PIPE)
	domain_info = command.communicate()[0].decode('utf-8')
	info = domain_info.split('\n')[:-1]
	clean_info = []

	for string in info:
		clean_spaces = re.sub(' +', ' ', string)
		clean_tab = re.sub('\t', ' ', clean_spaces)
		clean_info.append(clean_tab)

	essence_info = []
	for info in clean_info:
		if re.match(r'Server:', info) \
		or re.match(r'Customer:', info):
			essence_info.append(info)
	return essence_info

# For check
# print(get_whois_data('tang0.ru'))