import subprocess
import re


def get_whois_data(domain):
	command = subprocess.Popen(['whois', domain], stdout=subprocess.PIPE)
	whois_info = command.communicate()[0].decode('utf-8')
	info = whois_info.split('\n')[:-1]
	clean_info = []

	for string in info:
		clean = re.sub(' +', ' ', string)
		clean_info.append(clean)

	essence_info = []
	for el in clean_info:
		if re.match(r'state:', el) \
		or re.match(r'registrar:', el) \
		or re.match(r'created:', el) \
		or re.match(r'paid-till:', el) \
		or re.match(r'free-date:', el) \
		or re.match(r'Last updated on', el)\
		or re.match(r'Domain Status:', el)\
		or re.match(r'Registrar:', el)\
		or re.match(r'Registrar URL:', el)\
		or re.match(r'Updated Date', el)\
		or re.match(r'Creation Date:', el)\
		or re.match(r'Registrar Registration Expiration Date:', el):
			essence_info.append(el)
	return essence_info

data = get_whois_data('tang0.ru')
