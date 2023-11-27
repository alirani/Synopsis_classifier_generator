from tqdm import tqdm
import requests
import json
import numpy as np

def Scraper_TMDB(ids_json_filepath, export_json_filepath, CUT_IN, call_type, API_BASE_URL, API_KEY):
    with open(ids_json_filepath) as ids:
        ids_list = ids.readlines()
        all_ids_list = [json.loads(each)['id'] for each in ids_list]

    print(f"Got {len(all_ids_list)} IDs from TMDB Json file")

    current_part = 1
    ids_part_list = np.array_split(all_ids_list, CUT_IN)

    for ids_part in ids_part_list:
        data_dict = {}
        index = 0
        for each_id in tqdm(ids_part):
            endpoint_path = f"/{call_type}/{each_id}"
            endpoint = f"{API_BASE_URL + endpoint_path}?api_key={API_KEY}"
            r = requests.get(endpoint)
            data = r.json()
            data_dict[index] = data
            index += 1
        
        with open(f"{export_json_filepath}/{call_type}-{current_part}.json", 'w') as outfile:
            json.dump(data_dict, outfile, indent=2)
        current_part += 1
        print(f"Finished part : {current_part}")