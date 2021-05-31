from django.shortcuts import render
from django.views.generic import TemplateView
import subprocess
import ipinfo
import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from mainapp.opt.ssl_check import get_certificate, get_issuer
from mainapp.opt.whois_parse import get_whois_data
from mainapp.opt.customer_info import get_customer_data
from mainapp.opt.server_info import get_server_ip


class Index(TemplateView):
    template_name = 'index.html'
    title = 'Hello'
    def index(request):
        return render(request, 'mainapp/index.html') 


def domain_info(request, domain='Not'):

    access_token = "a445e03d977a3d"
    handler = ipinfo.getHandler(access_token) #Получаем токен для ipinfo.io, информация об IP
    domain = request.GET.get('q')
    command = subprocess.Popen(['dig', domain, '+short'], stdout=subprocess.PIPE)
    ip = command.communicate()[0].decode('utf-8')
    ipadreses = ip.split('\n')[:-1]
    command = subprocess.Popen(['dig', 'www.'+ domain, '+short'], stdout=subprocess.PIPE)
    www_ip = command.communicate()[0].decode('utf-8')
    ipadreses = ip.split('\n')[:-1]
    command = subprocess.Popen(['dig', domain, 'NS', '+short'], stdout=subprocess.PIPE)
    ns = command.communicate()[0].decode('utf-8')
    name_servers = ns.split('\n')[:-1]
    command = subprocess.Popen(['dig', domain, 'MX', '+short'], stdout=subprocess.PIPE)
    ns = command.communicate()[0].decode('utf-8')
    mx_servers = ns.split('\n')[:-1]
    organisations = []
    for ip in ipadreses: # Получаем информацию об IP через API ipinfo.io
        details = handler.getDetails(ip)
        try:
            organisations.append(details.org)
        except AttributeError as err:
            organisations.append('oops... not found')

    answer_code = requests.get('http://' + domain) # Проверка протокола и коды ответа.
    if answer_code.history != []:
        redirect = 'Yes'
    else:
        redirect = 'No'
    protocol = answer_code.url.split(':')[0].upper()
    actual_url = answer_code.url # URL по которому открывается сайт, после всех редиректов, если они были.

    #[Server IP section START]
    server_ip = get_server_ip(domain)
    #[Server IP section END]

    #[SCRISNHOT section start] делаем скриншот сайта с помощью браузера и selenium
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'opt/chromedriver')
    driver.get('http://' + domain)
    sleep(1)
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backendPerformance_calc = responseStart - navigationStart
    frontendPerformance_calc = domComplete - responseStart
    driver.get_screenshot_as_file("static/img/screenshots/screenshot.png")
    driver.quit()
    #[SCRISNHOT section END]

    #[SSL Certificate section START]
    notbefore = 'None'
    notafter = 'None'
    issuer_by = 'None'
    try:
        hostinfo = get_certificate(domain, 443)
        notbefore = hostinfo.cert.not_valid_before
        notafter = hostinfo.cert.not_valid_after
        issuer_by = get_issuer(hostinfo.cert)
    except Exception as err:
        print(err)
        pass

    #[SSL Certificate section END]

    #[WHOIS section START]
    whois_data = get_whois_data(domain)
    print(whois_data)
    if whois_data != [] and len(whois_data) > 5:
        state = whois_data[0]
        registrar = whois_data[1]
        created = whois_data[2]
        paid_till = whois_data[3]
        free_date = whois_data[4]
        last_update = whois_data[5]
    else:
        state = 'None'
        registrar = 'None'
        created = 'None'
        paid_till = 'None'
        free_date = 'None'
        last_update = 'None'
    #[WHOIS section END]

    #[Get customer data START]
    customer_data = get_customer_data(domain)
    #[Get custome data END]



    context = {'domain': domain}
    try:
        context['server'] = customer_data[0]
    except IndexError as err:
        context['server'] = 'Не наш сервер'
    context['ipadreses'] = ipadreses
    context['nginx_ip'] = server_ip[0]
    context['ssl_ip'] = server_ip[1]

    context['organisations'] = organisations[0]
    context['answer_code'] = answer_code
    context['name_servers'] = name_servers
    context['mx_servers'] = mx_servers
    context['www_ip'] = www_ip
    context['back_end'] = backendPerformance_calc
    context['fron_end'] = frontendPerformance_calc
    context['all_time'] = backendPerformance_calc + frontendPerformance_calc
    context['redirect'] = redirect
    context['protocol'] = protocol
    context['notbefore'] = notbefore
    context['notafter'] = notafter
    context['issuer_by'] = issuer_by
    context['state'] = state
    context['registrar'] = registrar
    context['created'] = created
    context['paid_till'] = paid_till
    context['free_date'] = free_date
    context['last_update'] = last_update
    context['customer_data'] = customer_data
    if customer_data == []:
        context['customer_data'] = ['В Beget нет этого домена']



    return render(request, 'mainapp/domain_info.html', context)