function textmess (mymess){
    return {type: 'text', content: mymess }
}
function cardmess (mymess){
    return {type: 'card', content: { code:'recommend', data:{ list: mymess } } }
}
function cardmess2 (mymess){
    return {type: 'card', content: { code:'promotion', data:{ array:[ {type:'recommend',list: mymess }]} } }
}
function cardmess3 (mymess){
    return {type: 'quick-replies', content: { list: mymess } }
}
function myaction (res,requestType) {
    let frutext = []
    let frucard = []
    for (let j = 0;j < res.length;j++){
        if (res[j].buttons) {
            let arr = []
            for (let i = 0;i < res[j].buttons.length;i++){
                let obj = {}
                let obj2 = {}
                obj['title']=res[j].buttons[i].title
                obj2=res[j].buttons[i].payload
                obj['content']=obj2
                arr.push(obj)
            }
            console.log(arr)
            frucard = [cardmess2(arr)]
        }
    }
    if (res.length>1) {
        let arr2 = []
        for (let i = 0;i < res.length;i++){
            let obj2={}
            obj2['text']=res[i].text
            frutext.push(textmess(obj2))
        }
        if (frucard){
            frutext.push(frucard[0])
        }
        console.log(frutext)
        return frutext
    }
    return {type: 'text', content: { text: res[0].text }}
}