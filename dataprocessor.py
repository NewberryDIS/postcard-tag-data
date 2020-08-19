import csv, json

itemData = []

# in this script's original run, there were some non-ascii characters which I manually replaced.  
# if there's a non-ascii error, search the dataset for [^\x00-\x7f] and manually fix;
# if there are more than a handful, we can add a substitution to the script.

def checkKey (array, key, deposit):
    if array.has_key(key): 
        deposit = array[key]

with open('databig.json') as json_file:
    items = json.load(json_file)
    index = 0
    for j in items:
        id = j['id']
        index += 1
        str_id = str(id)
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
        print(str(index) + ': ' + str_id)
        itemObj['filename'] = j['val2'][str_id]['FILENAME']
        itemData.append(itemObj)

with open('output.tsv', 'w') as output_file:
    dw = csv.DictWriter(output_file, sorted(itemData[0].keys()), delimiter='\t')
    dw.writeheader()
    dw.writerows(itemData)