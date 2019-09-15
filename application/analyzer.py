import os, csv, requests, json, time, sys
import scraper, config
from multiprocessing.dummy import Pool as ThreadPool

def get_recent_run(pv_path):
    #find the most timestamp of shops added to the archive 
    scraper.pprint('--get recent run')
    files = os.listdir(pv_path)
    dates = []
    for f in files:
        sub_f = f[:-15]
        if sub_f == "shops":
            lcl_t = f[6:]
            lcl_t = lcl_t[:-4]
            dates.append(lcl_t)

    dates = sorted(dates, reverse=True)
    try:
        date = dates[0]
        return date
    except IndexError:
        scraper.pprint('Data Folder is missing shop lists') 
        return 0

def get_shops(pv_timestamp, key, pv_path):
    #get the shop list from ./data/shops_'timestamp'
    scraper.pprint("--get shops, pv_timestamp: {}".format(pv_timestamp))
    lcl_path = "{}/shops_{}.csv".format(pv_path,pv_timestamp)
    shops = []
    try:
        with open(lcl_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = 0
            for row in reader:
                shop = {}
                if count > 0:
                    shop['count'] = row[0]
                    shop['id'] = row[1]
                    shop['name'] = row[2]
                    shop['listings'] = row[3]
                    shop['key'] = key
                    shops.append(shop)
                count+=1
        
    except FileNotFoundError:
        scraper.pprint("FILE NOT FOUND ERROR!! Did you provide an incorrect timestamp?")
        scraper.pprint(" ")
        shop = {}
        shop['count'] = 0
        shop['id'] = 0
        shop['name'] = "Error, FILE NOT FOUND"
        shop['listings'] = "0"
        shop['key'] = "KEY NOT SAVED"
        shops.append(shop)
        
    return shops

def strip_punctuation(pv_list):
    scraper.pprint("--strip punctuation")
    clean_words = []   
    for item in pv_list:
        item = item.strip(',')
        item = item.strip('.')
        item = item.strip('?')
        item = item.strip('!')
        item = item.strip('@')
        item = item.strip('#')
        item = item.strip('\n')
        clean_words.append(item)
    return clean_words

def get_unique_words(pv_list):
    word_set = set()
    for word in pv_list:
        word_set.add(word)
    return word_set

def count_words(word_set, word_list):
    word_gram  = []
    #use word set to build set of unique words
    for w_set in word_set:
        tmp_word = w_set
        count = 0
        #count the occurances of the clean words
        for w_word in word_list:
            if w_set == w_word:
                count+=1
        word_frame = {}
        word_frame['word'] = tmp_word
        word_frame['count'] = count
        word_gram.append(word_frame)
    return word_gram

def word_counter(shop):
    print("shop id: {}, name: {}, listings: {}".format(shop['id'],shop['name'], shop['listings']))
    shop_id = shop['id']
    key = shop['key']
    #returns a distribution chart of the 5 most common terms related to one shop
    scraper.pprint("--word counter, shop_id: {}".format(shop_id))

    #gather data
    url = "https://openapi.etsy.com/v2/shops/{}/listings/active?limit=25&offset=0&api_key={}".format(shop_id, key)
    headers = {'user-agent': 'my-app/0.0.1'}

    r = requests.get(url, headers=headers)
    r_status=r.status_code
    scraper.pprint("API RESPONSE: {}".format(r_status))
    if r_status == 200:
        content = r.content
        d_content = content.decode("utf-8")
        content_json = json.loads(d_content)
        result_string = ''
        #create string
        for result in content_json['results']:
            result_string+=str(result['title'])
            result_string+=str(result['description'])
        
        result_list = result_string.lower().split(' ')    
        clean_words = strip_punctuation(result_list)
        word_set = get_unique_words(clean_words)
        
        
        return_list = []
        return_frame = {}
        return_frame["shop_id"] = shop_id
        return_list.append(return_frame)

        for w in filter_gram(count_words(word_set, clean_words)):
            return_list.append(w)

        scraper.pprint("     Top Terms: {}".format(return_list))
        

    else:
        
        return_dict = {}
        return_dict["word"] = 'Error Code Status {}'.format(r_status)
        return_dict["count"] = 1
        return_list.append(return_dict)
    
    return return_list

def filter_gram(pv_word_gram):
    scraper.pprint("--filter gram")
    return_list = []
    sorted_gram = sorted(pv_word_gram, key = lambda i:i["count"], reverse=True) 
    r_count = 0
    for i in sorted_gram:
        if r_count < 5:
            if not i["word"] in config.stop_words:                
                return_list.append(i)
                r_count+=1
        if r_count ==config.term_count:
            break

    return return_list



def read(pv_list):
    scraper.pprint("--read")
    for item in pv_list:
        scraper.pprint(item)
    return pv_list

def save(distributions, save_path):
    scraper.pprint("--save")
    s_t = '{}'.format(time.time())
    time_split = s_t.split('.')
    e = time_split[0]
    lcl_path = save_path+'_{}.csv'.format(e)
    scraper.pprint('make {}'.format(lcl_path))
    with open(lcl_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "id"
                    ,"shop_id"
                    ,"e_time"
                ]
            )
            lcl_id = 1
            for d in distributions:
                lcl_list = []                
                lcl_list.append(lcl_id)
                lcl_list.append(d)
                lcl_list.append(str(time.time()))   
                writer.writerow(lcl_list)
                lcl_id+=1    

def threaded_counter(shops):
    scraper.pprint('--threader')
    pool = ThreadPool(4)
    results = pool.map(word_counter, shops)
    return results
    
def main():
    scraper.pprint("--'main, analyzer.py'")
    key = scraper.get_key()
    distributions = []
    data_path = config.data_path
    save_path = config.save_path
    arg_length = len(sys.argv)
    if not arg_length == 2:
        timestamp = get_recent_run(data_path)
    if arg_length == 2:
        timestamp = sys.argv[1]
    scraper.pprint('timestamp: {}'.format(timestamp))
    if not timestamp == 0:
        shops = get_shops(timestamp,key, data_path)
        lcl_distributions = threaded_counter(shops)
        for lcl in lcl_distributions:
            distributions.append(lcl)

        save(read(distributions), save_path)
    else:
        scraper.pprint("Please run 'scraper.py' first.")

if __name__ == "__main__":
    main()
