# Kevin Kencana, 18219050

import json
from fastapi import FastAPI, HTTPException, Body, Depends
from model import UserSchema, UserLoginSchema
from auth_handler import signJWT
from auth_bearer import JWTBearer
from auth_handler import signJWT

with open("menu.json", "r") as read_file:
    data = json.load(read_file)
app = FastAPI()

users = []

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return "Username dan password telah terdaftar!"

def check_user(data: UserLoginSchema):
    for user in users:
        if user.username == data.username and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.username)
    return {
        "error": "username tidak terdaftar!"
    }

@app.get('/')
def root():
    return{'Menu':'Item'}

# Ini operasi read/GET
@app.get('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def read_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
        )

# Ini operasi update/PUT
@app.put('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def update_menu(name_menu_awal: str, name_menu_akhir: str): # Nama menu awal adalah nama dari item
    # menu yang sudah ada di dalam file menu, lalu ingin diganti dengan nama_menu_akhir
    for menu_item in data['menu']: 
        if menu_item['name'] == name_menu_awal: #Jika sudah ketemu nama item menu yang ingin diganti
            menu_item['name'] = name_menu_akhir
            read_file.close() #Sementara tutup operasi read file json, karena mau di-write oleh operasi add menu
            with open("menu.json", "w") as write_file: #Buka menu.json sekarang untuk di-write
                json.dump(data,write_file,indent=4) #indent=4 supaya teks yang ditambah jadi bagus
            write_file.close() #operasi write ditutup supaya dapat diread oleh fungsi lain lagi
            return {"message":"Menu has been changed!"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

# Ini operasi DELETE
@app.delete('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def delete_menu(name:str):
    for menu_item in data['menu']: 
        if menu_item['name'] == name: #Jika sudah ketemu nama item menu yang ingin didelete
            id_deleted = menu_item['id'] #menyimpan nilai id dari item yang didelete
            data['menu'].remove(menu_item) #delete menu_item dimana nama item menu yang ingin didelete ditemukan
            # Sekarang, kita mau item menu yang di "belakang" item yang kita hapus untuk maju nilai id sebesar 1
            for menu_item_2 in data['menu']:
                if menu_item_2['id'] > id_deleted:
                    menu_item_2['id'] = menu_item_2['id'] - 1 # Maju 1 id
            read_file.close() #Sementara tutup operasi read file json, karena mau di-write oleh operasi add menu
            with open("menu.json", "w") as write_file: #Buka menu.json sekarang untuk di-write
                json.dump(data,write_file,indent=4) #indent=4 supaya teks yang ditambah jadi bagus
            write_file.close() #operasi write ditutup supaya dapat diread oleh fungsi lain lagi
            return {"message":"Menu has been deleted!"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )


# Ini operasi add/POST
@app.post('/menu', dependencies=[Depends(JWTBearer())])
async def add_menu(name:str):
    id = 1 # Setting id awal sebagai 1
    if (len(data['menu'])>0): #Jika menu sudah ada item, berarti nilai "len" akan lebih dari 0, berarti id
                              #harus geser ke id setelah id item menu terakhir
        id = data['menu'][len(data['menu'])-1]['id'] + 1
    input_data={'id':id,'name':name} #Menyatukan id dan name yang ingin ditambah sebagai bentuk tuple
    data['menu'].append(dict(input_data)) #append input menu baru ke array menu
    #Sekarang menu belum ditambahkan ke file json menu, maka kita perlu write di file json langsung
    read_file.close() #Sementara tutup operasi read file json, karena mau di-write oleh operasi add menu
    with open("menu.json", "w") as write_file: #Buka menu.json sekarang untuk di-write
        json.dump(data,write_file,indent=4) #indent=4 supaya teks yang ditambah jadi bagus
    write_file.close() #operasi write ditutup supaya dapat diread oleh fungsi lain lagi

    return (input_data)
