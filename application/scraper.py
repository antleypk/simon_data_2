import requests, json, csv, os, time, config

def get_shops(pv_count, pv_listing_count, key):
    #get shops returns a configureable amount of stores, pv_count
    #the stores must have at least as many listings as pv_listing_count
    #the api shared key must be passed to complete transaction
    pprint("--get shops, pv_count: {}, pv_listing_count {}".format(pv_count, pv_listing_count))
    state = True
    limit = 50
    offset = 0
    increment = 50
    count = 0
    stores = []
    store_ids = set()
    while(state):
        url = "https://openapi.etsy.com/v2/shops?limit={}&offset={}&api_key={}".format(limit, offset, key)
        headers = {'user-agent': 'my-app/0.0.1'}
        r = requests.get(url, headers=headers)
        pprint('---- API response code: {}, Limit: {}, Offset: {}'.format(r, limit, offset))
        content = r.content
        d_content = content.decode("utf-8")
        content_json = json.loads(d_content)
        for r in content_json['results']:
            if r['listing_active_count'] > pv_listing_count:
                lcl_id = r['shop_id']
                if not lcl_id in store_ids:
                    count+=1
                    store_ids.add(lcl_id) 
                    pprint("Shop ID: {}, Shop Name: {}, Active Listings: {}, Count: {}".format(r['shop_id'], r['shop_name'], r['listing_active_count'], count))
                    stores.append(r)
            if len(stores) == pv_count:
                state = False
                break
        limit+=increment
        offset+=increment
        pprint(' ')
    pprint(' ')
    return stores    


def save(shops, path):
    #saves the list of shops to the passed path
    pprint("--save")
    s_t = '{}'.format(time.time())
    time_split = s_t.split('.')
    e = time_split[0]
    lcl_path = path+'_{}.csv'.format(e)
    if not os.path.isfile(lcl_path):
        pprint('make {}'.format(lcl_path))
        with open(lcl_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        "id"
                        ,"shop_id"
                        ,"shop_name"
                        ,"listing_count"
                        ,"e_time"
                    ]
                )
                lcl_id = 1
                for shop in shops:
                    lcl_list = [lcl_id, shop['shop_id'], shop['shop_name'], shop['listing_active_count'], str(time.time())]     
                    writer.writerow(lcl_list)
                    lcl_id+=1

def pprint(string):
    #prints and logs print statements
    print(string)
    if not os.path.isdir("./data"):
        os.makedirs("./data")
    if not os.path.isfile("./data/logs.csv"):
        os.system("touch ./data/logs.csv")
    with open("./data/logs.csv","a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(time.time()),'    ', string])

def get_key():
    #gets key from .gitignored file
    print('--get key')
    with open("./secret.key") as f:
        key = f.readline()
        return key

def main():
    pprint("--main 'scraper.py'")
    shop_count = config.shop_count
    min_active_listing = config.min_active_listings
    save_path = './data/shops'
    key = get_key()
    shops = get_shops(shop_count,min_active_listing,key)
    for shop in shops:
        pprint('shop: {}, id: {} active listings: {}'.format(shop["shop_name"],shop["shop_id"],shop["listing_active_count"]))
    pprint(' ')
    save(shops, save_path)


if __name__ == "__main__":
    main()
