import csv, json

# the main array that will be stuffed with data and exported to tsv
itemData = []

# used to check for a key's existence before attempting to add its value.
# state_l and state_v were sometimes not present, so I sent the key/value pair to this function
# I expected to have to refactor the entire script to use this function, but no other k/v's required intervention

def checkKey (array, key, deposit):
    if array.has_key(key): 
        deposit = array[key]

# input file needs to be formatted as described in README.

with open('databig.json') as json_file:
    items = json.load(json_file)
    # basic counter, just used in the print line 
    counter = 0
    for j in items:
        id = j['id']
        counter += 1
        # to access the field where the id is the key, the id has to be a string
        str_id = str(id)
        # for checkKey to work, we had to declare the itemObj keys; ended up being unnecessary, could've just done state_l and state_v
        itemObj = {
            'id': id,
            'title': '',
            'prodno': '',
            'publisher': '',
            'date': '',
            'state_l': '',
            'state_v': '',
            'city_us': '',
            'loc_not_us': '',
            'city_not_us': '',
            'body_of_water': '',
            'loc_box_checked': '',
            'category_T10': '',
            'keyword_subj_T11': '',
            'subj_2_T12': '',
            'subj_3_T13': '',
            'category_T15': '',
            'subj_T16': '',
            'incorrect_orientation_T21': '',
            'other_info_T22': '',
        }
        # each field is buried in levels of T0-22.  
        # T0:
        #   T1: caption/title
        # T3:
        #    production number
        #    publisher
        #    date
        # T4:
        #   T5: US state
        #   T6: US city
        #   T7: non-US location (country/region)
        #   T8: non-US city
        #   T18: body of water
        #   T19: a checkbox indicating that there is no location provided; Not checked is NULL (*None* in python); checked is "Unidentified"; 
        # T9: 
        #   T10: "category"; specifics unclear
        #   T11: keyword/subject; specifics unclear
        # T14: 
        #   T12: subject; specifics unclear
        #   T13: subject; specifics unclear
        #   T15: category; specifics unclear
        #   T16: subject; specifics unclear
        # T20: 
        #   T21: postcard scan is incorrected oriented; requires rotation
        #   T22: "other info"; in the dataset, T22 always preceded T21.
        for e in j['val1']:
            if e['task'] == 'T0':
                for n in e['value']:
                    if n['task'] == 'T1':
                        for w in n['value']:
                            if w['tool_label'] == "Caption/Title":
                                itemObj['title'] = w['details'][0]['value']
            if e['task'] == 'T3':
                for n in e['value']:
                    if n['tool_label'] == "Production Number":
                        itemObj['prodno'] = n['details'][0]['value']
                    if n['tool_label'] == "Publisher":
                        itemObj['publisher'] = n['details'][0]['value']
                    if n['tool_label'] == "Date":
                        itemObj['date'] = n['details'][0]['value']
            if e['task'] == 'T4':
                for n in e['value']:
                    if n['task'] == 'T5':
                        checkKey(n['value'][0], 'label', itemObj['state_l'] )
                        checkKey(n['value'][0], 'value', itemObj['state_v'] )
                    if n['task'] == 'T6':
                        itemObj['city_us'] = n['value']
                    if n['task'] == 'T7':
                        itemObj['loc_not_us'] = n['value']
                    if n['task'] == 'T8':
                        itemObj['city_not_us'] = n['value']
                    if n['task'] == 'T18':
                        itemObj['body_of_water'] = n['value']
                    if n['task'] == 'T19':
                        if n['value'] is not None: 
                            itemObj['loc_box_checked'] = n['value']
            if e['task'] == 'T9':
                for n in e['value']:
                    if n['task'] == 'T10':
                        itemObj['category_T10'] = n['value'][0]['label']
                    if n['task'] == 'T11':
                        itemObj['keyword_subj_T11'] = n['value']
            if e['task'] == 'T14':
                for n in e['value']:
                    if n['task'] == 'T12': 
                        itemObj['subj_2_T12'] = n['value']
                    if n['task'] == 'T13': 
                        itemObj['subj_3_T13'] = n['value']
                    if n['task'] == 'T15': 
                        itemObj['category_T15'] = n['value'][0]['label']
                    if n['task'] == 'T16': 
                        itemObj['subj_T16'] = n['value']
            if e['task'] == 'T20':
                for n in e['value']:
                    if n['task'] == 'T21': 
                        itemObj['incorrect_orientation_T21'] = n['value']
                    if n['task'] == 'T22': 
                        itemObj['other_info_T22'] = n['value']
        # filename is the only data currently taken from "val2"
        itemObj['filename'] = j['val2'][str_id]['FILENAME']
        # keep track of script while it runs
        print(str(counter) + ': ' + str_id)
        itemData.append(itemObj)

with open('output.tsv', 'w') as output_file:
    dw = csv.DictWriter(output_file, sorted(itemData[0].keys()), delimiter='\t')
    dw.writeheader()
    dw.writerows(itemData)