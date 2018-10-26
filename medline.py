import pymongo


USERNAME='manos'
PASSWORD='11Ian19891989'
HOST='d0002332'
PORT='27017'
MONGO_DATABASE='large_papers'
count=1
client = pymongo.MongoClient('mongodb://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+MONGO_DATABASE)
db = client['large_papers']
text=open('Medline.txt','wb')
results=db['patents'].find()
for r in results:
	brief_text=''
	patent_id=str(r['id'])
	title='TI  - '+str(r['title']).strip().lstrip()
	abstract='AB  - '+r['abstract'].strip().lstrip()
	brief_results=db['brf_sum_text'].find_one({'patent_id':patent_id})
	if brief_results:
		brief_text=' '+str(brief_results['text'])
		print(brief_text)
	patent_id_write='PMID- '+patent_id
	full_text=abstract.strip().lstrip().rstrip()+' '+brief_text.strip().lstrip().rstrip()
	text_to_write=patent_id_write.strip().lstrip().rstrip()+'\n'+title.strip().lstrip().rstrip()+'\n'+full_text.strip()
	text.write(text_to_write[:2500].encode('ascii')+'\n\n'.encode('ascii'))
	if count%10==0:
		print(count)
		quit()
	count+=1

text.close()

