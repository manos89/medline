import pymongo
import unicodedata
import string

def whatisthis(s):
    if isinstance(s, str):
        print("ordinary string")
    elif isinstance(s, unicode):
        print("unicode string")
    else:
        print("not a string")

all_letters = string.ascii_letters +string.digits+'"'+string.ascii_uppercase+" -.,"
n_letters = len(all_letters)

# Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn' and c in all_letters)


def get_ids():
	text=open('patent_ids.txt','r')
	ids=[int(line.strip()) for line in text]
	text.close()
	return ids

ids=get_ids()

USERNAME='manos'
PASSWORD='11Ian19891989'
HOST='d0002332'
PORT='27017'
MONGO_DATABASE='large_papers'
count=1
client = pymongo.MongoClient('mongodb://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+MONGO_DATABASE)
db = client['large_papers']
text=open('Medline.txt','wb')
results=db['patents'].find({'id':{'$in':ids}})

for r in results:
	try:
		brief_text=''
		patent_id=str(r['id'])
		title='TI  - '+str(r['title']).strip().lstrip()
		abstract='AB  - '+str(r['abstract']).strip().lstrip()
		brief_results=db['brf_sum_text'].find_one({'patent_id':patent_id})
		if brief_results:
			brief_text=' '+str(brief_results['text'])
		patent_id_write=unicodeToAscii('PMID- '+patent_id)
		full_text=abstract.strip().lstrip().rstrip()+' '+brief_text.strip().lstrip().rstrip()
		text_to_write=str(patent_id_write).strip().lstrip().rstrip()+'\n'+title.strip().lstrip().rstrip()+'\n'+full_text.strip()
		text_to_write=unicodeToAscii(text_to_write)
		text.write(text_to_write[:2500].encode('ascii')+'\n\n'.encode('ascii'))
		count+=1
	except Exception as E:
		text=open('missingids.txt','a')
		text.write(patent_id+'\n')
		text.close()
		print(str(E))

text.close()

