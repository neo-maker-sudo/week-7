const searchBtn = document.getElementById('search');
const updateBtn = document.getElementById('update');
const nameH3 = document.getElementById('name-h3');
const SH3 = document.getElementById('search-h3');
const UP3 = document.getElementById('update-h3');

let SI
let newName

searchBtn.onclick = () => {
    SI = document.getElementById('search-input').value;
    url = `http://127.0.0.1:3000/api/users?username=${SI}`
    fetch(url)
    .then( async (response)=>{
        data = await response.json()
        return data
    })
    .then((result)=>{
        if(result.data === 'null'){
            SH3.textContent = '無此使用者，請重新輸入 !!'
            document.getElementById('search-input').value = '';
        }else{
            SH3.textContent = '姓名:' + result.data.name + ` (帳號:${result.data.username})`
        }
    })
    .catch((err)=>{
        console.log(err)
    })
}

updateBtn.onclick = () =>{
    newName = document.getElementById('update-input').value;
    url = `http://127.0.0.1:3000/api/user`
    fetch(url,{
        method: 'POST',
        body: JSON.stringify({name:newName}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(async(response)=>{
        data = await response.json()
        return data
    })
    .then((result)=>{
        if(result.ok === true){
            UP3.textContent = '更新成功';
            nameH3.textContent = newName;
            document.getElementById('update-input').value = '';
        }
        else if(result.error === 'empty value'){
            UP3.textContent = '請勿輸入空值，請重新輸入'
            document.getElementById('update-input').value = '';
        }
        else if(result.error === 'this name already taken'){
            UP3.textContent = '名字已被取走，請重新輸入';
            document.getElementById('update-input').value = '';
        }
        else if(result.error === 'same name error'){
            UP3.textContent = '請勿重複輸入自己名稱';
            document.getElementById('update-input').value = '';
        }
        else{
            UP3.textContent = '系統錯誤，請稍後再試';
            document.getElementById('update-input').value = '';
        }
    })
    .catch((err)=>{
        console.log(err)
    })
}
