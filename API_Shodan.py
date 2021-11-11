import shodan

def search(buscar):
    api=input("API key: ")
    s = shodan.Shodan(api)
    try:
        # Search Shodan
        results = s.search(buscar)
        # Show the results
        print('Results: %s' % results['total'])

        for i in results['matches']:
                print('IP: %s' % i['ip'])
                print('Port: %s' % i['port'])
                print('Hostnames: %s' % i['hostnames'])
                print('-----------'*5)


    except Exception as e:
        print('Ups! Ha ocurrido un error: %s' % e)
